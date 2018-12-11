import wx

from .base import WxComponent


class WxApp(WxComponent):
    def create(self, index):
        return wx.App()

    def start(self):
        self.mount()
        self.wx.MainLoop()
