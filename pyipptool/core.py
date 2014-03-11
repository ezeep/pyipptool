import functools
import os
import plistlib
import shutil
import subprocess
import tempfile
import time
import threading
import urlparse

import colander

from .forms import (cancel_job_form,
                    release_job_form,
                    create_job_form,
                    create_job_subscription_form,
                    create_printer_subscription_form,
                    cups_add_modify_class_form,
                    cups_add_modify_printer_form,
                    cups_delete_printer_form,
                    cups_delete_class_form,
                    cups_get_classes_form,
                    cups_get_devices_form,
                    cups_get_ppds_form,
                    cups_get_printers_form,
                    cups_move_job_form,
                    cups_reject_jobs_form,
                    get_job_attributes_form,
                    get_jobs_form,
                    get_printer_attributes_form,
                    get_subscriptions_form,
                    get_notifications_form,
                    pause_printer_form,
                    print_job_form,
                    resume_printer_form,
                    send_document_form,
                    hold_new_jobs_form,
                    release_held_new_jobs_form,
                    cancel_subscription_form,
                    )

try:
    from tornado.gen import coroutine, Return, Task
    from tornado.ioloop import TimeoutError
except ImportError:
    def coroutine(f):
        return f

    class TimeoutError(Exception):
        pass

    class Return(Exception):
        def __init__(self, value):
            self.value = value


def pyipptool_coroutine(method):
    """
    Mark the method as a coroutine.
    If use with tornado the side effect of this decorator will be
    cancelled and the original_method will be wrapped by
    tornado.gen.coroutine .
    Otherwise the sync_coroutine_consumer wrapper
    will take care to consume the generator synchronously.
    """
    method.ipptool_caller = True

    @functools.wraps(method)
    def sync_coroutine_consumer(*args, **kw):
        gen = method(*args, **kw)
        while True:
            value = gen.next()
            try:
                gen.send(value)
            except Return as returned:
                return returned.value
            except StopIteration:
                return value
    sync_coroutine_consumer.original_method = method
    return sync_coroutine_consumer


def _get_filename_for_content(content):
    """
    Return the name of a file based on type of content
    - already a file ?
        - does he have a name ?
            take its name
        - else
            copy to temp file and return its name
    - binary content ?
        copy to temp file and return its name

    if a temp file is created the caller is responsible to
    destroy the file. the flag delete is meant for it.
    """
    file_ = None
    delete = False
    if isinstance(content, file):
        # regular file
        file_ = content
    if isinstance(getattr(content, 'file', None), file):
        # tempfile
        file_ = content
    if (hasattr(content, 'read') and hasattr(content, 'read') and
            hasattr(content, 'tell')):
        # most likely a file like object
        file_ = content
    if file_ is not None:
        if file_.name:
            name = file_.name
        else:
            with tempfile.NamedTemporaryFile(delete=False,
                                             mode='rb') as tmp:
                delete = True
                shutil.copyfileobj(file_, tmp)
            name = tmp.name
    elif isinstance(content, basestring):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            delete = True
            tmp.write(content)
        name = tmp.name
    else:
        raise NotImplementedError(
            'Got unknow document\'s content type {}'.format(
                type(content)))

    return name, delete


class MetaAsyncShifter(type):
    """
    Based on async flage defined on IPPToolWrapper
    methods will be decorated by tornado.gen.coroutine otherwise
    with a fake one.
    """
    def __new__(cls, name, bases, attrs):
        klass = super(MetaAsyncShifter, cls).__new__(cls, name, bases, attrs)
        if attrs.get('async'):
            # ASYNC Wrapper
            for method_name in dir(bases[0]):
                method = getattr(bases[0], method_name)
                if getattr(method, 'ipptool_caller', False):
                    # Patch Method with tornado.gen.coroutine
                    setattr(klass, method_name,
                            coroutine(method.original_method))
        return klass


