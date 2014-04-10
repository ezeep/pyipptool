import re

import colander
from .widgets import (IPPAttributeWidget,
                      IPPBodyWidget,
                      IPPFileWidget,
                      IPPGroupWidget,
                      IPPNameWidget)


class IntegerOrTuple(colander.List):
    def serialize(self, node, appstruct):
        if isinstance(appstruct, (tuple, list)):
            return super(IntegerOrTuple, self).serialize(
                node,
                ','.join([str(i) for i in appstruct]))
        return super(IntegerOrTuple, self).serialize(node, appstruct)


class StringOrTuple(colander.String):
    def serialize(self, node, appstruct):
        if isinstance(appstruct, (tuple, list)):
            return super(StringOrTuple, self).serialize(node,
                                                        ','.join(appstruct))
        return super(StringOrTuple, self).serialize(node, appstruct)


class Charset(colander.String):
    pass


class Enum(colander.String):
    pass


class Integer(IntegerOrTuple):
    pass


class Keyword(StringOrTuple):
    pass


class Language(colander.String):
    pass


class MimeMediaType(colander.String):
    pass


class Name(colander.String):
    pass


class NaturalLanguage(colander.String):
    pass


class RangeOfInteger(colander.String):
    pass


class Resolution(colander.String):
    pass


range_regex = re.compile('^(\d+)-(\d+)$')


def range_of_integer_validator(node, value):
    match = range_regex.match(value)
    if match is None:
        raise colander.Invalid(node,
                               "Invalid range e.g '1-5'")
    low, high = match.groups()
    if int(low) >= int(high):
        raise colander.Invalid(node,
                               'Low bound must be lower than high bound')


class Text(colander.String):
    def serialize(self, node, appstruct):
        if appstruct is None:
            raise ValueError('None value provided for {!r}'.format(node.name))
        if appstruct is colander.null:
            return colander.null
        value = super(Text, self).serialize(node, appstruct)
        return '"{}"'.format(value)


class Uri(StringOrTuple):
    pass


