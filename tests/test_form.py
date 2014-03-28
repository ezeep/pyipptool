import colander
import mock
import pytest


def test_cancel_job_form():
    from pyipptool.forms import cancel_job_form
    request = cancel_job_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/classes/PIY',
          'job_id': 8,
          'job_uri': 'https://localhost:631/jobs/8',
          'purge_job': True}})
    assert 'NAME "Cancel Job"' in request
    assert 'OPERATION "Cancel-Job"' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/PIY' in request
    assert 'ATTR integer job-id 8' in request
    assert 'ATTR uri job-uri https://localhost:631/jobs/8' in request
    assert 'ATTR boolean purge-job 1' in request


def test_release_job_form_with_job_id():
    from pyipptool.forms import release_job_form
    request = release_job_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/classes/PIY',
          'job_id': 7}})
    assert 'NAME "Release Job"' in request
    assert 'OPERATION "Release-Job"' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/PIY' in request
    assert 'ATTR integer job-id 7' in request


def test_release_job_form_with_job_uri():
    from pyipptool.forms import release_job_form
    request = release_job_form.render(
        {'operation_attributes_tag':
         {'job_uri': 'https://localhost:631/jobs/7'}})
    assert 'NAME "Release Job"' in request
    assert 'OPERATION "Release-Job"' in request
    assert 'ATTR uri job-uri https://localhost:631/jobs/7' in request


def test_create_printer_subscription_form():
    from pyipptool.forms import create_printer_subscription_form
    request = create_printer_subscription_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/classes/PIY',
          'requesting_user_name': 'admin'},
         'subscription_attributes_tag':
         {'notify_recipient_uri': 'rss://',
          'notify_events': 'all',
          'notify_attributes': 'notify-subscriber-user-name',
          'notify_charset': 'utf-8',
          'notify_natural_language': 'de',
          'notify_lease_duration': 128,
          'notify_time_interval': 1}})
    assert 'NAME "Create Printer Subscription"' in request, request
    assert 'OPERATION "Create-Printer-Subscription"' in request, request
    assert 'ATTR charset attributes-charset utf-8' in request, request
    assert 'ATTR language attributes-natural-language en' in request, request
    assert 'ATTR name requesting-user-name admin' in request, request
    assert 'GROUP subscription-attributes-tag' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/PIY' in request
    assert 'ATTR uri notify-recipient-uri rss://' in request
    assert 'ATTR keyword notify-events all' in request
    assert 'ATTR charset notify-charset utf-8' in request
    assert 'ATTR language notify-natural-language de' in request
    assert 'ATTR integer notify-lease-duration 128' in request
    assert 'ATTR integer notify-time-interval 1' in request


def test_create_job_subscription_form_for_pull_delivery_method():
    from pyipptool.forms import create_job_subscription_form
    request = create_job_subscription_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printer/p',
          'requesting_user_name': 'admin'},
         'subscription_attributes_tag':
         {'notify_recipient_uri': 'rss://',
          'notify_job_id': 12,
          'notify_events': ('job-completed', 'job-created', 'job-progress'),
          'notify_attributes': 'notify-subscriber-user-name',
          'notify_charset': 'utf-8',
          'notify_natural_language': 'de',
          'notify_time_interval': 1}})
    assert 'NAME "Create Job Subscription"' in request
    assert 'OPERATION "Create-Job-Subscription"' in request

    assert 'GROUP operation-attributes-tag' in request, request
    assert 'ATTR charset attributes-charset utf-8' in request
    assert 'ATTR language attributes-natural-language en' in request
    assert 'ATTR name requesting-user-name admin' in request

    assert 'GROUP subscription-attributes-tag' in request
    assert 'ATTR uri printer-uri https://localhost:631/printer/p' in request
    assert 'ATTR integer notify-job-id 12' in request, request
    assert 'ATTR uri notify-recipient-uri rss://' in request
    assert ('ATTR keyword notify-events job-completed,job-created,job-progress'
            in request), request
    assert 'ATTR charset notify-charset utf-8' in request
    assert 'ATTR language notify-natural-language de' in request
    assert 'ATTR integer notify-time-interval 1' in request


