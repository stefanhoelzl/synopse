from unittest.mock import MagicMock, patch

from synopse.core.component import Index
from synopse.core.native_component import NativeComponent


ReconcileDictFn = "synopse.core.native_component.reconcile_dicts"


class TestNativeComponent:
    def test_layout_returns_attributes(self):
        component = NativeComponent()
        component.attributes = {"a": 1}
        assert component.attributes == component.layout()

    def test_mount_children(self):
        component = NativeComponent()
        component.layout = MagicMock(
            return_value={"k": NativeComponent(), "p": [NativeComponent()]}
        )
        component.mount()
        assert Index(component, "k", None) == component.content["k"].index
        assert Index(component, "p", 0) == component.content["p"][0].index

    def test_unmount_children(self):
        component = NativeComponent()
        key_child, pos_child = MagicMock(), MagicMock()
        component.content = {"k": key_child, "p": [pos_child]}
        component.unmount()
        key_child.unmount.assert_called_once()
        pos_child.unmount.assert_called_once()

    def test_update_reconciles_content(self):
        component = NativeComponent()
        component.content = {"o": "OLD"}
        component.layout = MagicMock(return_value={"n": "NEW"})
        with patch(ReconcileDictFn) as reconcile:
            component.update()
        reconcile.assert_called_once_with(component, {"o": "OLD"}, {"n": "NEW"})
