from unittest.mock import patch, MagicMock

import pytest

from synopse.ui.wx.app import WxApp


@pytest.fixture
def app():
    app = WxApp()
    app.wx = MagicMock()
    app.create = MagicMock()
    return app


class TestWxApp:
    def test_create_app(self):
        app = WxApp()
        with patch("synopse.ui.wx.app.wx.App", return_value="app") as app_mock:
            assert "app" == app.create(None)
        app_mock.assert_called_once()

    def test_start_mount(self, app):
        app.mount = MagicMock()
        app.start()
        app.mount.assert_called_once()

    def test_start_mainloop(self, app):
        app.start()
        app.wx.MainLoop.assert_called_once()