class OperationAttributesGroup(colander.Schema):
    attributes_charset = colander.SchemaNode(Charset(),
                                             default='utf-8',
                                             widget=IPPAttributeWidget())
    attributes_natural_language = colander.SchemaNode(
        Language(),
        default='en',
        widget=IPPAttributeWidget())
    compression = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    printer_uri = colander.SchemaNode(Uri(),
                                      widget=IPPAttributeWidget())
    job_uri = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())
    job_id = colander.SchemaNode(colander.Integer(),
                                 widget=IPPAttributeWidget())
    exclude_schemes = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    include_schemes = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    limit = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())
    purge_job = colander.SchemaNode(colander.Boolean(true_val=1, false_val=0),
                                    widget=IPPAttributeWidget())
    requesting_user_name = colander.SchemaNode(Name(),
                                               widget=IPPAttributeWidget())
    job_name = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    ipp_attribute_fidelity = colander.SchemaNode(colander.Boolean(true_val=1,
                                                                  false_val=0),
                                                 widget=IPPAttributeWidget())
    job_k_octets = colander.SchemaNode(Integer(), widget=IPPAttributeWidget())
    job_impressions = colander.SchemaNode(Integer(),
                                          widget=IPPAttributeWidget())
    job_media_sheets = colander.SchemaNode(Integer(),
                                           widget=IPPAttributeWidget())
    document_name = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    device_class = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    document_format = colander.SchemaNode(MimeMediaType(),
                                          widget=IPPAttributeWidget())
    document_natural_language = colander.SchemaNode(
        NaturalLanguage(),
        widget=IPPAttributeWidget())

    notify_subscription_id = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())

    printer_message_from_operator = colander.SchemaNode(
        Text(), widget=IPPAttributeWidget())

    limit = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    requested_attributes = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())
    which_jobs = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    my_jobs = colander.SchemaNode(colander.Boolean(true_val=1, false_val=0),
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

    notify_subscription_ids = colander.SchemaNode(
        Integer(),
        widget=IPPAttributeWidget())
    notify_sequence_numbers = colander.SchemaNode(
        Integer(),
        widget=IPPAttributeWidget())
    notify_wait = colander.SchemaNode(
        colander.Boolean(false_val=0, true_val=1),
        widget=IPPAttributeWidget())

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

    timeout = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())

    first_printer_name = colander.SchemaNode(
        Name(),
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

    document_name = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    compression = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    document_format = colander.SchemaNode(MimeMediaType(),
                                          widget=IPPAttributeWidget())
    document_natural_language = colander.SchemaNode(
        NaturalLanguage(),
        widget=IPPAttributeWidget())
    last_document = colander.SchemaNode(
        colander.Boolean(false_val=0, true_val=1),
        widget=IPPAttributeWidget())


class JobAttributesGroup(colander.Schema):
    job_priority = colander.SchemaNode(Integer(),
                                       widget=IPPAttributeWidget())
    job_printer_uri = colander.SchemaNode(Uri(),
                                          widget=IPPAttributeWidget())
    job_hold_until = colander.SchemaNode(Keyword(),
                                         widget=IPPAttributeWidget())
    job_sheets = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    auth_info = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    job_billing = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    multiple_document_handling = colander.SchemaNode(
        Keyword(),
        widget=IPPAttributeWidget())
    copies = colander.SchemaNode(Integer(), widget=IPPAttributeWidget())
    finishings = colander.SchemaNode(Enum(), widget=IPPAttributeWidget())
    page_ranges = colander.SchemaNode(RangeOfInteger(),
                                      widget=IPPAttributeWidget(),
                                      validator=range_of_integer_validator)
    sides = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    number_up = colander.SchemaNode(Integer(), widget=IPPAttributeWidget())
    orientation_requested = colander.SchemaNode(Enum(),
                                                widget=IPPAttributeWidget())
    media = colander.SchemaNode(Keyword(), widget=IPPAttributeWidget())
    printer_resolution = colander.SchemaNode(Resolution(),
                                             widget=IPPAttributeWidget())
    print_quality = colander.SchemaNode(Enum(), widget=IPPAttributeWidget())

    # Arbitrary Job Attributes
    ezeep_job_uuid = colander.SchemaNode(Text(),
                                         widget=IPPAttributeWidget())


class SubscriptionGroup(colander.Schema):
    notify_recipient_uri = colander.SchemaNode(Uri(),
                                               widget=IPPAttributeWidget())
    notify_events = colander.SchemaNode(Keyword(),
                                        widget=IPPAttributeWidget())
    notify_job_id = colander.SchemaNode(colander.Integer(),
                                        widget=IPPAttributeWidget())
    notify_pull_method = colander.SchemaNode(Keyword(),
                                             widget=IPPAttributeWidget())
    notify_attributes = colander.SchemaNode(Keyword(),
                                            widget=IPPAttributeWidget())
    notify_charset = colander.SchemaNode(Charset(),
                                         widget=IPPAttributeWidget())
    notify_natural_language = colander.SchemaNode(Language(),
                                                  widget=IPPAttributeWidget())
    notify_time_interval = colander.SchemaNode(colander.Integer(),
                                               widget=IPPAttributeWidget())
    notify_lease_duration = colander.SchemaNode(colander.Integer(),
                                                widget=IPPAttributeWidget())


class DocumentAttributesGroup(colander.Schema):
    file = colander.SchemaNode(colander.String(), widget=IPPFileWidget())


class PrinterAttributesGroup(colander.Schema):
    auth_info_required = colander.SchemaNode(Keyword(),
                                             widget=IPPAttributeWidget())

    printer_is_accepting_jobs = colander.SchemaNode(
        colander.Boolean(false_val=0, true_val=1),
        widget=IPPAttributeWidget())
    printer_info = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    printer_location = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    printer_more_info = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())
    printer_op_policy = colander.SchemaNode(Name(),
                                            widget=IPPAttributeWidget())
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
    printer_is_shared = colander.SchemaNode(colander.Boolean(true_val=1,
                                                             false_val=0),
                                            widget=IPPAttributeWidget())
    job_sheets_default = colander.SchemaNode(Name(),
                                             widget=IPPAttributeWidget())
    device_uri = colander.SchemaNode(Uri(),
                                     widget=IPPAttributeWidget())
    port_monitor = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    ppd_name = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    member_uris = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())


class BaseIPPSchema(colander.Schema):
    name = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation_attributes_tag = OperationAttributesGroup(
        widget=IPPGroupWidget())


class CancelJobSchema(BaseIPPSchema):
    name = 'Cancel Job'
    operation = 'Cancel-Job'


class ReleaseJobSchema(BaseIPPSchema):
    name = 'Release Job'
    operation = 'Release-Job'


class CupsAddModifyPrinterSchema(BaseIPPSchema):
    name = 'CUPS Add Modify Printer'
    operation = 'CUPS-Add-Modify-Printer'
    printer_attributes_tag = PrinterAttributesGroup(widget=IPPGroupWidget())


class CupsDeletePrinterSchema(BaseIPPSchema):
    name = 'CUPS Delete Printer'
    operation = 'CUPS-Delete-Printer'


class CupsAddModifyClassSchema(BaseIPPSchema):
    name = 'CUPS Add Modify Class'
    operation = 'CUPS-Add-Modify-Class'
    printer_attributes_tag = PrinterAttributesGroup(widget=IPPGroupWidget())


class CupsDeleteClassSchema(CupsDeletePrinterSchema):
    name = 'CUPS Delete Class'
    operation = 'CUPS-Delete-Class'


