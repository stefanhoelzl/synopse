from synopse.utils.attributes import IntAttribute, FloatAttribute, \
    StrAttribute, TupleAttribute


def test_int_attribute(create_component_class):
    component_class = create_component_class(i=IntAttribute())
    assert component_class(i="100").i == 100
    assert component_class(i="0xFF").i == 255
    assert component_class(i=1).i == 1


def test_float_attribute(create_component_class):
    component_class = create_component_class(i=FloatAttribute())
    assert component_class(i="1.1").i == 1.1
    assert component_class(i=1.5).i == 1.5


def test_str_attribute(create_component_class):
    component_class = create_component_class(i=StrAttribute())
    assert component_class(i=1).i == "1"
