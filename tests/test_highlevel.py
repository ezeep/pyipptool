import BaseHTTPServer
import SocketServer
import functools
import threading
import time

import mock
import pytest

import pyipptool


def patch_config(**kwconfig):
    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kw):
            import pyipptool
            old_values = {}
            for k, v in kwconfig.items():
                old_values[k] = getattr(pyipptool, k)
                setattr(pyipptool, k, v)
            try:
                return fn(*args, **kw)
            finally:
                for k, v in old_values.items():
                    setattr(pyipptool, k, v)
        return inner
    return wrapper


@mock.patch.object(pyipptool, '_call_ipptool')
def test_ipptool_create_printer_subscription(_call_ipptool):
    from pyipptool import create_printer_subscription
    create_printer_subscription(
        'https://localhost:631/',
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        requesting_user_name='ecp_admin',
        notify_recipient_uri='ezpnotifier://',
        notify_events='all',
        notify_lease_duration=0,
        notify_lease_expiration_time=0)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'requesting-user-name ecp_admin' in request, request
    assert 'printer-uri https://localhost:631/classes/PUBLIC-PDF' in request
    assert 'notify-recipient-uri ezpnotifier://' in request
    assert 'notify-events all' in request
    assert 'notify-lease-duration 0' in request
    assert 'notify-lease-expiration-time 0' in request


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_add_modify_printer(_call_ipptool):
    from pyipptool import cups_add_modify_printer
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    cups_add_modify_printer(
        'https://localhost:631/',
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        device_uri='cups-pdf:/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'printer-uri https://localhost:631/classes/PUBLIC-PDF' in request
    assert 'device-uri cups-pdf:/' in request


@mock.patch.object(pyipptool, '_call_ipptool')
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


@mock.patch.object(pyipptool, '_call_ipptool')
def test_get_job_attributes_with_job_uri(_call_ipptool):
    from pyipptool import get_job_attributes
    get_job_attributes(
        'https://localhost:631/',
        job_uri='https://localhost:631/jobs/2')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'job-uri https://localhost:631/jobs/2' in request
    assert 'printer-uri' not in request


@patch_config(TIMEOUT=1)
def test_timeout():
    from pyipptool import TimeoutError, _call_ipptool
    from pyipptool.forms import get_subscriptions_form
    PORT = 6789

    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
        """
        HTTP Handler that will make ipptool waiting
        """

        def do_POST(self):
            time.sleep(2)
            assassin = threading.Thread(target=self.server.shutdown)
            assassin.daemon = True
            assassin.start()

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    request = get_subscriptions_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri':
           'http://localhost:%s/printers/fake' % PORT}}})
    with pytest.raises(TimeoutError):
        _call_ipptool('http://localhost:%s/' % PORT, request)


@patch_config(LOGIN='ezeep', PASSWORD='secret')
def test_authentication():
    from pyipptool import authenticate_uri

    assert (authenticate_uri('http://localhost:631/printers/?arg=value') ==
            'http://ezeep:secret@localhost:631/printers/?arg=value')


@mock.patch.object(pyipptool, '_call_ipptool')
def test_release_job(_call_ipptool):
    from pyipptool import release_job
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    release_job('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cancel_job(_call_ipptool):
    from pyipptool import cancel_job
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    cancel_job('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_add_modify_class(_call_ipptool):
    from pyipptool import cups_add_modify_class
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    cups_add_modify_class('https://localhost:631/',
                          printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_delete_printer(_call_ipptool):
    from pyipptool import cups_delete_printer
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    cups_delete_printer('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_delete_class(_call_ipptool):
    from pyipptool import cups_delete_class
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    cups_delete_class('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_get_classes(_call_ipptool):
    from pyipptool import cups_get_classes
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    cups_get_classes('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_get_printers(_call_ipptool):
    from pyipptool import cups_get_printers
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    cups_get_printers('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_get_devices(_call_ipptool):
    from pyipptool import cups_get_devices
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    cups_get_devices('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_get_ppds(_call_ipptool):
    from pyipptool import cups_get_ppds
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    cups_get_ppds('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_move_job(_call_ipptool):
    from pyipptool import cups_move_job
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    cups_move_job('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cups_reject_jobs(_call_ipptool):
    from pyipptool import cups_reject_jobs
    _call_ipptool.return_value = {'Tests': [{'StatusCode': 'successful-ok'}]}
    cups_reject_jobs('https://localhost:631/')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_get_jobs(_call_ipptool):
    from pyipptool import get_jobs
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    get_jobs('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_get_printer_attributes(_call_ipptool):
    from pyipptool import get_printer_attributes
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    get_printer_attributes('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_get_subscriptions(_call_ipptool):
    from pyipptool import get_subscriptions
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    get_subscriptions('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_pause_printer(_call_ipptool):
    from pyipptool import pause_printer
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    pause_printer('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_hold_new_jobs(_call_ipptool):
    from pyipptool import hold_new_jobs
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    hold_new_jobs('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_release_held_new_jobs(_call_ipptool):
    from pyipptool import release_held_new_jobs
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    release_held_new_jobs('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_resume_printer(_call_ipptool):
    from pyipptool import resume_printer
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    resume_printer('https://localhost:631/', printer_uri='')
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'


@mock.patch.object(pyipptool, '_call_ipptool')
def test_cancel_subscription(_call_ipptool):
    from pyipptool import cancel_subscription
    _call_ipptool.return_value = {'Tests': [{'ResponseAttributes': ''}]}
    cancel_subscription('https://localhost:631/',
                        printer_uri='',
                        notify_subscription_id=3)
    assert _call_ipptool._mock_mock_calls[0][1][0] == 'https://localhost:631/'
