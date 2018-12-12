from typing import Any, Callable

from synopse.core.component import Component
from synopse.core.attributes import Attribute


class Event:
    def __init__(self, name: str, emitter: "Component") -> None:
        self.name = name
        self.emitter = emitter


class EventHandler(Attribute):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            validator=lambda eh: eh is None or callable(eh),
            **kwargs
        )

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def getter(name: str) -> Callable[[Any], None]:
        def wrapper(self: Component, *args: Any, **kwargs: Any) -> None:
            if self.attributes[name] is not None:
                self.attributes[name](Event(name, self), *args, **kwargs)
        return wrapper
