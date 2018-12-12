import wx

from synopse.core import Attribute
from .base import WxComponent


class WxApp(WxComponent):
    children = Attribute()[:]

    def create(self, index):
        return wx.App()

    def start(self):
        self.mount()
        self.wx.MainLoop()
