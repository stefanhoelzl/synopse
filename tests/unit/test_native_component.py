from unittest import mock

from synopse.native_component import ComponentDiff, Replace


class TestComponentDiff:
    def test_replace_when_different_classes(self):
        original = mock.MagicMock()
        changed = mock.MagicMock()
        expected = (Replace(original, changed),)
        assert expected == tuple(ComponentDiff(original, changed))

    def test_yield_from_component_diff_when_same_class_but_not_equal(self):
        component = mock.MagicMock()
        component.diff = lambda **a: [1, 2]
        component.__eq__ = lambda s, o: False
        assert (1, 2) == tuple(ComponentDiff(component, component))

    def test_diff_nothing_if_equal(self):
        component = object()
        assert () == tuple(ComponentDiff(component, component))
