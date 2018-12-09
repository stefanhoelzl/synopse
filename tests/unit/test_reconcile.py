from unittest.mock import MagicMock

from synopse.component import Component
from synopse.reconcile import reconcile


class TestReconcile:
    def test_on_different_types_unmount_old_mount_new(
            self, index, create_component_class):
        old = create_component_class()()
        old.unmount = MagicMock()
        old.index = index
        new = create_component_class()()
        new.mount = MagicMock()
        assert new == reconcile(old, new)
        new.mount.assert_called_once_with(index)
        old.unmount.assert_called_once()

    def test_if_neq_update_old(self):
        old = Component()
        old.update = MagicMock()
        new = Component()
        new.attributes = {"attr": True}
        assert old == reconcile(old, new)
        old.update.assert_called_once_with(new.attributes)

    def test_if_eq_no_update(self):
        old = Component()
        old.update = MagicMock()
        new = Component()
        assert old == reconcile(old, new)
        old.update.assert_not_called()