def test_cups_add_modify_class_form():
    from pyipptool.forms import cups_add_modify_class_form
    m_uri_0 = 'ipp://localhost:631/printers/p0'
    m_uri_1 = 'ipp://localhost:631/classes/c0'
    request = cups_add_modify_class_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printers/p0'},
         'printer_attributes_tag':
         {'auth_info_required': 'john',
          'member_uris': (m_uri_0, m_uri_1),
          'printer_is_accepting_jobs': True,
          'printer_info': 'multiline\ntext',
          'printer_location': 'The Office',
          'printer_more_info': 'http://example.com',
          'printer_op_policy': 'brain',
          'printer_state': '3',
          'printer_state_message': 'Ready to print',
          'requesting_user_name_allowed': 'me',
          'printer_is_shared': False}})
    assert 'NAME "CUPS Add Modify Class"'
    assert 'OPERATION "CUPS-Add-Modify-Class"' in request
    assert 'GROUP operation-attributes-tag' in request, request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request

    assert 'GROUP printer-attributes-tag' in request
    assert 'ATTR uri member-uris %s,%s' % (m_uri_0, m_uri_1) in request
    assert 'ATTR keyword auth-info-required john' in request, request
    assert 'ATTR boolean printer-is-accepting-jobs 1' in request, request
    assert 'ATTR text printer-info "multiline\ntext"' in request
    assert 'ATTR text printer-location "The Office"' in request
    assert 'ATTR uri printer-more-info http://example.com' in request
    assert 'ATTR name printer-op-policy brain' in request
    assert 'ATTR enum printer-state 3' in request, request
    assert 'ATTR text printer-state-message "Ready to print"' in request
    assert 'ATTR name requesting-user-name-allowed me' in request
    assert 'ATTR boolean printer-is-shared 0' in request


def test_cups_add_modify_printer_form():
    from pyipptool.forms import cups_add_modify_printer_form
    request = cups_add_modify_printer_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printers/p0'},
         'printer_attributes_tag':
         {'device_uri': 'cups-pdf:/',
          'auth_info_required': 'john',
          'job_sheets_default': 'none',
          'port_monitor': 'port',
          'ppd_name': 'printer.ppd',
          'printer_is_accepting_jobs': True,
          'printer_info': 'multiline\ntext',
          'printer_location': 'The Office',
          'printer_more_info': 'http://example.com',
          'printer_op_policy': 'pinky',
          'printer_state': '3',
          'printer_state_message': 'Ready to print',
          'requesting_user_name_allowed': 'me',
          'printer_is_shared': True}})
    assert 'NAME "CUPS Add Modify Printer"'
    assert 'OPERATION "CUPS-Add-Modify-Printer"' in request
    assert 'GROUP operation-attributes-tag' in request
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
    assert 'ATTR enum printer-state 3' in request
    assert 'ATTR text printer-state-message "Ready to print"' in request
    assert 'ATTR name requesting-user-name-allowed me' in request
    assert 'ATTR boolean printer-is-shared 1' in request


def test_cups_add_modify_printer_form_with_None():
    from pyipptool.forms import cups_add_modify_printer_form
    with pytest.raises(ValueError) as exec_info:
        cups_add_modify_printer_form.render(
            {'operation_attributes_tag':
             {'printer_uri': 'https://localhost:631/printers/p0'},
             'printer_attributes_tag': {'printer_state_message': None}})
    assert exec_info.value.message == ("None value provided for"
                                       " 'printer_state_message'")


def test_cups_delete_printer_form():
    from pyipptool.forms import cups_delete_printer_form
    request = cups_delete_printer_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printers/p0'}})
    assert 'NAME "CUPS Delete Printer"' in request
    assert 'OPERATION "CUPS-Delete-Printer"' in request
    assert 'GROUP operation-attributes-tag' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request


def test_cups_delete_class_form():
    from pyipptool.forms import cups_delete_class_form
    request = cups_delete_class_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/classes/p0'}})
    assert 'NAME "CUPS Delete Class"' in request
    assert 'OPERATION "CUPS-Delete-Class"' in request
    assert 'GROUP operation-attributes-tag' in request
    assert 'ATTR uri printer-uri https://localhost:631/classes/p0' in request


