from unittest import mock

import pytest

from synopse import Attribute
from synopse.base_component import BaseComponent, Patch, SetAttribute, \
    temporary_attributes


def create_component_class(**attributes):
    return type("ComponentToTest", (BaseComponent,), attributes)


class TestBaseComponent:
    def test_init_attribute(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        assert component.my_attr is True

    def test_init_subclass_create_own_copy_of_attribute_definitions(self):
        create_component_class(my_attr=Attribute())
        assert {} == BaseComponent.Attributes

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

    def test_diff_yield_diff_attribute_for_changed_attribute(self):
        component = create_component_class(my_attr=Attribute())(
            attr_a=False, attr_b=False)
        component.diff_attribute = lambda n, v: ((n, v),)
        assert (("attr_a", True),) == tuple(component.diff(attr_a=True))

    def test_diff_attribute_yields_set_attribute(self):
        component = BaseComponent()
        patch = tuple(component.diff_attribute("attr", True))
        assert (SetAttribute(component, "attr", True),) == patch

    def test_update_apply_diff_patches_and_pass_attributes(self):
        patches = [Patch(), Patch()]
        patches[0].apply = mock.MagicMock()
        patches[1].apply = mock.MagicMock()
        component = BaseComponent()
        component.diff = mock.MagicMock(side_effect=(patches,))

        component.update(attr=True)

        component.diff.assert_called_once_with(attr=True)
        patches[0].apply.assert_called_once_with()
        patches[1].apply.assert_called_once_with()


class TestTemporaryComponent:
    def test_set_and_restore_attributes(self):
        component = BaseComponent()
        component.attributes = {"a": True}
        with temporary_attributes(component, {"b": True}):
            assert {"b": True} == component.attributes
        assert {"a": True} == component.attributes


class TestSetAttributePatch:
    def test_apply_set_attribute_on_component(self):
        component = create_component_class(my_attr=Attribute())(my_attr=False)
        patch = SetAttribute(component, "my_attr", True)
        patch.apply()
        assert component.my_attr
