from pricky import Blueprint, Attribute


def create_blueprint_class(**attributes):
    return type("BlueprintToTest", (Blueprint,), attributes)


class TestBlueprintDescription:
    def test_init_attribute(self):
        blueprint_class = create_blueprint_class(my_attr=Attribute())
        b = blueprint_class(my_attr=True)
        assert b.my_attr is True
