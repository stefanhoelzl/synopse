from synopse import Component, Attribute, Structure


def create_component_class(**attributes):
    return type("ComponentToTest", (Component,), attributes)


class TestComponentDescription:
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

    def test_update_without_target(self):
        component = Component()
        component.update()

    def test_update_attributes(self):
        component_class = create_component_class(my_attr=Attribute())
        component = component_class(my_attr=True)
        component.update(component_class(my_attr=False))
        assert not component.my_attr

    def test_update_set_new(self):
        component = Component()
        component.structure = lambda: (Component(),)
        component.update()
        assert {0: Component()} == component.structure_instance

    def test_update_del_old(self):
        component = Component()
        component.structure_instance = Structure(Component())
        component.update()
        assert {} == component.structure_instance

    def test_update_replace_old_with_new(self):
        new_component = create_component_class()
        component = Component()
        component.structure_instance = Structure((Component(), Component()))
        component.structure = lambda: (new_component(), Component())
        component.update()
        assert {0: new_component(), 1: Component()} == component.structure_instance

    def test_update_insert_after_delete(self):
        component = Component()
        component.structure_instance = Structure(Component())
        component.structure = lambda: (None, Component())
        component.update()
        assert {0: Component()} == component.structure_instance

    def test_update_empty_structure_with_none(self):
        component = Component()
        component.structure_instance = Structure()
        component.structure = lambda: (None,)
        component.update()
        assert {} == component.structure_instance

    def test_update_recursive(self):
        component_class = create_component_class(attr=Attribute())
        component = Component()
        sub_component = component_class(attr=False)
        component.structure_instance = Structure(sub_component)
        component.structure = lambda: component_class(attr=True)
        component.update()
        assert {0: sub_component} == component.structure_instance
        assert sub_component.attr
