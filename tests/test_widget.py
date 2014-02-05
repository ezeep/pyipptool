import colander
from deform.tests.test_widget import DummyField, DummyRenderer
import pytest


class DummyType(object):
    pass


class DummySchema(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


def test_ipp_attribute_widget_null():
    from pyipptool.widgets import IPPAttributeWidget
    widget = IPPAttributeWidget()
    rendrer = DummyRenderer()
    field = DummyField(None, renderer=rendrer)
    response = widget.serialize(field, colander.null)
    assert response == ''


def test_ipp_attribute_widget_with_value():
    from pyipptool.widgets import IPPAttributeWidget
    widget = IPPAttributeWidget()
    rendrer = DummyRenderer()
    schema = DummySchema()
    schema.typ = DummyType()
    field = DummyField(schema, renderer=rendrer)
    response = widget.serialize(field, 'hello')
    assert response == 'ATTR dummyType name hello'


def test_ipp_attribute_widget_with_None():
    from pyipptool.widgets import IPPAttributeWidget
    widget = IPPAttributeWidget()
    rendrer = DummyRenderer()
    schema = DummySchema()
    schema.typ = DummyType()
    field = DummyField(schema, renderer=rendrer)
    with pytest.raises(ValueError) as exc_info:
        widget.serialize(field, None)
    assert exc_info.value.message == "None value provided for 'name'"


def test_ipp_display_widget():
    from pyipptool.widgets import IPPDisplayWidget
    widget = IPPDisplayWidget()
    rendrer = DummyRenderer()
    field = DummyField(None, renderer=rendrer)
    response = widget.serialize(field, None)
    assert response == 'DISPLAY name'


def test_ipp_name_widget():
    from pyipptool.widgets import IPPNameWidget
    widget = IPPNameWidget()
    rendrer = DummyRenderer()
    schema = DummySchema(name='FOO')

    field = DummyField(schema, renderer=rendrer)
    field.parent = None
    sub_field = DummyField(None, renderer=rendrer)
    sub_field.parent = field

    response = widget.serialize(sub_field, 'world')
    assert response == 'NAME "FOO"'


def test_ipp_group_widget():
    from pyipptool.widgets import IPPGroupWidget
    widget = IPPGroupWidget()
    rendrer = DummyRenderer()
    schema = DummySchema(name='FOO')

    field = DummyField(schema, renderer=rendrer)
    field.parent = None
    sub_field = DummyField(None, renderer=rendrer)
    sub_field.parent = field

    response = widget.serialize(sub_field, 'world')
    assert response == 'GROUP FOO'
