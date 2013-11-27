def test_cups_add_modify_class_request():
    from pyipptool.forms import cups_add_modify_class_form
    request = cups_add_modify_class_form.render(
        {'device_uri': 'cups-pdf:/',
         'auth_info_required': 'john',
         'job_sheets_default': 'none',
         'port_monitor': 'port',
         'ppd_name': 'printer.ppd',
         'printer_is_accepting_jobs': True,
         'printer_info': 'multiline\ntext',
         'printer_location': 'The Office',
         'printer_more_info': 'http://example.com',
         'printer_state': 'idle',
         'printer_state_message': 'Ready to print',
         'requesting_user_name_allowed': 'me'})
    assert 'NAME "CUPS Add Modify Class"'
    assert 'OPERATION "CUPS-Add-Modify-Class"' in request
    assert 'GROUP printer-object-attributes-tag' in request
    assert 'device-uri cups-pdf:/' in request
    assert 'auth-info-required john' in request
    assert 'job-sheets-default none' in request
    assert 'port-monitor port' in request
    assert 'ppd-name printer.ppd' in request
    assert 'printer-is-accepting-jobs 1' in request, request
    assert 'printer-info "multiline\ntext"' in request
    assert 'printer-location "The Office"' in request
    assert 'printer-more-info http://example.com' in request
    assert 'printer-state idle' in request
    assert 'printer-state-message "Ready to print"' in request
    assert 'requesting-user-name-allowed me' in request


def test_cups_add_modify_printer_request():
    from pyipptool.forms import cups_add_modify_printer_form
    request = cups_add_modify_printer_form.render(
        {'device_uri': 'cups-pdf:/',
         'auth_info_required': 'john',
         'job_sheets_default': 'none',
         'port_monitor': 'port',
         'ppd_name': 'printer.ppd',
         'printer_is_accepting_jobs': True,
         'printer_info': 'multiline\ntext',
         'printer_location': 'The Office',
         'printer_more_info': 'http://example.com',
         'printer_state': 'idle',
         'printer_state_message': 'Ready to print',
         'requesting_user_name_allowed': 'me'})
    assert 'NAME "CUPS Add Modify Printer"'
    assert 'OPERATION "CUPS-Add-Modify-Printer"' in request
    assert 'GROUP printer-object-attributes-tag' in request
    assert 'device-uri cups-pdf:/' in request
    assert 'auth-info-required john' in request
    assert 'job-sheets-default none' in request
    assert 'port-monitor port' in request
    assert 'ppd-name printer.ppd' in request
    assert 'printer-is-accepting-jobs 1' in request, request
    assert 'printer-info "multiline\ntext"' in request
    assert 'printer-location "The Office"' in request
    assert 'printer-more-info http://example.com' in request
    assert 'printer-state idle' in request
    assert 'printer-state-message "Ready to print"' in request
    assert 'requesting-user-name-allowed me' in request


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
    assert 'NAME "Create Printer Subscription"' in request, request
    assert 'OPERATION "Create-Printer-Subscription"' in request, request
    assert 'GROUP subscription-attributes-tag' in request
    assert 'requesting-user-name ecp_admin' in request
    assert 'printer-uri https://localhost:631/classes/PINKY' in request
    assert 'notify-recipient-uri ezpnotifier://' in request
    assert 'notify-events all' in request
    assert 'notify-lease-duration 128' in request
    assert 'notify-lease-expiration-time 0' in request
