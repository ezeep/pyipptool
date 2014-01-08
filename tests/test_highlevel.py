import BaseHTTPServer
import SocketServer
import functools
import threading
import time

import mock
import pytest

import pyipptool


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


def patch_timeout(value):
    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kw):
            import pyipptool
            previous = pyipptool.TIMEOUT
            pyipptool.TIMEOUT = value
            try:
                return fn(*args, **kw)
            finally:
                pyipptool.TIMEOUT = previous
        return inner
    return wrapper


@patch_timeout(1)
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
    # time.sleep(.1)  # Warmup

    request = get_subscriptions_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri':
           'http://localhost:%s/printers/fake' % PORT}}})
    with pytest.raises(TimeoutError):
        _call_ipptool('http://localhost:%s/' % PORT, request)
