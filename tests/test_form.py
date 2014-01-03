def test_cancel_job_form():
    from pyipptool.forms import cancel_job_form
    request = cancel_job_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/classes/PIY',
                     'job_id': 8,
                     'job_uri': 'https://localhost:631/jobs/8',
                     'purge_job': True}}})
    assert 'NAME "Cancel Job"' in request
    assert 'OPERATION "Cancel-Job"' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/PIY' in request
    assert 'ATTR integer job-id 8' in request
    assert 'ATTR uri job-uri https://localhost:631/jobs/8' in request
    assert 'ATTR boolean purge-job 1' in request


def test_release_job_form_with_job_id():
    from pyipptool.forms import release_job_form
    request = release_job_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/classes/PIY',
                     'job_id': 7}}})
    assert 'NAME "Release Job"' in request
    assert 'OPERATION "Release-Job"' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/PIY' in request
    assert 'ATTR integer job-id 7' in request


def test_release_job_form_with_job_uri():
    from pyipptool.forms import release_job_form
    request = release_job_form.render(
        {'header': {'operation_attributes':
                    {'job_uri': 'https://localhost:631/jobs/7'}}})
    assert 'NAME "Release Job"' in request
    assert 'OPERATION "Release-Job"' in request
    assert 'ATTR uri job-uri https://localhost:631/jobs/7' in request


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
    m_uri_0 = 'ipp://localhost:631/printers/p0'
    m_uri_1 = 'ipp://localhost:631/classes/c0'
    request = cups_add_modify_class_form.render(
        {'auth_info_required': 'john',
         'member_uris': '%s,%s' % (m_uri_0, m_uri_1),
         'printer_is_accepting_jobs': True,
         'printer_info': 'multiline\ntext',
         'printer_location': 'The Office',
         'printer_more_info': 'http://example.com',
         'printer_op_policy': 'brain',
         'printer_state': 'idle',
         'printer_state_message': 'Ready to print',
         'requesting_user_name_allowed': 'me'})
    assert 'NAME "CUPS Add Modify Class"'
    assert 'OPERATION "CUPS-Add-Modify-Class"' in request
    assert 'GROUP printer-attributes-tag' in request
    assert 'ATTR uri member-uris %s,%s' % (m_uri_0, m_uri_1) in request
    assert 'ATTR keyword auth-info-required john' in request, request
    assert 'ATTR boolean printer-is-accepting-jobs 1' in request, request
    assert 'ATTR text printer-info "multiline\ntext"' in request
    assert 'ATTR text printer-location "The Office"' in request
    assert 'ATTR uri printer-more-info http://example.com' in request
    assert 'ATTR name printer-op-policy brain' in request
    assert 'ATTR enum printer-state idle' in request, request
    assert 'ATTR text printer-state-message "Ready to print"' in request
    assert 'ATTR name requesting-user-name-allowed me' in request


def test_cups_add_modify_printer_form():
    from pyipptool.forms import cups_add_modify_printer_form
    request = cups_add_modify_printer_form.render(
        {'device_uri': 'cups-pdf:/',
         'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/printers/p0'}},
         'auth_info_required': 'john',
         'job_sheets_default': 'none',
         'port_monitor': 'port',
         'ppd_name': 'printer.ppd',
         'printer_is_accepting_jobs': True,
         'printer_info': 'multiline\ntext',
         'printer_location': 'The Office',
         'printer_more_info': 'http://example.com',
         'printer_op_policy': 'pinky',
         'printer_state': 'idle',
         'printer_state_message': 'Ready to print',
         'requesting_user_name_allowed': 'me'})
    assert 'NAME "CUPS Add Modify Printer"'
    assert 'OPERATION "CUPS-Add-Modify-Printer"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'GROUP printer-attributes-tag' in request
    assert 'ATTR uri device-uri cups-pdf:/' in request
    assert 'ATTR keyword auth-info-required john' in request
    assert 'ATTR name job-sheets-default none' in request
    assert 'ATTR name port-monitor port' in request
    assert 'ATTR name ppd-name printer.ppd' in request
    assert 'ATTR boolean printer-is-accepting-jobs 1' in request, request
    assert 'ATTR text printer-info "multiline\ntext"' in request
    assert 'ATTR text printer-location "The Office"' in request
    assert 'ATTR uri printer-more-info http://example.com' in request
    assert 'ATTR name printer-op-policy pinky' in request
    assert 'ATTR enum printer-state idle' in request
    assert 'ATTR text printer-state-message "Ready to print"' in request
    assert 'ATTR name requesting-user-name-allowed me' in request


