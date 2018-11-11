from unittest import mock
import pytest

from synopse import Component
from synopse.component import Replace, SetRendering, IndexedComponent


class ComponentMock(IndexedComponent):
    def __init__(self, eq=True, native="native", diffs=()):
        super().__init__()
        self.calls = []
        self.equals = eq
        self.diffs = diffs
        self._native = native

    @property
    def native(self):
        return self._native

    @property
    def state(self):
        if not self.calls:
            return None
        return self.calls[-1]

    def __eq__(self, other):
        return self.equals and other.equals

    def mount(self):
        self.calls.append("mounted")

    def diff(self, **attributes):
        yield from self.diffs

    def unmount(self):
        self.calls.append("unmounted")


def create_component_class(**attributes):
    return type("ComponentToTest", (Component,), attributes)


class ComponentRenderingMocks(Component):
    def __init__(self, renderings=None):
        super().__init__()
        self.renderings = renderings if renderings else ComponentMock()

    def render(self):
        if isinstance(self.renderings, list):
            return self.renderings.pop(0)
        return self.renderings


class TestComponent:
    def test_native_from_rendered(self):
        component = ComponentRenderingMocks()
        component.mount()
        assert "native" == component.native

    def test_mount_set_rendered(self):
        component = ComponentRenderingMocks()
        component.mount()
        assert component.renderings == component.rendered

    def test_mount_recursive(self):
        component = ComponentRenderingMocks()
        component.mount()
        assert "mounted" == component.renderings.state

    def test_unmount_recursive(self):
        component = ComponentRenderingMocks()
        component.mount()
        component.unmount()
        assert "unmounted" == component.renderings.state

    def test_unmount_set_rendered_to_none(self):
        component = ComponentRenderingMocks()
        component.mount()
        component.unmount()
        assert component.rendered is None

    def test_diff_raise_runtime_error_if_not_mounted(self):
        component = ComponentRenderingMocks()
        with pytest.raises(RuntimeError):
            tuple(component.diff())

    def test_diff_replace_and_set_rendering_when_class_changed(self):
        class ComponentMockA(ComponentMock):
            pass

        class ComponentMockB(ComponentMock):
            pass

        old_rendering = ComponentMockA()
        new_rendering = ComponentMockB()
        component = ComponentRenderingMocks(renderings=[old_rendering,
                                                        new_rendering])
        component.mount()
        expected = (Replace(old_rendering, new_rendering),
                    SetRendering(component, new_rendering))
        assert expected == tuple(component.diff())

    def test_diff_yield_from_rendered_diff_when_same_class_but_different(self):
        diffs = (mock.MagicMock(), mock.MagicMock())
        component = ComponentRenderingMocks(
            renderings=ComponentMock(eq=False, diffs=diffs))
        component.mount()
        assert diffs == tuple(component.diff())

    def test_diff_nothing_if_equal(self):
        component = ComponentRenderingMocks()
        component.mount()
        assert () == tuple(component.diff())

    def test_diff_render_with_temporary_attributes(self):
        class MyTestComponent(Component):
            def __init__(self):
                super().__init__()
                self.rendered = ComponentMock()
                self.rendering_attributes = None

            def render(self):
                self.rendering_attributes = self.attributes

        component = MyTestComponent()
        tuple(component.diff(a=True))
        assert {"a": True} == component.rendering_attributes
        assert {} == component.attributes


class TestSetRendering:
    def test_apply_set_rendering_of_component(self):
        rendering = ComponentRenderingMocks()
        component = ComponentRenderingMocks()
        patch = SetRendering(component, rendering)

        patch.apply()

        assert rendering == component.rendered
