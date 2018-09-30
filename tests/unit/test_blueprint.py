from pricky import Blueprint, Attribute, Structure


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
        old = blueprint_class(my_attr=True)
        new = blueprint_class(my_attr=False)
        old.update(new)
        assert not old.my_attr

    def test_update_set_new(self):
        blueprint = Blueprint()
        new_blueprint = Blueprint()
        target = Blueprint()
        # pylint: disable=unnecessary-lambda
        target.structure_definition = lambda: Blueprint()
        blueprint.update(target)
        assert {0: new_blueprint} == blueprint.structure

    def test_update_del_old(self):
        blueprint = Blueprint()
        blueprint.structure[0] = Blueprint()
        blueprint.update(Blueprint())
        assert {} == blueprint.structure

    def test_update_replace_old_with_new(self):
        new_child = create_blueprint_class()()
        blueprint = Blueprint()
        blueprint.structure = Structure(Blueprint())
        target = Blueprint()
        target.structure_definition = lambda: new_child
        blueprint.update(target)
        assert {0: new_child} == blueprint.structure
