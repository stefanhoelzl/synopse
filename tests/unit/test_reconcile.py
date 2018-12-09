from unittest.mock import MagicMock, patch

from synopse.component import Component, Index
from synopse.reconcile import reconcile, reconcile_dict


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


class TestReconcileDict:
    def test_mount_new_key(self, component):
        new = Component()
        new.mount = MagicMock()
        assert {"k": new} == reconcile_dict(component, {}, {"k": new})
        new.mount.assert_called_once_with(Index(component, "k", None))

    def test_reconcile_existing_key(self, component):
        new = Component()
        old = Component()
        with patch("synopse.reconcile.reconcile") as mock:
            mock.return_value = "reconciled"
            assert {"k": "reconciled"} == reconcile_dict(
                component, {"k": old}, {"k": new}
            )
        mock.assert_called_once_with(old, new)

    def test_unmount_unused_old_key(self, component):
        old = Component()
        old.unmount = MagicMock()
        assert {} == reconcile_dict(component, {"k": old}, {})
        old.unmount.assert_called_once()
