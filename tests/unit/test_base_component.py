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

    def test_update_attributes(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        component.update(component_class(my_attr=False))
        assert not component.my_attr
