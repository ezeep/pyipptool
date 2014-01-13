import colander
from .widgets import (IPPAttributeWidget, IPPBodyWidget, IPPDisplayWidget,
                      IPPGroupWidget, IPPNameWidget, IPPTupleWidget,
                      IPPConstantTupleWidget)


class Charset(colander.String):
    pass


class Enum(colander.String):
    pass


class Keyword(colander.String):
    pass


class Language(colander.String):
    pass


class Name(colander.String):
    pass


class NaturalLanguage(colander.String):
    pass


class Text(colander.String):
    def serialize(self, node, appstruct):
        value = super(Text, self).serialize(node, appstruct)
        if value is colander.null:
            return colander.null
        return '"{}"'.format(value)


class Uri(colander.String):
    pass


class OperationAttributes(colander.Schema):
    attributes_charset = colander.SchemaNode(Charset(),
                                             default='utf-8',
                                             widget=IPPAttributeWidget())
    attributes_natural_language = colander.SchemaNode(
        Language(),
        default='en',
        widget=IPPAttributeWidget())


class OperationAttributesWithPrinterUri(OperationAttributes):
    printer_uri = colander.SchemaNode(Uri(),
                                      widget=IPPAttributeWidget())


class OperationAttributesWithJobUri(OperationAttributes):
    job_uri = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())


class JobOperationAttributes(OperationAttributesWithPrinterUri,
                             OperationAttributesWithJobUri):
    job_id = colander.SchemaNode(colander.Integer(),
                                 widget=IPPAttributeWidget())


class GetDevicesOperationAttributes(OperationAttributes):
    exclude_schemes = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    include_schemes = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    limit = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())


class CancelJobOperationAttributes(JobOperationAttributes):
    purge_job = colander.SchemaNode(colander.Boolean(true_val=1, false_val=0),
                                    widget=IPPAttributeWidget())


class SubscriptionOperationAttributes(OperationAttributesWithPrinterUri):
    requesting_user_name = colander.SchemaNode(Name(),
                                               widget=IPPAttributeWidget())


class CancelSubscriptionOperationAttributes(SubscriptionOperationAttributes):
    notify_subscription_id = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())


class HoldNewJobsOperationAttributes(SubscriptionOperationAttributes):
    printer_message_from_operator = colander.SchemaNode(
        Text(), widget=IPPAttributeWidget())


class GetJobsOperationAttributes(SubscriptionOperationAttributes):
    limit = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())
    which_jobs = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    my_jobs = colander.SchemaNode(colander.Boolean(true_val=1, false_val=0),
                                  widget=IPPAttributeWidget())


class MoveJobOperationAttributes(OperationAttributesWithPrinterUri):
    job_id = colander.SchemaNode(colander.Integer(),
                                 widget=IPPAttributeWidget())
    job_uri = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())


class GetSubscriptionsAttributes(OperationAttributesWithPrinterUri):
    requesting_user_name = colander.SchemaNode(
        Name(),
        widget=IPPAttributeWidget())
    notify_job_id = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    limit = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())
    my_subscriptions = colander.SchemaNode(
        colander.Boolean(false_val=0, true_val=1),
        widget=IPPAttributeWidget())


class CupsGetPPDsSchemaOperationAttributes(GetDevicesOperationAttributes):
    ppd_make = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    ppd_make_and_model = colander.SchemaNode(
        Text(),
        widget=IPPAttributeWidget())
    ppd_model_number = colander.SchemaNode(colander.Integer(),
                                           widget=IPPAttributeWidget())
    ppd_natural_language = colander.SchemaNode(NaturalLanguage(),
                                               widget=IPPAttributeWidget())
    ppd_product = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    ppd_psversion = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    ppd_type = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())


class CupsGetDevicesSchemaOperationAttributes(GetDevicesOperationAttributes):
    device_class = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    timeout = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())


class CupsGetPrintersSchemaOperationAttributes(OperationAttributes):
    first_printer_name = colander.SchemaNode(
        Name(),
        widget=IPPAttributeWidget())
    limit = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    printer_location = colander.SchemaNode(
        Text(),
        widget=IPPAttributeWidget())
    printer_type = colander.SchemaNode(Enum(), widget=IPPAttributeWidget())
    printer_type_mask = colander.SchemaNode(
        Enum(),
        widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())
    requested_user_name = colander.SchemaNode(Name(),
                                              widget=IPPAttributeWidget())


class GetJobAttributesOperationAttributes(MoveJobOperationAttributes):
    requesting_user_name = colander.SchemaNode(Name(),
                                               widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())


class GetPrinterAttributesOperationAttributes(
        OperationAttributesWithPrinterUri):
    requesting_user_name = colander.SchemaNode(Name(),
                                               widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())


