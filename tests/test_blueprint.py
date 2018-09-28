import pytest

from pricky import blueprint, Attribute, \
    RequiredAttributeMissing, AttributeValidationFailed


def create_blueprint_class(**attributes):
    return blueprint("BlueprintToTest", (), attributes)


class TestBlueprint:
    def test_init_keyword_attribute(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        b = blueprint_class(my_attr=True)
        assert b.my_attr is True

    def test_init_keyword_attribute_to_none_if_not_specified(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        b = blueprint_class()
        assert b.my_attr is None

    def test_init_keyword_attribute_with_default(self):
        blueprint_class = create_blueprint_class(
            my_attr=Attribute(default=True)
        )
        b = blueprint_class()
        assert b.my_attr is True

    def test_init_required_keyword_attribute_raises_execption(self):
        blueprint_class = create_blueprint_class(
            my_attr=Attribute(required=True)
        )
        with pytest.raises(RequiredAttributeMissing):
            blueprint_class()

    def test_init_successfull_attribute_validation(self):
        blueprint_class = create_blueprint_class(
            my_attr=Attribute(validator=lambda attr: True)
        )
        blueprint_class(my_attr=None)

    def test_init_attribute_validation_error(self):
        blueprint_class = create_blueprint_class(
            my_attr=Attribute(validator=lambda attr: False)
        )
        with pytest.raises(AttributeValidationFailed):
            blueprint_class(my_attr=None)

    def test_init_single_positional_argument(self):
        blueprint_class = create_blueprint_class(
            my_attr=Attribute()[0]
        )
        b = blueprint_class(True)
        assert b.my_attr is True

    def test_init_positional_argument_with_default(self):
        blueprint_class = create_blueprint_class(
            my_attr=Attribute(default=True)[0]
        )
        b = blueprint_class()
        assert b.my_attr is True

    def test_init_slice_of_positional_arguments(self):
        blueprint_class = create_blueprint_class(
            my_attr=Attribute()[1:6:2]
        )
        b = blueprint_class(0, 1, 2, 3, 4, 5, 6, 7, 8)
        assert (1, 3, 5) == b.my_attr
