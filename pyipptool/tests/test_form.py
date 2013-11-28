def test_cancel_job_form():
    from pyipptool.forms import cancel_job_form
    request = cancel_job_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/classes/PIY',
                     'purge_job': True}}})
    assert 'NAME "Cancel Job"' in request
    assert 'OPERATION "Cancel-Job"' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/PIY' in request
    assert 'ATTR boolean purge-job 1' in request


def test_create_printer_subscription_form():
    from pyipptool.forms import create_printer_subscription_form
    request = create_printer_subscription_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/classes/PIY',
                     'requesting_user_name': 'ecp_admin'}},
         'notify_recipient_uri': 'ezpnotifier://',
         'notify_events': 'all',
         'notify_lease_duration': 128,
         'notify_lease_expiration_time': 0})
    assert 'NAME "Create Printer Subscription"' in request, request
    assert 'OPERATION "Create-Printer-Subscription"' in request, request
    assert 'ATTR charset attributes-charset utf-8' in request, request
    assert 'ATTR language attributes-natural-language en' in request, request
    assert 'ATTR name requesting-user-name ecp_admin' in request, request
    assert 'GROUP subscription-attributes-tag' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/PIY' in request
    assert 'ATTR uri notify-recipient-uri ezpnotifier://' in request
    assert 'ATTR keyword notify-events all' in request
    assert 'ATTR integer notify-lease-duration 128' in request
    assert 'ATTR integer notify-lease-expiration-time 0' in request


def test_cups_add_modify_class_form():
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
    assert 'ATTR uri device-uri cups-pdf:/' in request
    assert 'ATTR keyword auth-info-required john' in request, request
    assert 'ATTR name job-sheets-default none' in request, request
    assert 'ATTR name port-monitor port' in request
    assert 'ATTR name ppd-name printer.ppd' in request
    assert 'ATTR boolean printer-is-accepting-jobs 1' in request, request
    assert 'ATTR text printer-info "multiline\ntext"' in request
    assert 'ATTR text printer-location "The Office"' in request
    assert 'ATTR uri printer-more-info http://example.com' in request
    assert 'ATTR enum printer-state idle' in request, request
    assert 'ATTR text printer-state-message "Ready to print"' in request
    assert 'ATTR name requesting-user-name-allowed me' in request


def test_cups_add_modify_printer_form():
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
    assert 'ATTR uri device-uri cups-pdf:/' in request
    assert 'ATTR keyword auth-info-required john' in request
    assert 'ATTR name job-sheets-default none' in request
    assert 'ATTR name port-monitor port' in request
    assert 'ATTR name ppd-name printer.ppd' in request
    assert 'ATTR boolean printer-is-accepting-jobs 1' in request, request
    assert 'ATTR text printer-info "multiline\ntext"' in request
    assert 'ATTR text printer-location "The Office"' in request
    assert 'ATTR uri printer-more-info http://example.com' in request
    assert 'ATTR enum printer-state idle' in request
    assert 'ATTR text printer-state-message "Ready to print"' in request
    assert 'ATTR name requesting-user-name-allowed me' in request


def test_cups_get_printers_form():
    from pyipptool.forms import cups_get_printers_form
    request = cups_get_printers_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/',
                     'first_printer_name': 'DA-Printer',
                     'limit': 2,
                     'printer_location': 'The Office',
                     'printer_type': 'network',
                     'printer_type_mask': 'net',
                     'requested_attributes':
                        'name printer-object-attributes-tag',
                     'requested_user_name': 'john'}}})
    assert 'NAME "CUPS Get Printers"' in request, request
    assert 'OPERATION "CUPS-Get-Printers"' in request, request
    assert 'ATTR name first-printer-name DA-Printer' in request, request
    assert 'ATTR integer limit 2' in request
    assert 'ATTR text printer-location "The Office"' in request, request
    assert 'ATTR enum printer-type network' in request
    assert 'ATTR enum printer-type-mask net' in request
    assert ('ATTR keyword requested-attributes'
            ' name printer-object-attributes-tag') in request
    assert 'ATTR name requested-user-name john' in request


def test_cups_reject_jobs_form():
    from pyipptool.forms import cups_reject_jobs_form
    request = cups_reject_jobs_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': ('https://localhost:631/'
                                     'printers/DA-PRINTER'),
                     'requesting_user_name': 'ecp_admin'}},
         'printer_state_message': 'You shall not pass'})
    assert 'NAME "CUPS Reject Jobs"' in request, request
    assert 'OPERATION "CUPS-Reject-Jobs"' in request, request
    assert 'ATTR text printer-state-message "You shall not pass"' in request


def test_get_jobs_form():
    from pyipptool.forms import get_jobs_form
    request = get_jobs_form.render({'header': {'operation_attributes':
                                               {'limit': 1,
                                                'requested_attributes':
                                                'job-uri',
                                                'which_jobs': 'pending',
                                                'my_jobs': True}}})
    assert 'NAME "Get Jobs"' in request
    assert 'OPERATION "Get-Jobs"' in request
    assert 'ATTR integer limit 1' in request
    assert 'ATTR keyword requested-attributes job-uri' in request
    assert 'ATTR keyword which-jobs pending' in request


def test_get_subscriptions_form():
    from pyipptool.forms import get_subscriptions_form
    request = get_subscriptions_form.render({'header':
                                             {'operation_attributes':
                                              {'limit': 1,
                                               'requested_attributes':
                                               'job-uri',
                                               'which_jobs': 'pending',
                                               'my_jobs': True}}})
    assert 'NAME "Get Subscriptions"' in request
    assert 'OPERATION "Get-Subscriptions"' in request
    assert 'ATTR integer limit 1' in request
    assert 'ATTR keyword requested-attributes job-uri' in request
    assert 'ATTR keyword which-jobs pending' in request
    assert 'ATTR boolean my-jobs 1' in request, request
    assert 'ATTR boolean my-jobs 1' in request, request
