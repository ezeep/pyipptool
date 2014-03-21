import BaseHTTPServer
import os.path
import SocketServer
import socket
import tempfile
import threading
import time

import mock
import pytest

import pyipptool


@pytest.mark.xfail
@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_ipptool_create_job_subscription_pull_delivery_method(_call_ipptool):
    from pyipptool import create_job_subscription
    create_job_subscription(
        'https://localhost:631/',
        printer_uri='https://localhost:631/printer/p',
        requesting_user_name='admin',
        notify_job_id=108,
        notify_recipient_uri='rss://',
        notify_events=('job-completed', 'job-created', 'job-progress'),
        notify_attributes='notify-subscriber-user-name',
        notify_charset='utf-8',
        notify_natural_language='de',
        notify_time_interval=1)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'printer-uri https://localhost:631/printer/p' in request
    assert 'requesting-user-name admin' in request
    assert 'notify-job-id 108' in request
    assert 'notify-recipient-uri rss://' in request
    assert 'notify-events job-completed,job-created,job-progress' in request
    assert 'notify-attributes notify-subscriber-user-name' in request
    assert 'notify-charset utf-8' in request
    assert 'notify-natural-language de' in request
    assert 'notify-time-interval 1' in request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_ipptool_create_printer_subscription(_call_ipptool):
    from pyipptool import create_printer_subscription
    create_printer_subscription(
        'https://localhost:631/',
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        requesting_user_name='admin',
        notify_recipient_uri='rss://',
        notify_events='all',
        notify_attributes='notify-subscriber-user-name',
        notify_charset='utf-8',
        notify_natural_language='de',
        notify_lease_duration=0,
        notify_time_interval=1)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'requesting-user-name admin' in request, request
    assert 'printer-uri https://localhost:631/classes/PUBLIC-PDF' in request
    assert 'notify-recipient-uri rss://' in request
    assert 'notify-events all' in request
    assert 'notify-attributes notify-subscriber-user-name' in request
    assert 'notify-charset utf-8' in request
    assert 'notify-natural-language de' in request
    assert 'notify-lease-duration 0' in request
    assert 'notify-time-interval 1' in request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_add_modify_printer(_call_ipptool):
    from pyipptool import cups_add_modify_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_add_modify_printer(
        'https://localhost:631/',
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        device_uri='cups-pdf:/',
        printer_is_shared=False,
    )
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'printer-uri https://localhost:631/classes/PUBLIC-PDF' in request
    assert 'device-uri cups-pdf:/' in request
    assert 'ATTR boolean printer-is-shared 0' in request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_job_attributes_with_job_id(_call_ipptool):
    from pyipptool import get_job_attributes
    get_job_attributes(
        'https://localhost:631/',
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        job_id=2)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'printer-uri https://localhost:631/classes/PUBLIC-PDF' in request
    assert 'job-id 2' in request
    assert 'job-uri' not in request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_job_attributes_with_job_uri(_call_ipptool):
    from pyipptool import get_job_attributes
    get_job_attributes(
        'https://localhost:631/',
        job_uri='https://localhost:631/jobs/2')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'job-uri https://localhost:631/jobs/2' in request
    assert 'printer-uri' not in request


def test_timeout():
    from pyipptool import wrapper
    from pyipptool.core import TimeoutError
    from pyipptool.forms import get_subscriptions_form

    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
        """
        HTTP Handler that will make ipptool waiting
        """

        def do_POST(self):
            time.sleep(.2)
            assassin = threading.Thread(target=self.server.shutdown)
            assassin.daemon = True
            assassin.start()

    PORT = 6789
    while True:
        try:
            httpd = SocketServer.TCPServer(("", PORT), Handler)
        except socket.error as exe:
            if exe.errno in (48, 98):
                PORT += 1
            else:
                raise
        else:
            break
    httpd.allow_reuse_address = True

    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    request = get_subscriptions_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri':
           'http://localhost:%s/printers/fake' % PORT}}})

    old_timeout = wrapper.config['timeout']
    wrapper.config['timeout'] = .1
    try:
        with pytest.raises(TimeoutError):
            wrapper._call_ipptool('http://localhost:%s/' % PORT, request)
    finally:
        wrapper.config['timeout'] = old_timeout