def test_cups_get_classes_form():
    from pyipptool.forms import cups_get_classes_form
    request = cups_get_classes_form.render(
        {'operation_attributes_tag':
         {'first_printer_name': 'DA-Printer',
          'limit': 2,
          'printer_location': 'The Office',
          'printer_type': '2',
          'printer_type_mask': '8',
          'requested_attributes': ('name', 'printer-attributes-tag'),
          'requested_user_name': 'john'}})
    assert 'NAME "CUPS Get Classes"' in request, request
    assert 'OPERATION "CUPS-Get-Classes"' in request, request
    assert 'ATTR name first-printer-name DA-Printer' in request, request
    assert 'ATTR integer limit 2' in request
    assert 'ATTR text printer-location "The Office"' in request, request
    assert 'ATTR enum printer-type 2' in request
    assert 'ATTR enum printer-type-mask 8' in request
    assert ('ATTR keyword requested-attributes'
            ' name,printer-attributes-tag' in request), request
    assert 'ATTR name requested-user-name john' in request


def test_cups_get_devices_form():
    from pyipptool.forms import cups_get_devices_form
    request = cups_get_devices_form.render(
        {'operation_attributes_tag':
         {'device_class': 'fermionic',
          'exclude_schemes': 'foo',
          'include_schemes': 'bar',
          'limit': 3,
          'requested_attributes': 'all',
          'timeout': 12}})
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
        {'operation_attributes_tag':
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
          'requested_attributes': 'all'}})
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
    assert 'ATTR integer limit 3' in request


def test_cups_get_printers_form():
    from pyipptool.forms import cups_get_printers_form
    request = cups_get_printers_form.render(
        {'operation_attributes_tag':
         {'first_printer_name': 'DA-Printer',
          'limit': 2,
          'printer_location': 'The Office',
          'printer_type': '2',
          'printer_type_mask': '8',
          'requested_attributes': ('name', 'printer-attributes-tag'),
          'requested_user_name': 'john'}})
    assert 'NAME "CUPS Get Printers"' in request, request
    assert 'OPERATION "CUPS-Get-Printers"' in request, request
    assert 'ATTR name first-printer-name DA-Printer' in request, request
    assert 'ATTR integer limit 2' in request
    assert 'ATTR text printer-location "The Office"' in request, request
    assert 'ATTR enum printer-type 2' in request
    assert 'ATTR enum printer-type-mask 8' in request
    assert ('ATTR keyword requested-attributes'
            ' name,printer-attributes-tag' in request), request
    assert 'ATTR name requested-user-name john' in request


def test_cups_reject_jobs_form():
    from pyipptool.forms import cups_reject_jobs_form
    request = cups_reject_jobs_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://cups:631/printers/p',
          'requesting_user_name': 'admin'},
         'printer_attributes_tag':
         {'printer_state_message': 'You shall not pass'}})
    assert 'NAME "CUPS Reject Jobs"' in request, request
    assert 'OPERATION "CUPS-Reject-Jobs"' in request, request

    assert 'GROUP operation-attributes-tag' in request
    assert 'ATTR uri printer-uri ipp://cups:631/printers/p' in request

    assert 'GROUP printer-attributes-tag' in request
    assert 'ATTR text printer-state-message "You shall not pass"' in request


def test_get_job_attributes_form():
    from pyipptool.forms import get_job_attributes_form
    request = get_job_attributes_form.render(
        {'operation_attributes_tag':
         {'printer_uri':
          'https://localhost:631/printers/DA-PRINTER',
          'job_id': 2,
          'requesting_user_name': 'susan',
          'requested_attributes': 'job-uri'}})
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
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printers/p0',
          'requesting_user_name': 'yoda',
          'limit': 1,
          'requested_attributes': 'job-uri',
          'which_jobs': 'pending',
          'my_jobs': True}})
    assert 'NAME "Get Jobs"' in request
    assert 'OPERATION "Get-Jobs"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR integer limit 1' in request
    assert 'ATTR keyword requested-attributes job-uri' in request
    assert 'ATTR keyword which-jobs pending' in request
    assert 'ATTR keyword requested-attributes job-uri' in request


