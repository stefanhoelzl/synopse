from unittest.mock import MagicMock, patch

from synopse.core.component import Component, Index
from synopse.core.reconcile import reconcile, \
    reconcile_components, reconcile_dicts, reconcile_list


ReconcileComponentsFn = "synopse.core.reconcile.reconcile_components"
ReconcileListFn = "synopse.core.reconcile.reconcile_list"


class TestReconcile:
    def test_old_is_none_mount_new_component(self, component):
        new = Component()
        new.mount = MagicMock()
        assert new == reconcile(component, "k", 0, None, new)
        new.mount.assert_called_once_with(Index(component, "k", 0))

    def test_old_is_none_mount_list(self, component):
        new = [Component(), Component()]
        with patch(ReconcileListFn, return_value="reconciled") as mock:
            assert "reconciled" == reconcile(component, "k", None, None, new)
        mock.assert_called_once_with(component, "k", [], new)

    def test_new_is_none_unmount_old_component(self, component):
        old = Component()
        old.unmount = MagicMock()
        assert reconcile(component, "k", 0, old, None) is None
        old.unmount.assert_called_once()

    def test_new_is_none_unmount_old_list(self, component):
        old = [Component(), Component()]
        with patch(ReconcileListFn, return_value="reconciled") as mock:
            assert "reconciled" == reconcile(component, "k", None, old, None)
        mock.assert_called_once_with(component, "k", old, [])

    def test_old_list_new_not_unmount_old_mount_new(self, component):
        old_0, old_1 = Component(), Component()
        old = [old_0, old_1]
        new = Component()
        new.mount = MagicMock()
        old_0.unmount = MagicMock()
        old_1.unmount = MagicMock()
        assert new == reconcile(component, "k", 0, old, new)
        new.mount.assert_called_once_with(Index(component, "k", None))
        old_0.unmount.assert_called_once()
        old_1.unmount.assert_called_once()

    def test_reconcile_lists(self, component):
        with patch(ReconcileListFn, return_value="reconciled") as mock:
            assert "reconciled" == reconcile(component, "k", None, [], [])
        mock.assert_called_once_with(component, "k", [], [])

    def test_reconcile_components(self, component):
        new, old = Component(), Component()
        with patch(ReconcileComponentsFn, return_value="reconciled") as mock:
            assert "reconciled" == reconcile(component, "k", None, old, new)
        mock.assert_called_once_with(old, new)


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
        with patch(ReconcileComponentsFn, return_value="reconciled") as mock:
            assert {"k": "reconciled"} == reconcile_dicts(
                component, {"k": old}, {"k": new}
            )
        mock.assert_called_once_with(old, new)

    def test_unmount_unused_old_key(self, component):
        old = Component()
        old.unmount = MagicMock()
        assert {} == reconcile_dicts(component, {"k": old}, {})
        old.unmount.assert_called_once()

    def test_unmount_unused_old_list(self, component):
        old0, old1 = Component(), Component()
        old0.unmount = MagicMock()
        old1.unmount = MagicMock()
        assert {} == reconcile_dicts(component, {"k": [old0, old1]}, {})
        old0.unmount.assert_called_once()
        old1.unmount.assert_called_once()


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
        with patch(ReconcileComponentsFn, return_value="reconciled") as mock:
            assert ["reconciled"] == reconcile_list(
                component, "k", [old], [new]
            )
        mock.assert_called_once_with(old, new)
