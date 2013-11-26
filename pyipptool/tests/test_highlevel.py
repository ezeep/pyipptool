import mock

import pyipptool


@mock.patch.object(pyipptool, '_call_ipptool')
def test_ipptool_create_printer_subscription(_call_ipptool):
    from pyipptool import create_printer_subscription
    create_printer_subscription(
        printer_uri='https://localhost:631/classes/PUBLIC-PDF',
        requesting_user_name='ecp_admin',
        notify_recipient_uri='ezpnotifier://',
        notify_events='all',
        notify_lease_duration=0,
        notify_lease_expiration_time=0)
    assert _call_ipptool._mock_mock_calls[0][1][0] == ('https://localhost:631/'
                                                       'classes/PUBLIC-PDF')
    request = _call_ipptool._mock_mock_calls[0][1][1]
    assert 'requesting-user-name ecp_admin' in request
    assert 'printer-uri https://localhost:631/classes/PUBLIC-PDF' in request
    assert 'notify-recipient-uri ezpnotifier://' in request
    assert 'notify-events all' in request
    assert 'notify-lease-duration 0' in request
    assert 'notify-lease-expiration-time 0' in request