def test_cups_delete_printer_form():
    from pyipptool.forms import cups_delete_printer_form
    request = cups_delete_printer_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/printers/p0'}}})
    assert 'NAME "CUPS Delete Printer"' in request
    assert 'OPERATION "CUPS-Delete-Printer"' in request
    assert 'GROUP operation-attributes-tag' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request


def test_cups_delete_class_form():
    from pyipptool.forms import cups_delete_class_form
    request = cups_delete_class_form.render(
        {'header': {'operation_attributes':
                    {'printer_uri': 'https://localhost:631/classes/p0'}}})
    assert 'NAME "CUPS Delete Class"' in request
    assert 'OPERATION "CUPS-Delete-Class"' in request
    assert 'GROUP operation-attributes-tag' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/p0' in request


def test_cups_get_classes_form():
    from pyipptool.forms import cups_get_classes_form
    request = cups_get_classes_form.render(
        {'header': {'operation_attributes':
                    {'first_printer_name': 'DA-Printer',
                     'limit': 2,
                     'printer_location': 'The Office',
                     'printer_type': 'network',
                     'printer_type_mask': 'net',
                     'requested_attributes':
                        'name printer-attributes-tag',
                     'requested_user_name': 'john'}}})
    assert 'NAME "CUPS Get Classes"' in request, request
    assert 'OPERATION "CUPS-Get-Classes"' in request, request
    assert 'ATTR name first-printer-name DA-Printer' in request, request
    assert 'ATTR integer limit 2' in request
    assert 'ATTR text printer-location "The Office"' in request, request
    assert 'ATTR enum printer-type network' in request
    assert 'ATTR enum printer-type-mask net' in request
    assert ('ATTR keyword requested-attributes'
            ' name printer-attributes-tag') in request
    assert 'ATTR name requested-user-name john' in request


def test_cups_get_devices_form():
    from pyipptool.forms import cups_get_devices_form
    request = cups_get_devices_form.render(
        {'header': {'operation_attributes':
                    {'device_class': 'fermionic',
                     'exclude_schemes': 'foo',
                     'include_schemes': 'bar',
                     'limit': 3,
                     'requested_attributes': 'all',
                     'timeout': 12}}})
    assert 'NAME "CUPS Get Devices"' in request
    assert 'OPERATION "CUPS-Get-Devices"' in request
    assert 'ATTR keyword device-class fermionic' in request
    assert 'ATTR name exclude-schemes foo' in request
    assert 'ATTR name include-schemes bar' in request
    assert 'ATTR integer limit 3' in request
    assert 'ATTR keyword requested-attributes all' in request
    assert 'ATTR integer timeout 12' in request


def test_cups_get_ppds_form():
    from pyipptool.forms import cups_get_ppds_form
    request = cups_get_ppds_form.render(
        {'header': {'operation_attributes':
                    {'exclude_schemes': 'foo',
                     'include_schemes': 'bar',
                     'limit': 3,
                     'ppd_make': 'Manufaktur',
                     'ppd_make_and_model': 'Manufaktur XYZ',
                     'ppd_model_number': '1234',
                     'ppd_natural_language': 'en',
                     'ppd_product': 'Generic',
                     'ppd_psversion': 'PS3',
                     'ppd_type': 'generic',
                     'requested_attributes': 'all'}}})
    assert 'NAME "CUPS Get PPDs"' in request
    assert 'OPERATION "CUPS-Get-PPDs"' in request
    assert 'ATTR name exclude-schemes foo' in request
    assert 'ATTR name include-schemes bar' in request
    assert 'ATTR text ppd-make "Manufaktur"' in request
    assert 'ATTR text ppd-make-and-model "Manufaktur XYZ"' in request
    assert 'ATTR integer ppd-model-number 1234' in request
    assert 'ATTR naturalLanguage ppd-natural-language en' in request
    assert 'ATTR text ppd-product "Generic"' in request
    assert 'ATTR text ppd-psversion "PS3"' in request
    assert 'ATTR keyword ppd-type generic' in request
    assert 'ATTR keyword requested-attributes all' in request


