from .config import get_config
from .core import IPPToolWrapper


config = get_config()

wrapper = IPPToolWrapper(config)
create_job_subscription = wrapper.create_job_subscription
create_printer_subscription = wrapper. create_printer_subscription
cancel_job = wrapper.cancel_job
release_job = wrapper.release_job
create_job = wrapper.create_job
create_printer_subscription = wrapper.create_printer_subscription
cups_add_modify_class = wrapper.cups_add_modify_class
cups_add_modify_printer = wrapper.cups_add_modify_printer
cups_delete_printer = wrapper.cups_delete_printer
cups_delete_class = wrapper.cups_delete_class
cups_get_classes = wrapper.cups_get_classes
cups_get_devices = wrapper.cups_get_devices
cups_get_ppd = wrapper.cups_get_ppd
cups_get_ppds = wrapper.cups_get_ppds
cups_get_printers = wrapper.cups_get_printers
cups_move_job = wrapper.cups_move_job
cups_reject_jobs = wrapper.cups_reject_jobs
get_job_attributes = wrapper.get_job_attributes
get_jobs = wrapper.get_jobs
get_printer_attributes = wrapper.get_printer_attributes
get_subscriptions = wrapper.get_subscriptions
get_notifications = wrapper.get_notifications
pause_printer = wrapper.pause_printer
print_job = wrapper.print_job
resume_printer = wrapper.resume_printer
send_document = wrapper.send_document
hold_new_jobs = wrapper.hold_new_jobs
release_held_new_jobs = wrapper.release_held_new_jobs
cancel_subscription = wrapper.cancel_subscription
