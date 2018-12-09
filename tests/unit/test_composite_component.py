from unittest.mock import MagicMock, patch


class TestCompositeComponent:
    def test_mount_calls_and_returns_content_mount(
            self, composite_component, index):
        mock = MagicMock()
        composite_component.layout = MagicMock(return_value=mock)
        composite_component.mount(index)
        mock.mount.assert_called_once()

    def test_unmount_calls_content_unmount(self, composite_component):
        mock = MagicMock()
        composite_component.content = mock
        composite_component.unmount()
        mock.unmount.assert_called_once()

    def test_update_reconciles_content(self, index, composite_component):
        composite_component.index = index
        composite_component.content = "OLD"
        composite_component.layout = MagicMock(return_value="NEW")
        with patch("synopse.composite_component.reconcile_components",
                   return_value="RECONCILED") as reconcile:
            composite_component.update()
        assert "RECONCILED" == composite_component.content
        reconcile.assert_called_once_with("OLD", "NEW")
