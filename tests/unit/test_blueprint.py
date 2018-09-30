from pricky import Blueprint, Attribute


def create_blueprint_class(**attributes):
    return type("BlueprintToTest", (Blueprint,), attributes)


class TestBlueprintDescription:
    def test_init_attribute(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        b = blueprint_class(my_attr=True)
        assert b.my_attr is True


def create_structure_blueprint(structure_definition):
        blueprint = Blueprint()
        blueprint.structure_definition = lambda: structure_definition
        return blueprint


class TestStructuredBlueprint:
    def test_rebuild_structure_from_dict(self):
        sub_blueprint = Blueprint()
        blueprint = create_structure_blueprint({0: sub_blueprint})
        assert {0: sub_blueprint} == blueprint.rebuild_structure()

    def test_rebuild_structure_from_none(self):
        blueprint = create_structure_blueprint(None)
        assert {} == blueprint.rebuild_structure()

    def test_rebuild_structure_from_blueprint(self):
        sub_blueprint = Blueprint()
        blueprint = create_structure_blueprint(sub_blueprint)
        assert {0: sub_blueprint} == blueprint.rebuild_structure()

    def test_rebuild_structure_from_iterable(self):
        blueprint_iter = (Blueprint(), Blueprint(), Blueprint())
        blueprint = create_structure_blueprint(blueprint_iter)
        assert {0: blueprint_iter[0],
                1: blueprint_iter[1],
                2: blueprint_iter[2]} == blueprint.rebuild_structure()
