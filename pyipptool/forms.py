from pkg_resources import resource_filename

import deform.template

from .schemas import (cups_add_modify_class_schema,
                      cups_add_modify_printer_schema,
                      create_printer_subscription_schema)


default_dir = resource_filename('pyipptool', 'templates/')
renderer = deform.template.ZPTRendererFactory((default_dir,))

deform.Form.set_default_renderer(renderer)

cups_add_modify_printer_form = deform.Form(cups_add_modify_printer_schema)
cups_add_modify_class_form = deform.Form(cups_add_modify_class_schema)

create_printer_subscription_form = deform.Form(
    create_printer_subscription_schema)
