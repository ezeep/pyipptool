import ConfigParser
import os
import plistlib
import subprocess
import tempfile
import urlparse

import colander
from .forms import (create_printer_subscription_form,
                    cups_add_modify_printer_form,
                    cups_get_printers_form,
                    cups_move_job_form,
                    cups_reject_jobs_form)


config = ConfigParser.SafeConfigParser()
config.read(['/etc/pyipptool/pyipptool.cfg',
             os.path.join(os.path.expanduser('~'), '.pyipptool.cfg')])
ipptool_path = config.get('main', 'ipptool_path')


def authenticate_printer_uri(printer_uri):
    login = config.get('main', 'login')
    password = config.get('main', 'password')
    if login:
        parsed_url = urlparse.urlparse(printer_uri)
        authenticated_netloc = '{}:{}@{}'.format(login, password,
                                                 parsed_url.netloc)
        authenticated_printer_uri = urlparse.ParseResult(parsed_url[0],
                                                         authenticated_netloc,
                                                         *parsed_url[2:])
        return authenticated_printer_uri.geturl()
    return printer_uri


def _call_ipptool(printer_uri, request):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(request)
    process = subprocess.Popen([ipptool_path,
                                authenticate_printer_uri(printer_uri),
                                '-X',
                                temp_file.name],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate()
    finally:
        os.unlink(temp_file.name)
    assert process.returncode == 0, stderr
    return plistlib.readPlistFromString(stdout)


def create_printer_subscription(printer_uri=None,
                                requesting_user_name=None,
                                notify_recipient_uri=None,
                                notify_events=None,
                                notify_lease_duration=colander.null,
                                notify_lease_expiration_time=colander.null):
    """
    Create a new subscription and return its id
    """
    kw = dict(header={'required_attributes':
                      {'printer_uri': printer_uri,
                       'requesting_user_name': requesting_user_name}},
              notify_recipient_uri=notify_recipient_uri,
              notify_events=notify_events,
              notify_lease_duration=notify_lease_duration,
              notify_lease_expiration_time=notify_lease_expiration_time)
    request = create_printer_subscription_form.render(kw)
    response = _call_ipptool(printer_uri, request)
    return response['Tests'][0]['notify-subscription-id']


def cups_add_modify_printer_request(printer_uri=None, device_uri=None):
    kw = {'printer_uri': printer_uri, 'device_uri': device_uri}
    request = cups_add_modify_printer_form.render(kw)
    response = _call_ipptool(printer_uri, request)
    assert response['Tests'][0]['StatusCode'] == 'successful-ok', response
    return True


def cups_get_printers_request(printer_uri=None,
                              first_printer_name=colander.null,
                              limit=colander.null,
                              printer_location=colander.null,
                              printer_type=colander.null,
                              printer_type_mask=colander.null,
                              requested_attributes=colander.null,
                              requested_user_name=colander.null):
    kw = {'header': {'required_attributes':
                     {'printer_uri': printer_uri,
                      'first_printer_name': first_printer_name,
                      'limit': limit,
                      'printer_location': printer_location,
                      'printer_type': printer_type,
                      'printer_type_mask': printer_type_mask,
                      'requested_attributes': requested_attributes,
                      'requested_user_name': requested_user_name}}}
    request = cups_get_printers_form.render(kw)
    response = _call_ipptool(printer_uri, request)
    assert response['Tests'][0]['StatusCode'] == 'successful-ok', response
    return response['Tests'][0]['ResponseAttributes']


def cups_move_job_request(printer_uri=colander.null,
                          job_id=colander.null,
                          job_uri=colander.null,
                          job_printer_uri=None,
                          printer_state_message=None):
    kw = dict(header={'required_attributes':
                      {'printer_uri': printer_uri,
                       'job_id': job_id,
                       'job_uri': job_uri}},
              job_printer_uri=job_printer_uri,
              printer_state_message=printer_state_message)
    request = cups_move_job_form.render(kw)
    response = _call_ipptool(printer_uri, request)
    assert response['Tests'][0]['StatusCode'] == 'successful-ok', response
    return True


def cups_reject_jobs_request(printer_uri=None,
                             requesting_user_name=None,
                             printer_state_message=colander.null):
    kw = dict(header={'required_attributes':
                      {'printer_uri': printer_uri,
                       'requesting_user_name': requesting_user_name}},
              printer_state_message=printer_state_message)
    request = cups_reject_jobs_form.render(kw)
    response = _call_ipptool(printer_uri, request)
    assert response['Tests'][0]['StatusCode'] == 'successful-ok', response
    return True
