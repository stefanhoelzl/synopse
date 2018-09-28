import pytest

from pricky import blueprint, Attribute, RequiredAttributeMissing


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