def test_cups_get_printers_form():
    from pyipptool.forms import cups_get_printers_form
    request = cups_get_printers_form.render(
        {'header': {'operation_attributes':
                    {'first_printer_name': 'DA-Printer',
                     'limit': 2,
                     'printer_location': 'The Office',
                     'printer_type': 'network',
                     'printer_type_mask': 'net',
                     'requested_attributes':
                        'name printer-attributes-tag',
                     'requested_user_name': 'john'}}})
    assert 'NAME "CUPS Get Printers"' in request, request
    assert 'OPERATION "CUPS-Get-Printers"' in request, request
    assert 'ATTR name first-printer-name DA-Printer' in request, request
    assert 'ATTR integer limit 2' in request
    assert 'ATTR text printer-location "The Office"' in request, request
    assert 'ATTR enum printer-type network' in request
    assert 'ATTR enum printer-type-mask net' in request
    assert ('ATTR keyword requested-attributes'
            ' name printer-attributes-tag') in request
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


def test_get_job_attributes_form():
    from pyipptool.forms import get_job_attributes_form
    request = get_job_attributes_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri':
           'https://localhost:631/printers/DA-PRINTER',
           'job_id': 2,
           'requesting_user_name': 'susan',
           'requested_attributes': 'job-uri'}}})
    assert 'NAME "Get Job Attributes"' in request
    assert 'OPERATION "Get-Job-Attributes"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/DA-PRINTER'\
        in request
    assert 'ATTR integer job-id 2' in request
    assert 'ATTR name requesting-user-name susan' in request
    assert 'ATTR keyword requested-attributes job-uri' in request


def test_get_jobs_form():
    from pyipptool.forms import get_jobs_form
    request = get_jobs_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri': 'https://localhost:631/printers/p0',
           'requesting_user_name': 'yoda',
           'limit': 1,
           'requested_attributes':
           'job-uri',
           'which_jobs': 'pending',
           'my_jobs': True}}})
    assert 'NAME "Get Jobs"' in request
    assert 'OPERATION "Get-Jobs"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR integer limit 1' in request
    assert 'ATTR keyword requested-attributes job-uri' in request
    assert 'ATTR keyword which-jobs pending' in request


def test_get_printer_attributes_form():
    from pyipptool.forms import get_printer_attributes_form
    request = get_printer_attributes_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri':
           'https://localhost:631/printers/p0',
           'requesting_user_name': 'yoda',
           'requested_attributes': ('printer-name',
                                    'operations-supported')}}})
    assert 'NAME "Get Printer Attributes"' in request
    assert 'OPERATION "Get-Printer-Attributes"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR keyword requested-attributes'
    ' printer-name,operations-supported' in request


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


def test_pause_printer_form():
    from pyipptool.forms import pause_printer_form
    request = pause_printer_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri': 'ipp://server:port/printers/name',
           'requesting_user_name': 'yoda'}}})
    assert 'NAME "Pause Printer"' in request
    assert 'OPERATION "Pause-Printer"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request


def test_resume_printer_form():
    from pyipptool.forms import resume_printer_form
    request = resume_printer_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri': 'ipp://server:port/printers/name',
           'requesting_user_name': 'yoda'}}})
    assert 'NAME "Resume Printer"' in request
    assert 'OPERATION "Resume-Printer"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request


def test_hold_new_jobs_form():
    from pyipptool.forms import hold_new_jobs_form
    request = hold_new_jobs_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri': 'ipp://server:port/printers/name',
           'requesting_user_name': 'yoda',
           'printer_message_from_operator': 'freeze jobs'}}})
    assert 'NAME "Hold New Jobs"' in request
    assert 'OPERATION "Hold-New-Jobs"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR text printer-message-from-operator "freeze jobs"' in request


def test_release_held_new_jobs_form():
    from pyipptool.forms import release_held_new_jobs_form
    request = release_held_new_jobs_form.render(
        {'header':
         {'operation_attributes':
          {'printer_uri': 'ipp://server:port/printers/name',
           'requesting_user_name': 'yoda',
           'printer_message_from_operator': 'melt jobs'}}})
    assert 'NAME "Release Held New Jobs"' in request
    assert 'OPERATION "Release-Held-New-Jobs"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR text printer-message-from-operator "melt jobs"' in request
