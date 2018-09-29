from pricky import blueprint, Attribute


def create_blueprint_class(**attributes):
    return blueprint("BlueprintToTest", (), attributes)


class TestBlueprint:
    def test_init_attribute(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        b = blueprint_class(my_attr=True)
        assert b.my_attr is True
