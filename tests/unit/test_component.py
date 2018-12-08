from unittest.mock import MagicMock

import pytest

from synopse import Attribute
from synopse.component import Component


class TestComponent:
    def test_init_attribute(self, create_component_class):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        assert component.my_attr is True

    def test_init_subclass_create_own_copy_of_attribute_definitions(
            self, create_component_class):
        create_component_class(my_attr=Attribute())
        assert {} == Component.Attributes

    def test_content_require_being_mounted_for_access(self, component):
        with pytest.raises(RuntimeError):
            assert component.content

    def test_eq_based_on_attributes(self, create_component_class):
        component_class = create_component_class(
            my_attr=Attribute()[0], another_attr=Attribute()[1]
        )
        assert component_class("Test", 100) == component_class("Test", 100)
        assert component_class("Test", 100) != component_class("Test", 101)

    def test_neq_if_different_class(self, create_component_class):
        assert create_component_class()() != create_component_class()()

    def test_attributes_readonly(self, create_component_class):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        with pytest.raises(AttributeError):
            component.my_attr = False

    def test_update_attributes(self, create_component_class):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        component.update({"my_attr": False})
        assert not component.my_attr

    def test_update_keep_attributes(self, create_component_class):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        component.update()
        assert component.my_attr

    def test_mount_set_index(self, component, index):
        component.mount(index)
        assert component.index is index

    def test_mount_set_content(self, component):
        component.layout = MagicMock(return_value="LAYOUT")
        component.mount()
        assert "LAYOUT" == component.content

    def test_unmount_delete_index(self, component, index):
        component.mount(index)
        component.unmount()
        assert component.index is None

    def test_unmount_delete_content(self, component):
        component.mount()
        component.unmount()
        with pytest.raises(RuntimeError):
            assert component.content
