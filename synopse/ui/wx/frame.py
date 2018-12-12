import wx

from synopse.core import Attribute

from .base import WxComponent


class WxFrame(WxComponent):
    children = Attribute()[:]

    def create(self, index):
        return wx.Frame(None)

    def mount(self, index=None):
        super().mount(index)
        self.wx.Show()
