def test_cups_add_modify_printer_request():
    from pyipptool.forms import cups_add_modify_printer_form
    request = cups_add_modify_printer_form.render(
        {'device_uri': 'cups-pdf:/'})
    assert 'GROUP printer-object-attributes-tag' in request
    assert 'device-uri cups-pdf:/' in request


def test_create_printer_subscription_request():
    from pyipptool.forms import create_printer_subscription_form
    request = create_printer_subscription_form.render(
        {'header': {'required_attributes':
                    {'printer_uri': 'https://localhost:631/classes/PINKY',
                     'requesting_user_name': 'ecp_admin'}},
         'notify_recipient_uri': 'ezpnotifier://',
         'notify_events': 'all',
         'notify_lease_duration': 128,
         'notify_lease_expiration_time': 0})
    assert 'GROUP subscription-attributes-tag' in request
    assert 'requesting-user-name ecp_admin' in request
    assert 'printer-uri https://localhost:631/classes/PINKY' in request
    assert 'notify-recipient-uri ezpnotifier://' in request
    assert 'notify-events all' in request
    assert 'notify-lease-duration 128' in request
    assert 'notify-lease-expiration-time 0' in request