def test_get_printer_attributes_form():
    from pyipptool.forms import get_printer_attributes_form
    request = get_printer_attributes_form.render(
        {'operation_attributes_tag':
         {'printer_uri':
          'https://localhost:631/printers/p0',
          'requesting_user_name': 'yoda',
          'requested_attributes': ('printer-name', 'operations-supported')}})
    assert 'NAME "Get Printer Attributes"' in request
    assert 'OPERATION "Get-Printer-Attributes"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR keyword requested-attributes'\
        ' printer-name,operations-supported' in request


def test_get_subscriptions_form():
    from pyipptool.forms import get_subscriptions_form
    request = get_subscriptions_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printers/p0',
          'requesting_user_name': 'yoda',
          'notify_job_id': 3,
          'limit': 1,
          'requested_attributes': 'notify-recipient-uri',
          'my_subscriptions': True}})
    assert 'NAME "Get Subscriptions"' in request
    assert 'OPERATION "Get-Subscriptions"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR integer notify-job-id 3' in request
    assert 'ATTR integer limit 1' in request
    assert 'ATTR keyword requested-attributes notify-recipient-uri' in request
    assert 'ATTR boolean my-subscriptions 1' in request


def test_get_notifications_form_for_one_notification():
    from pyipptool.forms import get_notifications_form
    request = get_notifications_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printers/p0',
          'requesting_user_name': 'yoda',
          'notify_subscription_ids': 3,
          'notify_sequence_numbers': 1,
          'notify_wait': True}})
    assert 'NAME "Get Notifications"' in request
    assert 'OPERATION "Get-Notifications"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR integer notify-subscription-ids 3' in request
    assert 'ATTR integer notify-sequence-numbers 1' in request
    assert 'ATTR boolean notify-wait 1' in request


def test_get_notifications_form_for_multiple_notifications():
    from pyipptool.forms import get_notifications_form
    request = get_notifications_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'https://localhost:631/printers/p0',
          'requesting_user_name': 'yoda',
          'notify_subscription_ids': (3, 4, 5),
          'notify_sequence_numbers': (2, 9, 29),
          'notify_wait': True}})
    assert 'NAME "Get Notifications"' in request
    assert 'OPERATION "Get-Notifications"' in request
    assert 'ATTR uri printer-uri https://localhost:631/printers/p0' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR integer notify-subscription-ids 3,4,5' in request
    assert 'ATTR integer notify-sequence-numbers 2,9,29' in request
    assert 'ATTR boolean notify-wait 1' in request


def test_pause_printer_form():
    from pyipptool.forms import pause_printer_form
    request = pause_printer_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://server:port/printers/name',
          'requesting_user_name': 'yoda'}})
    assert 'NAME "Pause Printer"' in request
    assert 'OPERATION "Pause-Printer"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request


def test_resume_printer_form():
    from pyipptool.forms import resume_printer_form
    request = resume_printer_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://server:port/printers/name',
          'requesting_user_name': 'yoda'}})
    assert 'NAME "Resume Printer"' in request
    assert 'OPERATION "Resume-Printer"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request


def test_hold_new_jobs_form():
    from pyipptool.forms import hold_new_jobs_form
    request = hold_new_jobs_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://server:port/printers/name',
          'requesting_user_name': 'yoda',
          'printer_message_from_operator': 'freeze jobs'}})
    assert 'NAME "Hold New Jobs"' in request
    assert 'OPERATION "Hold-New-Jobs"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR text printer-message-from-operator "freeze jobs"' in request


def test_release_held_new_jobs_form():
    from pyipptool.forms import release_held_new_jobs_form
    request = release_held_new_jobs_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://server:port/printers/name',
          'requesting_user_name': 'yoda',
          'printer_message_from_operator': 'melt jobs'}})
    assert 'NAME "Release Held New Jobs"' in request
    assert 'OPERATION "Release-Held-New-Jobs"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR text printer-message-from-operator "melt jobs"' in request


