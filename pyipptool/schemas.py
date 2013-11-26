import colander
from .widgets import (IPPAttributeWidget, IPPBodyWidget, IPPDisplayWidget,
                      IPPGroupWidget, IPPNameWidget, IPPTupleWidget,
                      IPPConstantTupleWidget)


class Charset(colander.String):
    pass


class Keyword(colander.String):
    pass


class Language(colander.String):
    pass


class Name(colander.String):
    pass


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


class SubscriptionOperationAttributes(OperationAttributes):
    attributes_charset = colander.SchemaNode(Charset(),
                                             default='utf-8',
                                             widget=IPPAttributeWidget())
    printer_uri = colander.SchemaNode(Uri(),
                                      widget=IPPAttributeWidget())
    requesting_user_name = colander.SchemaNode(Name(),
                                               widget=IPPAttributeWidget())


class HeaderIPPRequest(colander.Schema):
    name = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation_attributes_tag = colander.SchemaNode(colander.String(),
                                                   widget=IPPGroupWidget())
    required_attributes = OperationAttributes(widget=IPPTupleWidget())
    object_attributes_tag = colander.SchemaNode(
        colander.String(),
        widget=IPPGroupWidget())


class BaseIPPRequest(colander.Schema):
    operation_attributes_tag = 'operation-attributes-tag'
    header = HeaderIPPRequest(widget=IPPConstantTupleWidget())


class CupsAddModifyPrinterRequest(BaseIPPRequest):
    name = 'CUPS Add Modify Printer'
    operation = 'CUPS-Add-Modify-Printer'
    object_attributes_tag = 'printer-object-attributes-tag'
    device_uri = colander.SchemaNode(Uri(),
                                     widget=IPPAttributeWidget())


class CreatePrinterSubscriptionRequest(BaseIPPRequest):
    name = 'Create Printer Subscription'
    operation = 'Create-Printer-Subscription'
    object_attributes_tag = 'subscription-attributes-tag'
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


cups_add_modify_printer_schema = CupsAddModifyPrinterRequest(
    widget=IPPBodyWidget())
create_printer_subscription_schema = CreatePrinterSubscriptionRequest(
    widget=IPPBodyWidget())
create_printer_subscription_schema['header']['required_attributes'] =\
    SubscriptionOperationAttributes(widget=IPPTupleWidget())
