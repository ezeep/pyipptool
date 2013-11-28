from pkg_resources import resource_filename

import deform.template

from .schemas import (cancel_job_schema,
                      create_printer_subscription_schema,
                      cups_add_modify_class_schema,
                      cups_add_modify_printer_schema,
                      cups_get_printers_schema,
                      cups_move_job_schema,
                      cups_reject_jobs_schema,
                      get_jobs_schema,
                      get_subscriptions_schema,
                      )

default_dir = resource_filename('pyipptool', 'templates/')
renderer = deform.template.ZPTRendererFactory((default_dir,))

deform.Form.set_default_renderer(renderer)


cancel_job_form = deform.Form(cancel_job_schema)
create_printer_subscription_form = deform.Form(
    create_printer_subscription_schema)
cups_add_modify_printer_form = deform.Form(cups_add_modify_printer_schema)
cups_add_modify_class_form = deform.Form(cups_add_modify_class_schema)
cups_get_printers_form = deform.Form(cups_get_printers_schema)
cups_move_job_form = deform.Form(cups_move_job_schema)
cups_reject_jobs_form = deform.Form(cups_reject_jobs_schema)
get_jobs_form = deform.Form(get_jobs_schema)
get_subscriptions_form = deform.Form(get_subscriptions_schema)