def test_authentication():
    from pyipptool import IPPToolWrapper
    wrapper = IPPToolWrapper({'login': 'ezeep',
                              'password': 'secret'})

    assert (wrapper.authenticate_uri(
        'http://localhost:631/printers/?arg=value') ==
        'http://ezeep:secret@localhost:631/printers/?arg=value')


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_release_job(_call_ipptool):
    from pyipptool import release_job
    _call_ipptool.return_value = {'Tests': [{}]}
    release_job('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cancel_job(_call_ipptool):
    from pyipptool import cancel_job
    _call_ipptool.return_value = {'Tests': [{}]}
    cancel_job('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_add_modify_class(_call_ipptool):
    from pyipptool import cups_add_modify_class
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_add_modify_class('https://localhost:631/',
                          printer_uri='',
                          printer_is_shared=True)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'ATTR boolean printer-is-shared 1' in request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_delete_printer(_call_ipptool):
    from pyipptool import cups_delete_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_delete_printer('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_delete_class(_call_ipptool):
    from pyipptool import cups_delete_class
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_delete_class('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_classes(_call_ipptool):
    from pyipptool import cups_get_classes
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_classes('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_printers(_call_ipptool):
    from pyipptool import cups_get_printers
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_printers('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_devices(_call_ipptool):
    from pyipptool import cups_get_devices
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_devices('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_ppds(_call_ipptool):
    from pyipptool import cups_get_ppds
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_ppds('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_move_job(_call_ipptool):
    from pyipptool import cups_move_job
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_move_job('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_reject_jobs(_call_ipptool):
    from pyipptool import cups_reject_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_reject_jobs('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_jobs(_call_ipptool):
    from pyipptool import get_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    get_jobs('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_printer_attributes(_call_ipptool):
    from pyipptool import get_printer_attributes
    _call_ipptool.return_value = {'Tests': [{}]}
    get_printer_attributes('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_subscriptions(_call_ipptool):
    from pyipptool import get_subscriptions
    _call_ipptool.return_value = {'Tests': [{}]}
    get_subscriptions('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_notifications(_call_ipptool):
    from pyipptool import get_notifications
    _call_ipptool.return_value = {'Tests': [{}]}
    get_notifications('https://localhost:631/',
                      printer_uri='',
                      notify_subscription_ids=3)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_pause_printer(_call_ipptool):
    from pyipptool import pause_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    pause_printer('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_hold_new_jobs(_call_ipptool):
    from pyipptool import hold_new_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    hold_new_jobs('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_release_held_new_jobs(_call_ipptool):
    from pyipptool import release_held_new_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    release_held_new_jobs('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_resume_printer(_call_ipptool):
    from pyipptool import resume_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    resume_printer('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cancel_subscription(_call_ipptool):
    from pyipptool import cancel_subscription
    _call_ipptool.return_value = {'Tests': [{}]}
    cancel_subscription('https://localhost:631/',
                        printer_uri='',
                        notify_subscription_id=3)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_create_job(_call_ipptool):
    from pyipptool import create_job
    _call_ipptool.return_value = {'Tests': [{}]}
    create_job('https://localhost:631/',
               printer_uri='',
               job_name='foo',
               job_priority=1,
               job_hold_until='indefinite',
               job_sheets='standard',
               multiple_document_handling='single-document',
               copies=2,
               finishings='punch',
               page_ranges='1-6',
               sides='two-sided-short-edge',
               number_up=4,
               orientation_requested='reverse-landscape',
               media='iso-a4-white',
               printer_resolution='600dpi',
               print_quality='5',
               ipp_attribute_fidelity=False,
               job_k_octets=1024,
               job_impressions=2048,
               job_media_sheets=2,
               )
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_print_job(_call_ipptool):
    from pyipptool import print_job
    _call_ipptool.return_value = {'Tests': [{}]}
    with open(os.path.join(os.path.dirname(__file__),
                           'hello.pdf'), 'rb') as tmp:
        print_job('https://localhost:631/',
                  printer_uri='',
                  job_name='foo',
                  ipp_attribute_fidelity=False,
                  document_name='foo.txt',
                  compression='gzip',
                  document_format='text/plain',
                  document_natural_language='en',
                  job_k_octets=1024,
                  job_impressions=2048,
                  job_media_sheets=2,
                  job_priority=1,
                  job_hold_until='indefinite',
                  job_sheets='standard',
                  multiple_document_handling='single-document',
                  copies=2,
                  finishings='punch',
                  page_ranges='1-6',
                  sides='two-sided-short-edge',
                  number_up=4,
                  orientation_requested='reverse-landscape',
                  media='iso-a4-white',
                  printer_resolution='600dpi',
                  print_quality='5',
                  document_content=tmp.read())
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    assert 'FILE /tmp/' in _call_ipptool._mock_mock_calls[0][1][-1]


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_send_document_with_file(_call_ipptool):
    from pyipptool import send_document
    _call_ipptool.return_value = {'Tests': [{}]}

    with tempfile.NamedTemporaryFile('rb') as tmp:
        send_document('https://localhost:631/',
                      document_content=tmp)
        assert (_call_ipptool._mock_mock_calls[0][1][0] ==
                'https://localhost:631/')
        assert ('FILE {}'.format(tmp.name)
                in _call_ipptool._mock_mock_calls[0][1][-1])


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_send_document_with_binary(_call_ipptool):
    from pyipptool import send_document
    _call_ipptool.return_value = {'Tests': [{}]}

    with open(os.path.join(os.path.dirname(__file__),
                           'hello.pdf'), 'rb') as tmp:
        send_document('https://localhost:631/',
                      document_content=tmp.read())
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    assert 'FILE /tmp/' in _call_ipptool._mock_mock_calls[0][1][-1]