class CupsGetClassesSchema(BaseIPPSchema):
    name = 'CUPS Get Classes'
    operation = 'CUPS-Get-Classes'


class CupsGetDevicesSchema(BaseIPPSchema):
    name = 'CUPS Get Devices'
    operation = 'CUPS-Get-Devices'


class CupsGetPPDsSchema(BaseIPPSchema):
    name = 'CUPS Get PPDs'
    operation = 'CUPS-Get-PPDs'


class CupsGetPrintersSchema(CupsGetClassesSchema):
    name = 'CUPS Get Printers'
    operation = 'CUPS-Get-Printers'


class CupsMoveJobSchema(BaseIPPSchema):
    name = 'CUPS Move Job'
    operation = 'CUPS-Move-Job'
    job_attributes_tag = JobAttributesGroup(widget=IPPGroupWidget())


class CupsRejectJobsSchema(BaseIPPSchema):
    name = 'CUPS Reject Jobs'
    operation = 'CUPS-Reject-Jobs'
    printer_attributes_tag = PrinterAttributesGroup(widget=IPPGroupWidget())


class CreateJobSchema(BaseIPPSchema):
    """
    http://www.cups.org/documentation.php/spec-ipp.html#CREATE_JOB
    """
    name = 'Create Job'
    operation = 'Create-Job'
    job_attributes_tag = JobAttributesGroup(widget=IPPGroupWidget())


class CreateJobSubscriptionSchema(BaseIPPSchema):
    name = 'Create Job Subscription'
    operation = 'Create-Job-Subscription'
    subscription_attributes_tag = SubscriptionGroup(
        widget=IPPGroupWidget())


class CreatePrinterSubscriptionSchema(CreateJobSubscriptionSchema):
    name = 'Create Printer Subscription'
    operation = 'Create-Printer-Subscription'


class GetJobAttributesSchema(BaseIPPSchema):
    name = 'Get Job Attributes'
    operation = 'Get-Job-Attributes'


class GetJobsSchema(BaseIPPSchema):
    name = 'Get Jobs'
    operation = 'Get-Jobs'


class GetPrinterAttributesSchema(BaseIPPSchema):
    name = 'Get Printer Attributes'
    operation = 'Get-Printer-Attributes'


class GetSubscriptionsSchema(BaseIPPSchema):
    name = 'Get Subscriptions'
    operation = 'Get-Subscriptions'


class GetNotificationsSchema(BaseIPPSchema):
    name = 'Get Notifications'
    operation = 'Get-Notifications'


class PausePrinterSchema(BaseIPPSchema):
    name = 'Pause Printer'
    operation = 'Pause-Printer'


class PrintJobSchema(CreateJobSchema):
    name = 'Print Job'
    operation = 'Print-Job'
    job_attributes_tag = JobAttributesGroup(widget=IPPGroupWidget())
    subscription_attributes_tag = SubscriptionGroup(
        widget=IPPGroupWidget())
    document_attributes_tag = DocumentAttributesGroup(widget=IPPGroupWidget())


class ResumePrinterSchema(PausePrinterSchema):
    name = 'Resume Printer'
    operation = 'Resume-Printer'


class SendDocumentSchema(BaseIPPSchema):
    name = 'Send Document'
    operation = 'Send-Document'
    document_attributes_tag = DocumentAttributesGroup(widget=IPPGroupWidget())


class HoldNewJobsSchema(PausePrinterSchema):
    name = 'Hold New Jobs'
    operation = 'Hold-New-Jobs'


class ReleaseHeldNewJobsSchema(HoldNewJobsSchema):
    name = 'Release Held New Jobs'
    operation = 'Release-Held-New-Jobs'


class CancelSubscriptionSchema(BaseIPPSchema):
    name = 'Cancel Subscription'
    operation = 'Cancel-Subscription'


cancel_job_schema = CancelJobSchema(widget=IPPBodyWidget())

release_job_schema = ReleaseJobSchema(widget=IPPBodyWidget())

create_job_subscription_schema = CreateJobSubscriptionSchema(
    widget=IPPBodyWidget())

create_job_schema = CreateJobSchema(widget=IPPBodyWidget())

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

get_notifications_schema = GetNotificationsSchema(widget=IPPBodyWidget())

pause_printer_schema = PausePrinterSchema(widget=IPPBodyWidget())

print_job_schema = PrintJobSchema(widget=IPPBodyWidget())

resume_printer_schema = ResumePrinterSchema(widget=IPPBodyWidget())

send_document_schema = SendDocumentSchema(widget=IPPBodyWidget())

hold_new_jobs_schema = HoldNewJobsSchema(widget=IPPBodyWidget())

release_held_new_jobs_schema = ReleaseHeldNewJobsSchema(widget=IPPBodyWidget())

cancel_subscription_schema = CancelSubscriptionSchema(widget=IPPBodyWidget())
