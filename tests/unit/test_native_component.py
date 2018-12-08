from unittest.mock import MagicMock, patch

from synopse.component import Index
from synopse.native_component import NativeComponent


class TestNativeComponent:
    def test_layout_returns_attributes(self):
        component = NativeComponent()
        component.attributes = {"a": 1}
        assert component.attributes == component.layout()

    def test_mount_children(self):
        component = NativeComponent()
        component.insert = MagicMock()
        component.layout = MagicMock(
            return_value={"k": NativeComponent(), "p": [NativeComponent()]}
        )
        component.mount()
        assert Index(component, "k", None) == component.content["k"].index
        assert Index(component, "p", 0) == component.content["p"][0].index

    def test_insert_if_index_provided(self):
        mock_host = MagicMock()
        component = NativeComponent()
        component.mount(Index(mock_host, "k", 1))
        mock_host.insert.assert_called_once_with("k", 1, component)

    def test_unmount_children(self):
        component = NativeComponent()
        component.remove = MagicMock()
        key_child, pos_child = MagicMock(), MagicMock()
        component.content = {"k": key_child, "p": [pos_child]}
        component.unmount()
        key_child.unmount.assert_called_once()
        pos_child.unmount.assert_called_once()

    def test_remove_if_index_provided(self):
        mock_host = MagicMock()
        component = NativeComponent()
        component.content = {}
        component.index = Index(mock_host, "k", 1)
        component.unmount()
        mock_host.remove.assert_called_once_with("k", 1, component)

    def test_update_reconciles_content(self):
        component = NativeComponent()
        component.content = {"o": "OLD"}
        component.layout = MagicMock(return_value={"n": "NEW"})
        with patch("synopse.native_component.reconcile_dict") as reconcile:
            component.update()
        reconcile.assert_called_once_with(component, {"o": "OLD"}, {"n": "NEW"})
