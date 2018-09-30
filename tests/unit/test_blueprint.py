from pricky import Blueprint, Attribute


def create_blueprint_class(**attributes):
    return type("BlueprintToTest", (Blueprint,), attributes)


class TestBlueprintDescription:
    def test_init_attribute(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        b = blueprint_class(my_attr=True)
        assert b.my_attr is True

    def test_eq_based_on_attributes(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute()[0],
                                                 another_attr=Attribute()[1])
        assert blueprint_class("Test", 100) == blueprint_class("Test", 100)
        assert blueprint_class("Test", 100) != blueprint_class("Test", 101)

    def test_neq_if_different_class(self):
        assert create_blueprint_class()() != create_blueprint_class()()

    def test_update_attributes(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        old = blueprint_class(my_attr=True)
        new = blueprint_class(my_attr=False)
        old.update(new)
        assert not old.my_attr
