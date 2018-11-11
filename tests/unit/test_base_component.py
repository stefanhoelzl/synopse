import pytest

from synopse import Attribute
from synopse.base_component import BaseComponent


def create_component_class(**attributes):
    return type("ComponentToTest", (BaseComponent,), attributes)


class TestBaseComponent:
    def test_init_attribute(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        assert component.my_attr is True

    def test_eq_based_on_attributes(self):
        component_class = create_component_class(my_attr=Attribute()[0],
                                                 another_attr=Attribute()[1])
        assert component_class("Test", 100) == component_class("Test", 100)
        assert component_class("Test", 100) != component_class("Test", 101)

    def test_neq_if_different_class(self):
        assert create_component_class()() != create_component_class()()

    def test_attributes_readonly(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        with pytest.raises(AttributeError):
            component.my_attr = False

    def test_init_subclass_create_own_copy_of_attribute_definitions(self):
        create_component_class(my_attr=Attribute())
        assert [] == BaseComponent.AttributeDefinitions
