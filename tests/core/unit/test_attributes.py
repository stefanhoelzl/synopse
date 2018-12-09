import pytest

from synopse.core.attributes import Attribute, extract_values
from synopse.core.errors import AttributeValidationFailed, \
    RequiredAttributeMissing


class TestAttribute:
    def test_set_position_on_getitem(self):
        attr = Attribute()[1]
        assert 1 == attr.position


class TestExtractValue:
    def test_from_keyword_attributes(self):
        assert {"my_attr": 1} == \
               extract_values({"my_attr": Attribute()}, my_attr=1)

    def test_from_positional_attribute(self):
        assert {"my_attr": 1} == \
               extract_values({"my_attr": Attribute(position=0)}, 1)

    def test_from_sliced_positional_attribute(self):
        assert {"my_attr": (1, 3, 5)} == \
               extract_values({"my_attr": Attribute(position=slice(1, 6, 2))},
                              *tuple(range(9)))

    def test_default_value_from_keyword_attributes(self):
        assert {"my_attr": True} == \
               extract_values({"my_attr": Attribute(default=True)})

    def test_default_value_from_positional_attributes(self):
        assert {"my_attr": True} == \
               extract_values({"my_attr": Attribute(default=True, position=0)})

    def test_default_is_none(self):
        assert {"my_attr": None} == extract_values({"my_attr": Attribute()})

    def test_raises_exception_when_required_and_not_given(self):
        with pytest.raises(RequiredAttributeMissing):
            extract_values({"my_attr": Attribute(required=True)})

    def test_with_successfull_validation(self):
        assert {"my_attr": None} == \
               extract_values({"my_attr": Attribute(validator=lambda a: True)})

    def test_raises_exception_when_validation_fails(self):
        with pytest.raises(AttributeValidationFailed):
            extract_values({"my_attr": Attribute(validator=lambda a: False)})