def test_cancel_subscription_form():
    from pyipptool.forms import cancel_subscription_form
    request = cancel_subscription_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://server:port/printers/name',
          'requesting_user_name': 'yoda',
          'notify_subscription_id': 5}})
    assert 'NAME "Cancel Subscription"' in request
    assert 'OPERATION "Cancel-Subscription"' in request
    assert 'ATTR uri printer-uri ipp://server:port/printers/name' in request
    assert 'ATTR name requesting-user-name yoda' in request
    assert 'ATTR integer notify-subscription-id 5' in request, request


def test_create_job_form():
    """
    http://www.cups.org/documentation.php/spec-ipp.html#CREATE_JOB
    """
    from pyipptool.forms import create_job_form
    request = create_job_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://server:port/printers/name',
          'job_name': 'foo',
          'ipp_attribute_fidelity': True,
          'job_k_octets': 1024,
          'job_impressions': 2048,
          'job_media_sheets': 2},
         'job_attributes_tag':
         {'job_priority': 1,
          'job_hold_until': 'indefinite',
          'job_sheets': 'standard',
          'media': 'iso-a4-white',
          'auth_info': 'michael',
          'job_billing': 'no-idea',
          'multiple_document_handling': 'single-document',
          'copies': 2,
          'finishings': 'punch',
          'page_ranges': '1-6',
          'sides': 'two-sided-short-edge',
          'number_up': 4,
          'orientation_requested': 'reverse-landscape',
          'printer_resolution': '600dpi',
          'print_quality': 5}})
    assert 'NAME "Create Job"' in request
    assert 'OPERATION "Create-Job"' in request
    assert ('ATTR uri printer-uri ipp://server:port/printers/name' in
            request), request
    assert 'ATTR name job-name foo' in request
    assert 'ATTR boolean ipp-attribute-fidelity 1' in request, request
    assert 'ATTR integer job-k-octets 1024' in request
    assert 'ATTR integer job-impressions 2048' in request
    assert 'ATTR integer job-media-sheets 2' in request
    assert 'ATTR text auth-info "michael"' in request, request
    assert 'ATTR text job-billing "no-idea"' in request, request

    assert 'GROUP job-attributes-tag' in request
    assert 'ATTR integer job-priority 1' in request
    assert 'ATTR keyword job-hold-until indefinite' in request
    assert 'ATTR keyword job-sheets standard' in request
    assert 'ATTR keyword multiple-document-handling single-document' in request
    assert 'ATTR integer copies 2' in request
    assert 'ATTR enum finishings punch' in request
    assert 'ATTR rangeOfInteger page-ranges 1-6' in request
    assert 'ATTR keyword sides two-sided-short-edge' in request
    assert 'ATTR integer number-up 4' in request
    assert 'ATTR enum orientation-requested reverse-landscape' in request
    assert 'ATTR keyword media iso-a4-white' in request
    assert 'ATTR resolution printer-resolution 600dpi' in request
    assert 'ATTR enum print-quality 5' in request