class HeaderIPPSchema(colander.Schema):
    name = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation_attributes_tag = colander.SchemaNode(colander.String(),
                                                   widget=IPPGroupWidget())
    operation_attributes = OperationAttributes(widget=IPPTupleWidget())
    object_attributes_tag = colander.SchemaNode(
        colander.String(),
        widget=IPPGroupWidget())


class BaseIPPSchema(colander.Schema):
    operation_attributes_tag = 'operation-attributes-tag'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())


class CancelJobSchema(BaseIPPSchema):
    name = 'Cancel Job'
    operation = 'Cancel-Job'
    object_attributes_tag = colander.null
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = CancelJobOperationAttributes(
        widget=IPPTupleWidget())


class ReleaseJobSchema(BaseIPPSchema):
    name = 'Release Job'
    operation = 'Release-Job'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = JobOperationAttributes(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


class BaseCupsAddModifyIPPSchema(BaseIPPSchema):
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = OperationAttributesWithPrinterUri(
        widget=IPPTupleWidget())

    object_attributes_tag = 'printer-attributes-tag'
    auth_info_required = colander.SchemaNode(Keyword(),
                                             widget=IPPAttributeWidget())

    printer_is_accepting_jobs = colander.SchemaNode(
        colander.Boolean(false_val=0, true_val=1),
        widget=IPPAttributeWidget())
    printer_info = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    printer_location = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    printer_more_info = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())
    printer_op_policy = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    printer_state = colander.SchemaNode(Enum(), widget=IPPAttributeWidget())
    printer_state_message = colander.SchemaNode(
        Text(),
        widget=IPPAttributeWidget())
    requesting_user_name_allowed = colander.SchemaNode(
        Name(),
        widget=IPPAttributeWidget())
    requesting_user_name_denied = colander.SchemaNode(
        Name(),
        widget=IPPAttributeWidget())


class CupsAddModifyPrinterSchema(BaseCupsAddModifyIPPSchema):
    name = 'CUPS Add Modify Printer'
    operation = 'CUPS-Add-Modify-Printer'

    job_sheets_default = colander.SchemaNode(Name(),
                                             widget=IPPAttributeWidget())
    device_uri = colander.SchemaNode(Uri(),
                                     widget=IPPAttributeWidget())
    port_monitor = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    ppd_name = colander.SchemaNode(Name(), widget=IPPAttributeWidget())


class CupsDeletePrinterSchema(BaseIPPSchema):
    name = 'CUPS Delete Printer'
    operation = 'CUPS-Delete-Printer'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = OperationAttributesWithPrinterUri(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


class CupsAddModifyClassSchema(BaseCupsAddModifyIPPSchema):
    name = 'CUPS Add Modify Class'
    operation = 'CUPS-Add-Modify-Class'
    member_uris = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())


class CupsDeleteClassSchema(CupsDeletePrinterSchema):
    name = 'CUPS Delete Class'
    operation = 'CUPS-Delete-Class'


class CupsGetClassesSchema(BaseIPPSchema):
    name = 'CUPS Get Classes'
    operation = 'CUPS-Get-Classes'
    object_attributes_tag = colander.null
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = CupsGetPrintersSchemaOperationAttributes(
        widget=IPPTupleWidget())


class CupsGetDevicesSchema(BaseIPPSchema):
    name = 'CUPS Get Devices'
    operation = 'CUPS-Get-Devices'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = CupsGetDevicesSchemaOperationAttributes(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


class CupsGetPPDsSchema(BaseIPPSchema):
    name = 'CUPS Get PPDs'
    operation = 'CUPS-Get-PPDs'
    object_attributes_tag = colander.null
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = CupsGetPPDsSchemaOperationAttributes(
        widget=IPPTupleWidget())


class CupsGetPrintersSchema(CupsGetClassesSchema):
    name = 'CUPS Get Printers'
    operation = 'CUPS-Get-Printers'


class CupsMoveJobSchema(BaseIPPSchema):
    name = 'CUPS Move Job'
    operation = 'CUPS-Move-Job'
    object_attributes_tag = 'job-attributes-tag'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = MoveJobOperationAttributes(
        widget=IPPTupleWidget())
    job_printer_uri = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())


class CupsRejectJobsSchema(BaseIPPSchema):
    name = 'CUPS Reject Jobs'
    operation = 'CUPS-Reject-Jobs'
    object_attributes_tag = 'printer-attributes-tag'
    printer_state_message = colander.SchemaNode(
        Text(),
        widget=IPPAttributeWidget())


