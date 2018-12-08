from unittest.mock import MagicMock

from synopse.component import Component, Index
from synopse.reconcile import reconcile


class TestReconcile:
    def test_if_new_is_none_unmount_old(self, index, component):
        component.unmount = MagicMock()
        assert reconcile(index, component, None) is None
        component.unmount.assert_called_once()

    def test_if_old_is_none_mount_new(self, index, component):
        component.mount = MagicMock()
        assert component == reconcile(index, None, component)
        component.mount.assert_called_once_with(index)

    def test_on_different_types_unmount_old_mount_new(
            self, index, create_component_class):
        old = create_component_class()()
        old.unmount = MagicMock()
        old.index = index
        new = create_component_class()()
        new.mount = MagicMock()
        assert new == reconcile(Index(None, "key", 0), old, new)
        new.mount.assert_called_once_with(index)
        old.unmount.assert_called_once()

    def test_if_neq_update_old(self, index):
        old = Component()
        old.update = MagicMock()
        new = Component()
        new.attributes = {"attr": True}
        assert old == reconcile(index, old, new)
        old.update.assert_called_once_with(new.attributes)

    def test_if_eq_no_update(self, index):
        old = Component()
        old.update = MagicMock()
        new = Component()
        assert old == reconcile(index, old, new)
        old.update.assert_not_called()
