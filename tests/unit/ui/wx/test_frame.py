from unittest.mock import patch, MagicMock

import pytest

from synopse.ui.wx.frame import WxFrame


@pytest.fixture
def frame():
    frame = WxFrame()
    frame.wx = MagicMock()
    frame.create = MagicMock()
    return frame


class TestWxApp:
    def test_create_app(self):
        frame = WxFrame()
        with patch("synopse.ui.wx.frame.wx.Frame", return_value="frame") as fm:
            assert "frame" == frame.create(None)
        fm.assert_called_once()

    def test_mount_show(self, frame):
        frame.mount(None)
        frame.wx.Show.assert_called_once()
