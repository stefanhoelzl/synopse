from dui.element import Element


class TestElement:
    def test_init_props_with_kwargs(self):
        c = Element(my_prop=True)
        assert c.__properties__["my_prop"]
