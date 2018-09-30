import pytest

from pricky.attributes import Attribute, NamedAttribute
from pricky.errors import AttributeValidationFailed, RequiredAttributeMissing


class TestAttribute:
    def test_set_position_on_getitem(self):
        attr = Attribute()[1]
        assert 1 == attr.position


class TestNamedAttribute:
    def test_extract_value_from_keyword_attributes(self):
        attr = NamedAttribute(name="my_attr")
        assert 1 == attr.extract_value(my_attr=1)

    def test_extract_value_from_positional_attribute(self):
        attr = NamedAttribute(name="my_attr", position=0)
        assert 1 == attr.extract_value(1)

    def test_extract_value_from_sliced_positional_attribute(self):
        attr = NamedAttribute(name="my_attr", position=slice(1, 6, 2))
        assert (1, 3, 5) == attr.extract_value(*tuple(range(9)))

    def test_extract_default_value_from_keyword_attributes(self):
        attr = NamedAttribute(name="my_attr", default=True)
        assert attr.extract_value()

    def test_extract_default_value_from_positional_attributes(self):
        attr = NamedAttribute(name="my_attr", default=True, position=0)
        assert attr.extract_value()

    def test_extract_value_default(self):
        attr = NamedAttribute(name="my_attr")
        assert attr.extract_value() is None

    def test_extract_value_raises_exception_when_required_and_not_given(self):
        attr = NamedAttribute(name="my_attr", required=True)
        with pytest.raises(RequiredAttributeMissing):
            attr.extract_value()

    def test_extract_value_with_successfull_validation(self):
        attr = NamedAttribute(name="my_attr", validator=lambda a: True)
        assert attr.extract_value() is None

    def test_extract_value_raises_exception_when_validation_fails(self):
        attr = NamedAttribute(name="my_attr", validator=lambda a: False)
        with pytest.raises(AttributeValidationFailed):
            attr.extract_value()