class CreatePrinterSubscriptionSchema(BaseIPPSchema):
    name = 'Create Printer Subscription'
    operation = 'Create-Printer-Subscription'
    object_attributes_tag = 'subscription-attributes-tag'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = SubscriptionOperationAttributes(
        widget=IPPTupleWidget())
    notify_recipient_uri = colander.SchemaNode(Uri(),
                                               widget=IPPAttributeWidget())
    notify_events = colander.SchemaNode(Keyword(),
                                        widget=IPPAttributeWidget())
    notify_lease_duration = colander.SchemaNode(colander.Integer(),
                                                widget=IPPAttributeWidget())
    notify_lease_expiration_time = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    notify_subscription_id = colander.SchemaNode(colander.String(),
                                                 widget=IPPDisplayWidget())


class GetJobAttributesSchema(BaseIPPSchema):
    name = 'Get Job Attributes'
    operation = 'Get-Job-Attributes'
    object_attributes_tag = colander.null
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = GetJobAttributesOperationAttributes(
        widget=IPPTupleWidget())


class GetJobsSchema(BaseIPPSchema):
    name = 'Get Jobs'
    operation = 'Get-Jobs'
    object_attributes_tag = colander.null
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = GetJobsOperationAttributes(
        widget=IPPTupleWidget())


class GetPrinterAttributesSchema(BaseIPPSchema):
    name = 'Get Printer Attributes'
    operation = 'Get-Printer-Attributes'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = GetPrinterAttributesOperationAttributes(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


class GetSubscriptionsSchema(BaseIPPSchema):
    name = 'Get Subscriptions'
    operation = 'Get-Subscriptions'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = GetSubscriptionsAttributes(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


class PausePrinterSchema(BaseIPPSchema):
    name = 'Pause Printer'
    operation = 'Pause-Printer'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = SubscriptionOperationAttributes(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


class ResumePrinterSchema(PausePrinterSchema):
    name = 'Resume Printer'
    operation = 'Resume-Printer'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = SubscriptionOperationAttributes(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


class HoldNewJobsSchema(PausePrinterSchema):
    name = 'Hold New Jobs'
    operation = 'Hold-New-Jobs'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = HoldNewJobsOperationAttributes(
        widget=IPPTupleWidget())


class ReleaseHeldNewJobsSchema(HoldNewJobsSchema):
    name = 'Release Held New Jobs'
    operation = 'Release-Held-New-Jobs'


class CancelSubscriptionSchema(BaseIPPSchema):
    name = 'Cancel Subscription'
    operation = 'Cancel-Subscription'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())
    header['operation_attributes'] = CancelSubscriptionOperationAttributes(
        widget=IPPTupleWidget())
    object_attributes_tag = colander.null


cancel_job_schema = CancelJobSchema(widget=IPPBodyWidget())

release_job_schema = ReleaseJobSchema(widget=IPPBodyWidget())

create_printer_subscription_schema = CreatePrinterSubscriptionSchema(
    widget=IPPBodyWidget())

cups_add_modify_class_schema = CupsAddModifyClassSchema(
    widget=IPPBodyWidget())

cups_add_modify_printer_schema = CupsAddModifyPrinterSchema(
    widget=IPPBodyWidget())

cups_delete_printer_schema = CupsDeletePrinterSchema(
    widget=IPPBodyWidget())

cups_delete_class_schema = CupsDeleteClassSchema(
    widget=IPPBodyWidget())

cups_get_classes_schema = CupsGetClassesSchema(widget=IPPBodyWidget())

cups_get_devices_schema = CupsGetDevicesSchema(widget=IPPBodyWidget())

cups_get_ppds_schema = CupsGetPPDsSchema(widget=IPPBodyWidget())

cups_get_printers_schema = CupsGetPrintersSchema(widget=IPPBodyWidget())

cups_move_job_schema = CupsMoveJobSchema(widget=IPPBodyWidget())

cups_reject_jobs_schema = CupsRejectJobsSchema(widget=IPPBodyWidget())

get_job_attributes_schema = GetJobAttributesSchema(widget=IPPBodyWidget())

get_jobs_schema = GetJobsSchema(widget=IPPBodyWidget())

get_printer_attributes_schema = GetPrinterAttributesSchema(
    widget=IPPBodyWidget())

get_subscriptions_schema = GetSubscriptionsSchema(widget=IPPBodyWidget())

pause_printer_schema = PausePrinterSchema(widget=IPPBodyWidget())

resume_printer_schema = ResumePrinterSchema(widget=IPPBodyWidget())

hold_new_jobs_schema = HoldNewJobsSchema(widget=IPPBodyWidget())

release_held_new_jobs_schema = ReleaseHeldNewJobsSchema(widget=IPPBodyWidget())

cancel_subscription_schema = CancelSubscriptionSchema(widget=IPPBodyWidget())
