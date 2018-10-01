from synopse import Blueprint, Attribute, Structure


def create_blueprint_class(**attributes):
    return type("BlueprintToTest", (Blueprint,), attributes)


class TestBlueprintDescription:
    def test_init_attribute(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        blueprint = blueprint_class(my_attr=True)
        assert blueprint.my_attr is True

    def test_eq_based_on_attributes(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute()[0],
                                                 another_attr=Attribute()[1])
        assert blueprint_class("Test", 100) == blueprint_class("Test", 100)
        assert blueprint_class("Test", 100) != blueprint_class("Test", 101)

    def test_neq_if_different_class(self):
        assert create_blueprint_class()() != create_blueprint_class()()

    def test_update_attributes(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        blueprint = blueprint_class(my_attr=True)
        blueprint.update(blueprint_class(my_attr=False))
        assert not blueprint.my_attr

    def test_update_set_new(self):
        blueprint_class = create_blueprint_class(
            structure_definition=lambda _self: Blueprint())
        blueprint = blueprint_class()
        blueprint.update(blueprint_class())
        assert {0: Blueprint()} == blueprint.structure

    def test_update_del_old(self):
        blueprint = Blueprint()
        blueprint.structure = Structure(Blueprint())
        blueprint.update(Blueprint())
        assert {} == blueprint.structure

    def test_update_replace_old_with_new(self):
        new_blueprint = create_blueprint_class()
        blueprint = Blueprint()
        blueprint.structure = Structure((Blueprint(), Blueprint()))
        blueprint.structure_definition = lambda: (new_blueprint(),  Blueprint())
        blueprint.update(Blueprint())
        assert {0: new_blueprint(), 1: Blueprint()} == blueprint.structure

    def test_update_insert_after_delete(self):
        blueprint = Blueprint()
        blueprint.structure = Structure(Blueprint())
        blueprint.structure_definition=lambda: (None, Blueprint())
        blueprint.update(Blueprint())
        assert {0: Blueprint()} == blueprint.structure