def test_print_job_form():
    from pyipptool.forms import print_job_form
    request = print_job_form.render(
        {'operation_attributes_tag':
         {'printer_uri': 'ipp://server:port/printers/name',
          'job_name': 'foo',
          'ipp_attribute_fidelity': True,
          'document_name': 'foo.txt',
          'compression': 'gzip',
          'document_format': 'text/plain',
          'document_natural_language': 'en',
          'job_k_octets': 1024,
          'job_impressions': 2048,
          'job_media_sheets': 2},
         'job_attributes_tag':
         {'job_priority': 1,
          'job_hold_until': 'indefinite',
          'job_sheets': 'standard',
          'auth_info': 'michael',
          'job_billing': 'no-idea',
          'media': 'media-default',
          'multiple_document_handling': 'single-document',
          'copies': 2,
          'finishings': 'punch',
          'page_ranges': '1-6',
          'sides': 'two-sided-short-edge',
          'number_up': 4,
          'orientation_requested': 'reverse-landscape',
          'printer_resolution': '600dpi',
          'print_quality': 5},
         'subscription_attributes_tag':
         {'notify_recipient_uri': 'rss://',
          'notify_events': ['all']},
         'document_attributes_tag':
         {'file': '/path/to/file.txt'}})

    print request
    assert 'NAME "Print Job"' in request
    assert 'OPERATION "Print-Job"' in request
    assert ('ATTR uri printer-uri ipp://server:port/printers/name' in
            request), request
    assert 'GROUP operation-attributes-tag' in request
    assert 'ATTR name job-name foo' in request
    assert 'ATTR boolean ipp-attribute-fidelity 1' in request, request
    assert 'ATTR name document-name foo.txt' in request
    assert 'ATTR keyword compression gzip' in request
    assert 'ATTR mimeMediaType document-format text/plain' in request
    assert 'ATTR naturalLanguage document-natural-language en' in request
    assert 'ATTR integer job-k-octets 1024' in request
    assert 'ATTR integer job-impressions 2048' in request
    assert 'ATTR integer job-media-sheets 2' in request

    assert 'GROUP job-attributes-tag' in request
    assert 'ATTR integer job-priority 1' in request
    assert 'ATTR keyword job-hold-until indefinite' in request
    assert 'ATTR keyword job-sheets standard' in request
    assert 'ATTR text auth-info "michael"' in request, request
    assert 'ATTR text job-billing "no-idea"' in request, request
    assert 'ATTR keyword job-sheets standard' in request, request
    assert 'ATTR keyword media media-default' in request
    assert 'ATTR keyword multiple-document-handling single-document' in request
    assert 'ATTR integer copies 2' in request
    assert 'ATTR enum finishings punch' in request
    assert 'ATTR rangeOfInteger page-ranges 1-6' in request
    assert 'ATTR keyword sides two-sided-short-edge' in request
    assert 'ATTR integer number-up 4' in request
    assert 'ATTR enum orientation-requested reverse-landscape' in request
    assert 'ATTR resolution printer-resolution 600dpi' in request
    assert 'ATTR enum print-quality 5' in request

    assert 'GROUP subscription-attributes-tag' in request
    assert 'ATTR uri notify-recipient-uri rss://' in request
    assert 'ATTR keyword notify-events all' in request

    assert 'GROUP document-attributes-tag' in request
    assert 'FILE /path/to/file.txt' in request

    assert (request.index('GROUP operation-attributes-tag') <
            request.index('GROUP job-attributes-tag') <
            request.index('GROUP subscription-attributes-tag') <
            request.index('GROUP document-attributes-tag')
            )


def test_send_document_form():
    from pyipptool.forms import send_document_form

    request = send_document_form.render(
        {'operation_attributes_tag':
         {'job_uri': 'http://cups:631/jobs/2',
          'requesting_user_name': 'sweet',
          'document_name': 'python.pdf',
          'compression': 'gzip',
          'document_format': 'application/pdf',
          'document_natural_language': 'en',
          'last_document': True},
         'document_attributes_tag':
         {'file': '/path/to/a/file.pdf'}})
    assert 'NAME "Send Document"' in request
    assert 'OPERATION "Send-Document"' in request

    assert 'GROUP operation-attributes-tag' in request
    assert 'ATTR uri job-uri http://cups:631/jobs/2' in request
    assert 'ATTR name requesting-user-name sweet' in request
    assert 'ATTR name document-name python.pdf' in request
    assert 'ATTR keyword compression gzip' in request
    assert 'ATTR mimeMediaType document-format application/pdf' in request
    assert 'ATTR naturalLanguage document-natural-language en' in request
    assert 'ATTR boolean last-document 1' in request, request

    assert 'GROUP document-attributes-tag'
    assert 'FILE /path/to/a/file.pdf' in request, request


def test_range_of_integer_validator():
    from pyipptool.schemas import range_of_integer_validator
    with pytest.raises(colander.Invalid):
        range_of_integer_validator(mock.MagicMock(), '12-98d')

    with pytest.raises(colander.Invalid):
        range_of_integer_validator(mock.MagicMock(), '-12')

    with pytest.raises(colander.Invalid):
        range_of_integer_validator(mock.MagicMock(), '10-9')

    range_of_integer_validator(mock.MagicMock(), '2-87')
