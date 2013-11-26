import ConfigParser
import os
import plistlib
import subprocess
import tempfile

import colander
from .forms import (create_printer_subscription_form,
                    cups_add_modify_printer_form)


config = ConfigParser.SafeConfigParser()
config.read(['/etc/pyipptool/pyipptool.cfg',
             os.path.join(os.path.expanduser('~'), '.pyipptool.cfg')])
ipptool_path = config.get('main', 'ipptool_path')


def _call_ipptool(printer_uri, request):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(request)
    process = subprocess.Popen([ipptool_path, printer_uri, '-X',
                               temp_file.name],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate()
    finally:
        os.unlink(temp_file.name)
    assert process.returncode == 0, stderr
    return plistlib.readPlistFromString(stdout)


def create_printer_subscription(printer_uri=None,
                                requesting_user_name=None,
                                notify_recipient_uri=None,
                                notify_events=None,
                                notify_lease_duration=colander.null,
                                notify_lease_expiration_time=colander.null):
    kw = dict(header={'required_attributes':
                      {'printer_uri': printer_uri,
                       'requesting_user_name': requesting_user_name}},
              notify_recipient_uri=notify_recipient_uri,
              notify_events=notify_events,
              notify_lease_duration=notify_lease_duration,
              notify_lease_expiration_time=notify_lease_expiration_time)
    request = create_printer_subscription_form.render(kw)
    response = _call_ipptool(printer_uri, request)
    return response['Tests'][0]['notify-subscription-id']


def cups_add_modify_printer_request(printer_uri=None, device_uri=None):
    kw = {'printer_uri': printer_uri, 'device_uri': device_uri}
    request = cups_add_modify_printer_form.render(kw)
    _call_ipptool(printer_uri, request)
    return True
