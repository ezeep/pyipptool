from pkg_resources import resource_filename

import deform.template

from .schemas import (cancel_job_schema,
                      release_job_schema,
                      create_printer_subscription_schema,
                      cups_add_modify_class_schema,
                      cups_add_modify_printer_schema,
                      cups_delete_printer_schema,
                      cups_delete_class_schema,
                      cups_get_classes_schema,
                      cups_get_devices_schema,
                      cups_get_ppds_schema,
                      cups_get_printers_schema,
                      cups_move_job_schema,
                      cups_reject_jobs_schema,
                      get_job_attributes_schema,
                      get_jobs_schema,
                      get_printer_attributes_schema,
                      get_subscriptions_schema,
                      pause_printer_schema,
                      resume_printer_schema,
                      hold_new_jobs_schema,
                      release_held_new_jobs_schema,
                      cancel_subscription_schema,
                      )

default_dir = resource_filename('pyipptool', 'templates/')
renderer = deform.template.ZPTRendererFactory((default_dir,))

deform.Form.set_default_renderer(renderer)


cancel_job_form = deform.Form(cancel_job_schema)
release_job_form = deform.Form(release_job_schema)
create_printer_subscription_form = deform.Form(
    create_printer_subscription_schema)
cups_add_modify_printer_form = deform.Form(cups_add_modify_printer_schema)
cups_delete_printer_form = deform.Form(cups_delete_printer_schema)
cups_delete_class_form = deform.Form(cups_delete_class_schema)
cups_add_modify_class_form = deform.Form(cups_add_modify_class_schema)
cups_get_classes_form = deform.Form(cups_get_classes_schema)
cups_get_devices_form = deform.Form(cups_get_devices_schema)
cups_get_ppds_form = deform.Form(cups_get_ppds_schema)
cups_get_printers_form = deform.Form(cups_get_printers_schema)
cups_move_job_form = deform.Form(cups_move_job_schema)
cups_reject_jobs_form = deform.Form(cups_reject_jobs_schema)
get_job_attributes_form = deform.Form(get_job_attributes_schema)
get_jobs_form = deform.Form(get_jobs_schema)
get_printer_attributes_form = deform.Form(get_printer_attributes_schema)
get_subscriptions_form = deform.Form(get_subscriptions_schema)
pause_printer_form = deform.Form(pause_printer_schema)
resume_printer_form = deform.Form(resume_printer_schema)
hold_new_jobs_form = deform.Form(hold_new_jobs_schema)
release_held_new_jobs_form = deform.Form(release_held_new_jobs_schema)
cancel_subscription_form = deform.Form(cancel_subscription_schema)
