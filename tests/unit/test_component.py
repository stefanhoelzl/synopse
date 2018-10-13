from synopse import Component


def create_component_class(**attributes):
    return type("ComponentToTest", (Component,), attributes)


class ComponentMock:
    def __init__(self, eq=True, create_returns="ComponentMock"):
        self.create_returns = create_returns
        self.calls = []
        self.equals = eq

    @property
    def state(self):
        if not self.calls:
            return None
        return self.calls[-1]

    def __eq__(self, other):
        return self.equals and other.equals

    def create(self):
        self.calls.append("created")
        return self.create_returns

    def update(self, target):  # pylint: disable=unused-argument
        self.calls.append("updated")

    def destroy(self):
        self.calls.append("destroyed")


def component_class_rendering_to_mock(mocks=None, **attributes):
    component_class = create_component_class(
        rendering_mocks=mocks if mocks  else ComponentMock(),
        **attributes
    )
    component_class.render = lambda s: s.rendering_mocks \
        if not isinstance(s.rendering_mocks, list) \
        else s.rendering_mocks.pop(0)
    return component_class


class TestComponent:
    def test_create_set_rendering(self):
        component = component_class_rendering_to_mock()()
        component.create()
        assert component.rendering_mocks == component.rendering

    def test_create_recursive(self):
        component = component_class_rendering_to_mock()()
        component.create()
        assert "created" == component.rendering_mocks.state

    def test_create_return_recursive_result(self):
        component = component_class_rendering_to_mock()()
        assert "ComponentMock" == component.create()

    def test_destroy_recursive(self):
        component = component_class_rendering_to_mock()()
        component.create()
        component.destroy()
        assert "destroyed" == component.rendering_mocks.state

    def test_destroy_set_rendering_to_none(self):
        component = component_class_rendering_to_mock()()
        component.create()
        component.destroy()
        assert component.rendering is None

    def test_update_skip_if_target_is_same(self):
        component = component_class_rendering_to_mock()()
        component.create()
        component.update(ComponentMock())
        assert "created" == component.rendering.state

    def test_update_recoursive_if_same_type(self):
        component = component_class_rendering_to_mock(
            mocks=ComponentMock(eq=False)
        )()
        component.create()
        component.update(Component())
        assert "updated" == component.rendering.state

    def test_destroy_and_create_if_different_type(self):
        old_rendering = ComponentMock(eq=False)
        new_rendering = type("AnotherMock", (ComponentMock,), {})()
        component = component_class_rendering_to_mock(
            mocks=[old_rendering, new_rendering]
        )()
        component.create()
        component.update(Component())
        assert "destroyed" == old_rendering.calls[-1]
        assert "created" == new_rendering.calls[-1]