class IPPToolWrapper(object):
    __metaclass__ = MetaAsyncShifter
    async = False

    def __init__(self, config):
        self.config = config

    def authenticate_uri(self, uri):
        if 'login' in self.config and 'password' in self.config:
            parsed_url = urlparse.urlparse(uri)
            authenticated_netloc = '{}:{}@{}'.format(self.config['login'],
                                                     self.config['password'],
                                                     parsed_url.netloc)
            authenticated_uri = urlparse.ParseResult(parsed_url[0],
                                                     authenticated_netloc,
                                                     *parsed_url[2:])
            return authenticated_uri.geturl()
        return uri

    def timeout_handler(self, process, future):
        future.append(True)
        beginning = time.time()
        process.terminate()
        while process.poll() is None:
            if time.time() - beginning > self.config['graceful_shutdown_time']:
                try:
                    process.kill()
                except OSError:
                    pass
                break
            time.sleep(.1)

    def _call_ipptool(self, uri, request):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(request)
        process = subprocess.Popen([self.config['ipptool_path'],
                                    self.authenticate_uri(uri),
                                    '-X',
                                    temp_file.name],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        future = []
        timer = threading.Timer(self.config['timeout'],
                                self.timeout_handler, (process, future))
        timer.start()
        try:
            stdout, stderr = process.communicate()
        finally:
            os.unlink(temp_file.name)
        timer.cancel()
        if future:
            raise TimeoutError
        return plistlib.readPlistFromString(stdout)['Tests'][0]

    @pyipptool_coroutine
    def release_job(self, uri,
                    printer_uri=colander.null,
                    job_id=colander.null,
                    job_uri=colander.null):
        kw = {'header': {'operation_attributes':
                         {'printer_uri': printer_uri,
                          'job_id': job_id,
                          'job_uri': job_uri}}}
        request = release_job_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cancel_job(self, uri,
                   printer_uri=colander.null,
                   job_id=colander.null,
                   job_uri=colander.null,
                   purge_job=colander.null):
        kw = {'header': {'operation_attributes':
                         {'printer_uri': printer_uri,
                          'job_id': job_id,
                          'job_uri': job_uri,
                          'purge_job': purge_job}}}
        request = cancel_job_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def create_job(self, uri,
                   printer_uri=None,
                   auth_info=colander.null,
                   job_billing=colander.null,
                   job_sheets=colander.null,
                   media=colander.null):
        kw = {'header':
              {'operation_attributes':
               {'printer_uri': printer_uri}},
              'auth_info': auth_info,
              'job_billing': job_billing,
              'job_sheets': job_sheets,
              'media': media}
        request = create_job_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def print_job(self, uri,
                  printer_uri=None,
                  auth_info=colander.null,
                  job_billing=colander.null,
                  job_sheets=colander.null,
                  media=colander.null,
                  document_content=None):
        filename, delete = _get_filename_for_content(document_content)
        kw = {'header':
              {'operation_attributes':
               {'printer_uri': printer_uri}},
              'auth_info': auth_info,
              'job_billing': job_billing,
              'job_sheets': job_sheets,
              'media': media,
              'file': filename}
        request = print_job_form.render(kw)
        try:
            response = yield self._call_ipptool(uri, request)
            raise Return(response)
        finally:
            if delete:
                os.unlink(filename)

    @pyipptool_coroutine
    def create_job_subscription(self,
                                uri,
                                printer_uri=None,
                                requesting_user_name=None,
                                notify_job_id=None,
                                notify_recipient_uri=colander.null,
                                notify_pull_method=colander.null,
                                notify_events=colander.null,
                                notify_attributes=colander.null,
                                notify_charset=colander.null,
                                notify_natural_language=colander.null,
                                notify_time_interval=colander.null):
        """
        Create a per-job subscription object.
        """
        kw = {'header': {'operation_attributes':
                         {'printer_uri': printer_uri,
                          'requesting_user_name': requesting_user_name,
                          'notify_job_id': notify_job_id}},
              'notify_recipient_uri': notify_recipient_uri,
              'notify_pull_method': notify_pull_method,
              'notify_events': notify_events,
              'notify_attributes': notify_attributes,
              'notify_charset': notify_charset,
              'notify_natural_language': notify_natural_language,
              'notify_time_interval': notify_time_interval}
        request = create_job_subscription_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def create_printer_subscription(
            self,
            uri,
            printer_uri=None,
            requesting_user_name=None,
            notify_recipient_uri=colander.null,
            notify_pull_method=colander.null,
            notify_events=colander.null,
            notify_attributes=colander.null,
            notify_charset=colander.null,
            notify_natural_language=colander.null,
            notify_lease_duration=colander.null,
            notify_time_interval=colander.null):
        """
        Create a new subscription and return its id
        """
        kw = {'header': {'operation_attributes':
                         {'printer_uri': printer_uri,
                          'requesting_user_name': requesting_user_name}},
              'notify_recipient_uri': notify_recipient_uri,
              'notify_pull_method': notify_pull_method,
              'notify_events': notify_events,
              'notify_attributes': notify_attributes,
              'notify_charset': notify_charset,
              'notify_natural_language': notify_natural_language,
              'notify_lease_duration': notify_lease_duration,
              'notify_time_interval': notify_time_interval}
        request = create_printer_subscription_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_add_modify_printer(self, uri,
                                printer_uri=None,
                                auth_info_required=colander.null,
                                job_sheets_default=colander.null,
                                device_uri=colander.null,
                                port_monitor=colander.null,
                                ppd_name=colander.null,
                                printer_is_accepting_jobs=colander.null,
                                printer_info=colander.null,
                                printer_location=colander.null,
                                printer_more_info=colander.null,
                                printer_op_policy=colander.null,
                                printer_state=colander.null,
                                printer_state_message=colander.null,
                                requesting_user_name_allowed=colander.null,
                                requesting_user_name_denied=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri}},
              'auth_info_required': auth_info_required,
              'job_sheets_default': job_sheets_default,
              'device_uri': device_uri,
              'port_monitor': port_monitor,
              'ppd_name': ppd_name,
              'printer_is_accepting_jobs': printer_is_accepting_jobs,
              'printer_info': printer_info,
              'printer_location': printer_location,
              'printer_more_info': printer_more_info,
              'printer_op_policy': printer_op_policy,
              'printer_state': printer_state,
              'printer_state_message': printer_state_message,
              'requesting_user_name_allowed ': requesting_user_name_allowed,
              'requesting_user_name_denied': requesting_user_name_denied,
              }

        request = cups_add_modify_printer_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_add_modify_class(self, uri,
                              printer_uri=None,
                              auth_info_required=colander.null,
                              member_uris=colander.null,
                              printer_is_accepting_jobs=colander.null,
                              printer_info=colander.null,
                              printer_location=colander.null,
                              printer_more_info=colander.null,
                              printer_op_policy=colander.null,
                              printer_state=colander.null,
                              printer_state_message=colander.null,
                              requesting_user_name_allowed=colander.null,
                              requesting_user_name_denied=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri}},
              'auth_info_required': auth_info_required,
              'member_uris': member_uris,
              'printer_is_accepting_jobs': printer_is_accepting_jobs,
              'printer_info': printer_info,
              'printer_location': printer_location,
              'printer_more_info': printer_more_info,
              'printer_op_policy': printer_op_policy,
              'printer_state': printer_state,
              'printer_state_message': printer_state_message,
              'requesting_user_name_allowed ': requesting_user_name_allowed,
              'requesting_user_name_denied': requesting_user_name_denied,
              }

        request = cups_add_modify_class_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_delete_printer(self, uri, printer_uri=None):
        kw = {'header': {'operation_attributes': {'printer_uri': printer_uri}}}
        request = cups_delete_printer_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_delete_class(self, uri, printer_uri=None):
        kw = {'header': {'operation_attributes': {'printer_uri': printer_uri}}}
        request = cups_delete_class_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_get_classes(self, uri,
                         first_printer_name=colander.null,
                         limit=colander.null,
                         printer_location=colander.null,
                         printer_type=colander.null,
                         printer_type_mask=colander.null,
                         requested_attributes=colander.null,
                         requested_user_name=colander.null):
        kw = {'header': {'operation_attributes':
                        {'first_printer_name': first_printer_name,
                         'limit': limit,
                         'printer_location': printer_location,
                         'printer_type': printer_type,
                         'printer_type_mask': printer_type_mask,
                         'requested_attributes': requested_attributes,
                         'requested_user_name': requested_user_name}}}
        request = cups_get_classes_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_get_devices(self, uri,
                         device_class=colander.null,
                         exclude_schemes=colander.null,
                         include_schemes=colander.null,
                         limit=colander.null,
                         requested_attributes=colander.null,
                         timeout=colander.null):
        kw = {'header': {'operation_attributes':
                        {'device_class': device_class,
                         'exclude_schemes': exclude_schemes,
                         'include-schemes': include_schemes,
                         'limit': limit,
                         'requested_attributes': requested_attributes,
                         'timeout': timeout}}}
        request = cups_get_devices_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_get_ppds(self, uri,
                      exclude_schemes=colander.null,
                      include_schemes=colander.null,
                      limit=colander.null,
                      ppd_make=colander.null,
                      ppd_make_and_model=colander.null,
                      ppd_model_number=colander.null,
                      ppd_natural_language=colander.null,
                      ppd_product=colander.null,
                      ppd_psversion=colander.null,
                      ppd_type=colander.null,
                      requested_attributes=colander.null):
        kw = {'header': {'operation_attributes':
                        {'exclude_schemes': exclude_schemes,
                         'include_schemes': include_schemes,
                         'limit': limit,
                         'ppd_make': ppd_make,
                         'ppd_make_and_model': ppd_make_and_model,
                         'ppd_model_number': ppd_model_number,
                         'ppd_natural_language': ppd_natural_language,
                         'ppd_product': ppd_product,
                         'ppd_psversion': ppd_psversion,
                         'ppd_type': ppd_type,
                         'requested_attributes': requested_attributes
                         }}}
        request = cups_get_ppds_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_get_printers(self, uri,
                          first_printer_name=colander.null,
                          limit=colander.null,
                          printer_location=colander.null,
                          printer_type=colander.null,
                          printer_type_mask=colander.null,
                          requested_attributes=colander.null,
                          requested_user_name=colander.null):
        kw = {'header': {'operation_attributes':
                        {'first_printer_name': first_printer_name,
                         'limit': limit,
                         'printer_location': printer_location,
                         'printer_type': printer_type,
                         'printer_type_mask': printer_type_mask,
                         'requested_attributes': requested_attributes,
                         'requested_user_name': requested_user_name}}}
        request = cups_get_printers_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_move_job(self, uri,
                      printer_uri=colander.null,
                      job_id=colander.null,
                      job_uri=colander.null,
                      job_printer_uri=None,
                      printer_state_message=None):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri,
                         'job_id': job_id,
                         'job_uri': job_uri}},
              'job_printer_uri': job_printer_uri,
              'printer_state_message': printer_state_message}
        request = cups_move_job_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cups_reject_jobs(self, uri,
                         printer_uri=None,
                         requesting_user_name=None,
                         printer_state_message=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri,
                         'requesting_user_name': requesting_user_name}},
              'printer_state_message': printer_state_message}
        request = cups_reject_jobs_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def get_job_attributes(self, uri,
                           printer_uri=colander.null,
                           job_id=colander.null,
                           job_uri=colander.null,
                           requesting_user_name=colander.null,
                           requested_attributes=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri,
                         'job_id': job_id,
                         'job_uri': job_uri,
                         'requesting_user_name': requesting_user_name,
                         'requested_attributes': requested_attributes}}}
        request = get_job_attributes_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def get_jobs(self, uri,
                 printer_uri=None,
                 requesting_user_name=colander.null,
                 limit=colander.null,
                 requested_attributes=colander.null,
                 which_jobs=colander.null,
                 my_jobs=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri,
                         'requesting_user_name': requesting_user_name,
                         'limit': limit,
                         'requested_attributes': requested_attributes,
                         'which_jobs': which_jobs,
                         'my_jobs': my_jobs}}}
        request = get_jobs_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def get_printer_attributes(self, uri,
                               printer_uri=None,
                               requesting_user_name=colander.null,
                               requested_attributes=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri,
                         'requesting_user_name': requesting_user_name,
                         'requested_attributes': requested_attributes}}}
        request = get_printer_attributes_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def get_subscriptions(self, uri,
                          printer_uri=None,
                          requesting_user_name=colander.null,
                          notify_job_id=colander.null,
                          limit=colander.null,
                          requested_attributes=colander.null,
                          my_subscriptions=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri,
                         'requesting_user_name': requesting_user_name,
                         'notify_job_id': notify_job_id,
                         'limit': limit,
                         'requested_attributes': requested_attributes,
                         'my_subscriptions': my_subscriptions}}}
        request = get_subscriptions_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def get_notifications(self,
                          uri,
                          printer_uri=None,
                          notify_subscription_ids=None,
                          requesting_user_name=colander.null,
                          notify_sequence_numbers=colander.null,
                          notify_wait=colander.null):
        kw = {'header':
              {'operation_attributes':
                  {'printer_uri': printer_uri,
                   'requesting_user_name': requesting_user_name,
                   'notify_subscription_ids': notify_subscription_ids,
                   'notify_sequence_numbers': notify_sequence_numbers,
                   'notify_wait': notify_wait}}}
        request = get_notifications_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def cancel_subscription(self, uri,
                            printer_uri=None,
                            requesting_user_name=colander.null,
                            notify_subscription_id=None):
        kw = {'header':
              {'operation_attributes':
               {'printer_uri': printer_uri,
                'requesting_user_name': requesting_user_name,
                'notify_subscription_id': notify_subscription_id}}}
        request = cancel_subscription_form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    @pyipptool_coroutine
    def _pause_or_resume_printer(self, form, uri, printer_uri=None,
                                 requesting_user_name=colander.null):
        kw = {'header': {'operation_attributes':
                        {'printer_uri': printer_uri,
                         'requesting_user_name': requesting_user_name}}}
        request = form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    def pause_printer(self, *args, **kw):
        return self._pause_or_resume_printer(pause_printer_form, *args, **kw)

    def resume_printer(self, *args, **kw):
        return self._pause_or_resume_printer(resume_printer_form, *args, **kw)

    @pyipptool_coroutine
    def _hold_or_release_new_jobs(self, form, uri, printer_uri=None,
                                  requesting_user_name=colander.null,
                                  printer_message_from_operator=colander.null):
        kw = {
            'header': {
                'operation_attributes':
                {'printer_uri': printer_uri,
                 'requesting_user_name': requesting_user_name,
                 'printer_message_from_operator': printer_message_from_operator
                 }}}
        request = form.render(kw)
        response = yield self._call_ipptool(uri, request)
        raise Return(response)

    def hold_new_jobs(self, *args, **kw):
        return self._hold_or_release_new_jobs(hold_new_jobs_form, *args, **kw)

    def release_held_new_jobs(self, *args, **kw):
        return self._hold_or_release_new_jobs(release_held_new_jobs_form,
                                              *args, **kw)

    @pyipptool_coroutine
    def send_document(self, uri,
                      job_uri=colander.null,
                      printer_uri=colander.null,
                      job_id=colander.null,
                      requesting_user_name=None,
                      document_name=colander.null,
                      compression=colander.null,
                      document_format='application/pdf',
                      document_natural_language=colander.null,
                      last_document=True,
                      document_content=None,
                      ):
        """
        :param document_content: Binary Content or Named File
        """
        delete = False
        filename, delete = _get_filename_for_content(document_content)
        kw = {'header':
              {'operation_attributes':
               {'job_uri': job_uri,
                'printer_uri': printer_uri,
                'job_id': job_id,
                'requesting_user_name': requesting_user_name,
                'document_name': document_name,
                'compression': compression,
                'document_format': document_format,
                'document_natural_language': document_natural_language,
                'last_document': last_document}},
              'file': filename}
        request = send_document_form.render(kw)
        try:
            response = yield self._call_ipptool(uri, request)
            raise Return(response)
        finally:
            if delete:
                os.unlink(filename)


class AsyncIPPToolWrapper(IPPToolWrapper):
    async = True

    def __init__(self, config, io_loop):
        self.config = config
        self.io_loop = io_loop

    @coroutine
    def _call_ipptool(self, uri, request):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(request)
        from tornado.process import Subprocess
        process = Subprocess([self.config['ipptool_path'],
                              self.authenticate_uri(uri), '-X',
                              temp_file.name],
                             stdin=subprocess.PIPE,
                             stdout=Subprocess.STREAM,
                             stderr=Subprocess.STREAM,
                             io_loop=self.io_loop)
        future = []
        self.io_loop.add_timeout(self.io_loop.time() + self.config['timeout'],
                                 functools.partial(self.timeout_handler,
                                                   process.proc, future))
        try:
            stdout, stderr = yield [Task(process.stdout.read_until_close),
                                    Task(process.stderr.read_until_close)]
            if future:
                raise TimeoutError
        finally:
            os.unlink(temp_file.name)

        raise Return(plistlib.readPlistFromString(stdout)['Tests'][0])
