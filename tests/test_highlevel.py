import BaseHTTPServer
import os.path
import SocketServer
import socket
import tempfile
import textwrap
import threading
import time

import mock
import pytest

import pyipptool


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_ipptool_create_job_subscription_pull_delivery_method(_call_ipptool):
    from pyipptool import create_job_subscription
    create_job_subscription(
        printer_uri='https://localhost:631/printer/p',
        requesting_user_name='admin',
        notify_job_id=108,
        notify_recipient_uri='rss://',
        notify_events=('job-completed', 'job-created', 'job-progress'),
        notify_attributes='notify-subscriber-user-name',
        notify_charset='utf-8',
        notify_natural_language='de',
        notify_time_interval=1)
    request = _call_ipptool._mock_mock_calls[0][1][-1]
    expected_request = textwrap.dedent("""
    {
    NAME "Create Job Subscription"
    OPERATION "Create-Job-Subscription"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri https://localhost:631/printer/p
    ATTR name requesting-user-name admin
    GROUP subscription-attributes-tag
    ATTR uri notify-recipient-uri rss://
    ATTR keyword notify-events job-completed,job-created,job-progress
    ATTR integer notify-job-id 108
    ATTR keyword notify-attributes notify-subscriber-user-name
    ATTR charset notify-charset utf-8
    ATTR language notify-natural-language de
    ATTR integer notify-time-interval 1
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_ipptool_create_printer_subscription(_call_ipptool):
    from pyipptool import create_printer_subscription
    create_printer_subscription(
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        requesting_user_name='admin',
        notify_recipient_uri='rss://',
        notify_events='all',
        notify_attributes='notify-subscriber-user-name',
        notify_charset='utf-8',
        notify_natural_language='de',
        notify_lease_duration=0,
        notify_time_interval=1)
    request = _call_ipptool._mock_mock_calls[0][1][-1]
    expected_request = textwrap.dedent("""
    {
    NAME "Create Printer Subscription"
    OPERATION "Create-Printer-Subscription"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri https://localhost:631/classes/PUBLIC-PDF
    ATTR name requesting-user-name admin
    GROUP subscription-attributes-tag
    ATTR uri notify-recipient-uri rss://
    ATTR keyword notify-events all
    ATTR keyword notify-attributes notify-subscriber-user-name
    ATTR charset notify-charset utf-8
    ATTR language notify-natural-language de
    ATTR integer notify-time-interval 1
    ATTR integer notify-lease-duration 0
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_add_modify_printer(_call_ipptool):
    from pyipptool import cups_add_modify_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_add_modify_printer(
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        device_uri='cups-pdf:/',
        printer_is_shared=False,
    )
    request = _call_ipptool._mock_mock_calls[0][1][-1]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Add Modify Printer"
    OPERATION "CUPS-Add-Modify-Printer"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri https://localhost:631/classes/PUBLIC-PDF
    GROUP printer-attributes-tag
    ATTR boolean printer-is-shared 0
    ATTR uri device-uri cups-pdf:/
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_job_attributes_with_job_id(_call_ipptool):
    from pyipptool import get_job_attributes
    get_job_attributes(
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        job_id=2)
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Get Job Attributes"
    OPERATION "Get-Job-Attributes"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri https://localhost:631/classes/PUBLIC-PDF
    ATTR integer job-id 2
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_job_attributes_with_job_uri(_call_ipptool):
    from pyipptool import get_job_attributes
    get_job_attributes(
        job_uri='https://localhost:631/jobs/2')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Get Job Attributes"
    OPERATION "Get-Job-Attributes"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri job-uri https://localhost:631/jobs/2
    }""").strip()
    assert request == expected_request, request


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
    wrapper.config['cups_uri'] = 'http://localhost:%s/' % PORT
    try:
        with pytest.raises(TimeoutError):
            wrapper._call_ipptool(request)
    finally:
        wrapper.config['timeout'] = old_timeout


def test_authentication():
    from pyipptool import IPPToolWrapper
    wrapper = IPPToolWrapper({'login': 'ezeep',
                              'password': 'secret',
                              'cups_uri': 'http://localhost:631/'
                                          'printers/?arg=value'})

    assert (wrapper.authenticated_uri == 'http://ezeep:secret@localhost:631/'
                                         'printers/?arg=value')


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_release_job(_call_ipptool):
    from pyipptool import release_job
    _call_ipptool.return_value = {'Tests': [{}]}
    release_job(job_uri='ipp://cups:631/jobs/3')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Release Job"
    OPERATION "Release-Job"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri job-uri ipp://cups:631/jobs/3
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cancel_job(_call_ipptool):
    from pyipptool import cancel_job
    _call_ipptool.return_value = {'Tests': [{}]}
    cancel_job(job_uri='ipp://cups:631/jobs/12')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Cancel Job"
    OPERATION "Cancel-Job"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri job-uri ipp://cups:631/jobs/12
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_add_modify_class(_call_ipptool):
    from pyipptool import cups_add_modify_class
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_add_modify_class(printer_uri='ipp://cups:631/classes/p',
                          printer_is_shared=True)
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Add Modify Class"
    OPERATION "CUPS-Add-Modify-Class"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/classes/p
    GROUP printer-attributes-tag
    ATTR boolean printer-is-shared 1
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_delete_printer(_call_ipptool):
    from pyipptool import cups_delete_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_delete_printer(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Delete Printer"
    OPERATION "CUPS-Delete-Printer"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_delete_class(_call_ipptool):
    from pyipptool import cups_delete_class
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_delete_class(printer_uri='ipp://cups:631/classes/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Delete Class"
    OPERATION "CUPS-Delete-Class"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/classes/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_classes(_call_ipptool):
    from pyipptool import cups_get_classes
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_classes()
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Get Classes"
    OPERATION "CUPS-Get-Classes"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_printers(_call_ipptool):
    from pyipptool import cups_get_printers
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_printers()
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Get Printers"
    OPERATION "CUPS-Get-Printers"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_devices(_call_ipptool):
    from pyipptool import cups_get_devices
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_devices()
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Get Devices"
    OPERATION "CUPS-Get-Devices"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_get_ppds(_call_ipptool):
    from pyipptool import cups_get_ppds
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_get_ppds()
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Get PPDs"
    OPERATION "CUPS-Get-PPDs"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_move_job(_call_ipptool):
    from pyipptool import cups_move_job
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_move_job(job_uri='ipp://cups:631/jobs/12',
                  job_printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Move Job"
    OPERATION "CUPS-Move-Job"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri job-uri ipp://cups:631/jobs/12
    GROUP job-attributes-tag
    ATTR uri job-printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cups_reject_jobs(_call_ipptool):
    from pyipptool import cups_reject_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    cups_reject_jobs(printer_uri='ipp://cups:631/printers/p',
                     requesting_user_name='boby')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "CUPS Reject Jobs"
    OPERATION "CUPS-Reject-Jobs"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    ATTR name requesting-user-name boby
    GROUP printer-attributes-tag
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_jobs(_call_ipptool):
    from pyipptool import get_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    get_jobs(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Get Jobs"
    OPERATION "Get-Jobs"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_printer_attributes(_call_ipptool):
    from pyipptool import get_printer_attributes
    _call_ipptool.return_value = {'Tests': [{}]}
    get_printer_attributes(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Get Printer Attributes"
    OPERATION "Get-Printer-Attributes"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_subscriptions(_call_ipptool):
    from pyipptool import get_subscriptions
    _call_ipptool.return_value = {'Tests': [{}]}
    get_subscriptions(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Get Subscriptions"
    OPERATION "Get-Subscriptions"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_get_notifications(_call_ipptool):
    from pyipptool import get_notifications
    _call_ipptool.return_value = {'Tests': [{}]}
    get_notifications(printer_uri='ipp://cups:631/printers/p',
                      notify_subscription_ids=3)
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Get Notifications"
    OPERATION "Get-Notifications"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    ATTR integer notify-subscription-ids 3
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_pause_printer(_call_ipptool):
    from pyipptool import pause_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    pause_printer(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Pause Printer"
    OPERATION "Pause-Printer"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_hold_new_jobs(_call_ipptool):
    from pyipptool import hold_new_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    hold_new_jobs(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Hold New Jobs"
    OPERATION "Hold-New-Jobs"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_release_held_new_jobs(_call_ipptool):
    from pyipptool import release_held_new_jobs
    _call_ipptool.return_value = {'Tests': [{}]}
    release_held_new_jobs(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Release Held New Jobs"
    OPERATION "Release-Held-New-Jobs"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_resume_printer(_call_ipptool):
    from pyipptool import resume_printer
    _call_ipptool.return_value = {'Tests': [{}]}
    resume_printer(printer_uri='ipp://cups:631/printers/p')
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Resume Printer"
    OPERATION "Resume-Printer"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_cancel_subscription(_call_ipptool):
    from pyipptool import cancel_subscription
    _call_ipptool.return_value = {'Tests': [{}]}
    cancel_subscription(printer_uri='ipp://cups:631/printers/p',
                        notify_subscription_id=3)
    request = _call_ipptool._mock_mock_calls[0][1][0]
    expected_request = textwrap.dedent("""
    {
    NAME "Cancel Subscription"
    OPERATION "Cancel-Subscription"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/printers/p
    ATTR integer notify-subscription-id 3
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_create_job(_call_ipptool):
    from pyipptool import create_job
    _call_ipptool.return_value = {'Tests': [{}]}
    create_job(printer_uri='ipp://cups:631/classes/p',
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
               auth_info='michael',
               job_billing='no-idea',
               )
    request = _call_ipptool._mock_mock_calls[0][1][-1]
    expected_request = textwrap.dedent("""
    {
    NAME "Create Job"
    OPERATION "Create-Job"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/classes/p
    ATTR name job-name foo
    ATTR boolean ipp-attribute-fidelity 0
    ATTR integer job-k-octets 1024
    ATTR integer job-impressions 2048
    ATTR integer job-media-sheets 2
    GROUP job-attributes-tag
    ATTR integer job-priority 1
    ATTR keyword job-hold-until indefinite
    ATTR keyword job-sheets standard
    ATTR text auth-info "michael"
    ATTR text job-billing "no-idea"
    ATTR keyword multiple-document-handling single-document
    ATTR integer copies 2
    ATTR enum finishings punch
    ATTR rangeOfInteger page-ranges 1-6
    ATTR keyword sides two-sided-short-edge
    ATTR integer number-up 4
    ATTR enum orientation-requested reverse-landscape
    ATTR keyword media iso-a4-white
    ATTR resolution printer-resolution 600dpi
    ATTR enum print-quality 5
    }""").strip()
    assert request == expected_request, request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_print_job(_call_ipptool):
    from pyipptool import print_job
    _call_ipptool.return_value = {'Tests': [{}]}
    filename = os.path.join(os.path.dirname(__file__),  'hello.pdf')
    with open(filename, 'rb') as tmp:
        print_job(printer_uri='ipp://cups:631/classes/p',
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
                  auth_info='michael',
                  job_billing='no-idea',
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
                  document_content=tmp.read(),
                  ezeep_job_uuid='bla')
    request = _call_ipptool._mock_mock_calls[0][1][-1]
    expected_request = textwrap.dedent("""
    {
    NAME "Print Job"
    OPERATION "Print-Job"
    GROUP operation-attributes-tag
    ATTR charset attributes-charset utf-8
    ATTR language attributes-natural-language en
    ATTR uri printer-uri ipp://cups:631/classes/p
    ATTR name job-name foo
    ATTR boolean ipp-attribute-fidelity 0
    ATTR integer job-k-octets 1024
    ATTR integer job-impressions 2048
    ATTR integer job-media-sheets 2
    ATTR name document-name foo.txt
    ATTR keyword compression gzip
    ATTR mimeMediaType document-format text/plain
    ATTR naturalLanguage document-natural-language en
    GROUP job-attributes-tag
    ATTR integer job-priority 1
    ATTR keyword job-hold-until indefinite
    ATTR keyword job-sheets standard
    ATTR text auth-info "michael"
    ATTR text job-billing "no-idea"
    ATTR keyword multiple-document-handling single-document
    ATTR integer copies 2
    ATTR enum finishings punch
    ATTR rangeOfInteger page-ranges 1-6
    ATTR keyword sides two-sided-short-edge
    ATTR integer number-up 4
    ATTR enum orientation-requested reverse-landscape
    ATTR keyword media iso-a4-white
    ATTR resolution printer-resolution 600dpi
    ATTR enum print-quality 5
    ATTR text ezeep-job-uuid "bla"
    GROUP subscription-attributes-tag
    GROUP document-attributes-tag
    FILE /tmp/
    }""").strip()
    assert ('\n'.join(request.splitlines()[:-2])
            == '\n'.join(expected_request.splitlines()[:-2])), request
    assert expected_request.splitlines()[-2].startswith('FILE /tmp/')


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_send_document_with_file(_call_ipptool):
    from pyipptool import send_document
    _call_ipptool.return_value = {'Tests': [{}]}

    with tempfile.NamedTemporaryFile('rb') as tmp:
        send_document(printer_uri='ipp://cups:631/printers/p',
                      requesting_user_name='you',
                      document_content=tmp)
        request = _call_ipptool._mock_mock_calls[0][1][-1]
        expected_request = textwrap.dedent("""
        {
        NAME "Send Document"
        OPERATION "Send-Document"
        GROUP operation-attributes-tag
        ATTR charset attributes-charset utf-8
        ATTR language attributes-natural-language en
        ATTR uri printer-uri ipp://cups:631/printers/p
        ATTR name requesting-user-name you
        ATTR mimeMediaType document-format application/pdf
        ATTR boolean last-document 1
        GROUP document-attributes-tag
        FILE %s
        }""" % tmp.name).strip()
        assert request == expected_request


@mock.patch.object(pyipptool.wrapper, '_call_ipptool')
def test_send_document_with_binary(_call_ipptool):
    from pyipptool import send_document
    _call_ipptool.return_value = {'Tests': [{}]}

    with open(os.path.join(os.path.dirname(__file__),
                           'hello.pdf'), 'rb') as tmp:
        send_document(document_content=tmp.read())
    assert 'FILE /tmp/' in _call_ipptool._mock_mock_calls[0][1][-1]
