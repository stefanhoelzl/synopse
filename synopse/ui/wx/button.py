import wx

from synopse.core.attributes import Attribute
from synopse.utils.attributes import StrAttribute, TupleAttribute

from .base import WxComponent, WxProperty, WxEventHandler


class WxButtonEventHandler(WxEventHandler):
    Event = wx.EVT_BUTTON


class WxLabelProperty(WxProperty):
    PropertyName = "Label"
    value = StrAttribute()[0]


class WxPositionProperty(WxProperty):
    PropertyName = "Position"
    value = TupleAttribute()[0]


class WxButton(WxComponent):
    label = Attribute(constructor=WxLabelProperty)
    position = Attribute(constructor=WxPositionProperty)
    button = Attribute(constructor=WxButtonEventHandler)

    def create(self, index):
        return wx.Button(index.host.wx)
