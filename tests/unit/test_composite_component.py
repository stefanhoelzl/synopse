from unittest import mock

from synopse import CompositeComponent
from synopse.composite_component import IndexedComponent, \
    CompositeComponentDiff, SetComponent


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


class CompositeComponentDescribingMocks(CompositeComponent):
    def __init__(self, components=None):
        super().__init__()
        self.components = components if components else ComponentMock()

    def describe(self):
        if isinstance(self.components, list):
            return self.components.pop(0)
        return self.components


class TestComponent:
    def test_native_from_component(self):
        component = CompositeComponentDescribingMocks()
        component.mount()
        assert "native" == component.native

    def test_mount_set_component(self):
        component = CompositeComponentDescribingMocks()
        component.mount()
        assert component.components == component.component

    def test_mount_recursive(self):
        component = CompositeComponentDescribingMocks()
        component.mount()
        assert "mounted" == component.components.state

    def test_unmount_recursive(self):
        component = CompositeComponentDescribingMocks()
        component.mount()
        component.unmount()
        assert "unmounted" == component.components.state

    def test_unmount_set_component_to_none(self):
        component = CompositeComponentDescribingMocks()
        component.mount()
        component.unmount()
        assert component.component is None

    def test_diff_describe_with_temporary_attributes(self):
        class MyTestCompositeComponent(CompositeComponent):
            def __init__(self):
                super().__init__()
                self.component = ComponentMock()
                self.component_attributes = None

            def describe(self):
                self.component_attributes = self.attributes

        component = MyTestCompositeComponent()
        tuple(component.diff(a=True))
        assert {"a": True} == component.component_attributes
        assert {} == component.attributes


class TestCompositeComponentDiff:
    def test_set_component_when_class_changed(self):
        changed = mock.MagicMock()
        composite = mock.MagicMock()
        expected = SetComponent(composite, changed)
        assert expected == \
               tuple(CompositeComponentDiff(composite, changed))[-1]


class TestSetcomponent:
    def test_apply_set_component_of_component(self):
        composite = CompositeComponentDescribingMocks()
        component = CompositeComponentDescribingMocks()
        patch = SetComponent(composite, component)

        patch.apply()

        assert component == composite.component
