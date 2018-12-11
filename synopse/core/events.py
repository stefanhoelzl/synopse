from typing import Any, Callable

from synopse.core.component import Component
from synopse.core.attributes import Attribute


class Event:
    def __init__(self, name: str, emitter: "Component") -> None:
        self.name = name
        self.emitter = emitter


class EventAttribute(Attribute):
    @staticmethod
    def getter(name: str) -> Callable[[Any], None]:
        def wrapper(self: Component, **kwargs: Any) -> None:
            self.attributes[name](Event(name, self), **kwargs)
        return wrapper
