from unittest.mock import MagicMock

import pytest

from synopse.ui.wx.base import WxProperty, WxEventHandler, WxComponent


@pytest.fixture
def prop():
    prop = WxProperty(value="value")
    prop.PropertyName = "Prop"
    prop.index = MagicMock()
    return prop


@pytest.fixture
def event_handler():
    event_handler = WxEventHandler(MagicMock())
    event_handler.Event = "Event"
    event_handler.index = MagicMock()
    return event_handler


class TestWxProperty:
    def test_mount_sets_value(self, prop):
        prop.mount(MagicMock())
        prop.index.host.wx.SetProp.assert_called_once_with("value")

    def test_update_sets_value(self, prop):
        prop.update({"value": "updated value"})
        prop.index.host.wx.SetProp.assert_called_once_with("updated value")


class TestWxEventHandler:
    def test_mount_bind_handler(self, event_handler):
        event_handler.mount(MagicMock())
        event_handler.index.host.wx.Bind.assert_called_once()

    def test_update_unbind_bind(self, event_handler):
        event_handler.update()
        event_handler.index.host.wx.Unbind.assert_called_once()
        event_handler.index.host.wx.Bind.assert_called_once()

    def test_unmount_unbind(self, event_handler):
        unbind = event_handler.index.host.wx.Unbind
        event_handler.unmount()
        unbind.assert_called_once()


class TestWxComponent:
    def test_mount(self):
        component = WxComponent()
        component.create = MagicMock()
        component.mount()
        component.create.assert_called_once()

    def test_unmount(self):
        mock = MagicMock()
        component = WxComponent()
        component.wx = mock
        component._content = {}
        component.unmount()
        mock.Destroy.assert_called_once()
        assert component.wx is None
