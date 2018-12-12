from synopse.core import NativeComponent, Component, Attribute
from synopse.core.events import EventHandler


class WxProperty(Component):
    PropertyName = None
    value = Attribute()

    def _set(self):
        getattr(self.index.host.wx, f"Set{self.PropertyName}")(self.value)

    def mount(self, index=None):
        super().mount(index)
        self._set()

    def update(self, attributes=None):
        super().update(attributes)
        self._set()

    def layout(self):
        return None


class WxEventHandler(Component):
    Event = None

    handler = EventHandler()[0]

    def mount(self, index=None):
        super().mount(index)
        self.index.host.wx.Bind(self.Event, self.handler)

    def update(self, attributes=None):
        self.index.host.wx.Unbind(self.Event)
        super().update(attributes)
        self.index.host.wx.Bind(self.Event, self.handler)

    def unmount(self):
        self.index.host.wx.Unbind(self.Event)
        super().unmount()

    def layout(self):
        return None


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
