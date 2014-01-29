import ConfigParser
import os

from .core import IPPToolWrapper


def read_config(paths=('/etc/opt/pyipptool/pyipptool.cfg',
                       os.path.join(os.path.expanduser('~'),
                                    '.pyipptool.cfg'))):
    config = {}
    fs_config = ConfigParser.ConfigParser()
    fs_config.read(paths)
    config['ipptool_path'] = fs_config.get('main', 'ipptool_path')
    try:
        config['login'] = fs_config.get('main', 'login')
    except ConfigParser.NoOptionError:
        pass
    try:
        config['password'] = fs_config.get('main', 'password')
    except ConfigParser.NoOptionError:
        pass
    try:
        config['graceful_shutdown_time'] = fs_config.getint(
            'main',
            'graceful_shutdown_time')
    except ConfigParser.NoOptionError:
        config['graceful_shutdown_time'] = 2
    try:
        config['timeout'] = fs_config.getint('main', 'timeout')
    except ConfigParser.NoOptionError:
        config['timeout'] = 10
    return config


config = read_config()

wrapper = IPPToolWrapper(config)
create_printer_subscription = wrapper. create_printer_subscription
cancel_job = wrapper.cancel_job
release_job = wrapper.release_job
create_printer_subscription = wrapper.create_printer_subscription
cups_add_modify_class = wrapper.cups_add_modify_class
cups_add_modify_printer = wrapper.cups_add_modify_printer
cups_delete_printer = wrapper.cups_delete_printer
cups_delete_class = wrapper.cups_delete_class
cups_get_classes = wrapper.cups_get_classes
cups_get_devices = wrapper.cups_get_devices
cups_get_ppds = wrapper.cups_get_ppds
cups_get_printers = wrapper.cups_get_printers
cups_move_job = wrapper.cups_move_job
cups_reject_jobs = wrapper.cups_reject_jobs
get_job_attributes = wrapper.get_job_attributes
get_jobs = wrapper.get_jobs
get_printer_attributes = wrapper.get_printer_attributes
get_subscriptions = wrapper.get_subscriptions
pause_printer = wrapper.pause_printer
resume_printer = wrapper.resume_printer
hold_new_jobs = wrapper.hold_new_jobs
release_held_new_jobs = wrapper.release_held_new_jobs
cancel_subscription = wrapper.cancel_subscription
