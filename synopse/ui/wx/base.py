from synopse.core import NativeComponent


class WxComponent(NativeComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wx = None

    def create(self, index):
        raise NotImplementedError()

    def mount(self, index=None):
        self.wx = self.create(index)
        super().mount(index)

    def unmount(self):
        super().unmount()
        self.wx.Destroy()
        self.wx = None
