from unittest.mock import MagicMock

import pytest

from synopse import Attribute
from synopse.component import Component, Index


def create_component_class(**attributes):
    return type("ComponentToTest", (Component,), attributes)


@pytest.fixture
def component():
    component = create_component_class()()
    component.layout = MagicMock(return_value="LAYOUT")
    return component


@pytest.fixture
def index():
    return Index(None, "key", 0)


class TestComponent:
    def test_init_attribute(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        assert component.my_attr is True

    def test_init_subclass_create_own_copy_of_attribute_definitions(self):
        create_component_class(my_attr=Attribute())
        assert {} == Component.Attributes

    def test_eq_based_on_attributes(self):
        component_class = create_component_class(
            my_attr=Attribute()[0], another_attr=Attribute()[1]
        )
        assert component_class("Test", 100) == component_class("Test", 100)
        assert component_class("Test", 100) != component_class("Test", 101)

    def test_neq_if_different_class(self):
        assert create_component_class()() != create_component_class()()

    def test_attributes_readonly(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        with pytest.raises(AttributeError):
            component.my_attr = False

    def test_update_attributes(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        component.update(my_attr=False)
        assert not component.my_attr

    def test_mount_set_index(self, component, index):
        component.mount(index)
        assert component.index is index

    def test_mount_set_content(self, component, index):
        component.mount(index)
        assert "LAYOUT" == component.content

    def test_unmount_delete_index(self, component, index):
        component.mount(index)
        component.unmount()
        assert component.index is None

    def test_unmount_delete_content(self, component, index):
        component.mount(index)
        component.unmount()
        assert component.content is None
