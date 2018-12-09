from unittest.mock import MagicMock, patch

from synopse.component import Component, Index
from synopse.reconcile import reconcile, \
    reconcile_components, reconcile_dicts, reconcile_list


reconcile_components_fn = "synopse.reconcile.reconcile_components"


class TestReconcileComponents:
    def test_on_different_types_unmount_old_mount_new(
            self, index, create_component_class):
        old = create_component_class()()
        old.unmount = MagicMock()
        old.index = index
        new = create_component_class()()
        new.mount = MagicMock()
        assert new == reconcile_components(old, new)
        new.mount.assert_called_once_with(index)
        old.unmount.assert_called_once()

    def test_if_neq_update_old(self):
        old = Component()
        old.update = MagicMock()
        new = Component()
        new.attributes = {"attr": True}
        assert old == reconcile_components(old, new)
        old.update.assert_called_once_with(new.attributes)

    def test_if_eq_no_update(self):
        old = Component()
        old.update = MagicMock()
        new = Component()
        assert old == reconcile_components(old, new)
        old.update.assert_not_called()


class TestReconcileDicts:
    def test_mount_new_key(self, component):
        new = Component()
        new.mount = MagicMock()
        assert {"k": new} == reconcile_dicts(component, {}, {"k": new})
        new.mount.assert_called_once_with(Index(component, "k", None))

    def test_reconcile_existing_key(self, component):
        new = Component()
        old = Component()
        with patch(reconcile_components_fn, return_value="reconciled") as mock:
            assert {"k": "reconciled"} == reconcile_dicts(
                component, {"k": old}, {"k": new}
            )
        mock.assert_called_once_with(old, new)

    def test_unmount_unused_old_key(self, component):
        old = Component()
        old.unmount = MagicMock()
        assert {} == reconcile_dicts(component, {"k": old}, {})
        old.unmount.assert_called_once()


class TestReconcileList:
    def test_mount_if_only_in_new(self, component):
        new = Component()
        new.mount = MagicMock()
        assert [new] == reconcile_list(component, "k", [], [new])
        new.mount.assert_called_once_with(Index(component, "k", 0))

    def test_unmount_if_only_in_old(self, component):
        old = Component()
        old.unmount = MagicMock()
        assert [] == reconcile_list(component, "k", [old], [])
        old.unmount.assert_called_once()

    def test_reconcile_if_both(self, component):
        old, new = Component(), Component()
        with patch(reconcile_components_fn, return_value="reconciled") as mock:
            assert ["reconciled"] == reconcile_list(
                component, "k", [old], [new]
            )
        mock.assert_called_once_with(old, new)
