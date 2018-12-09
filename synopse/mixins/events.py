import typing
from typing import Any, Callable
from collections import ChainMap

from synopse.helper.capture import capture


class Event:
    def __init__(self, name: str, emitter: "EventMixin") -> None:
        self.name = name
        self.emitter = emitter


class EventAttribute:
    def __call__(self, **kwargs: Any) -> None:
        raise NotImplementedError()


def _action_wrapper(name: str) -> Callable[[Any], None]:
    def wrapper(self: "EventMixin", **kwargs: Any) -> None:
        self.actions[name](Event(name, self), **kwargs)
    return wrapper


class EventMixin:
    Events: typing.ChainMap[str, EventAttribute] = ChainMap()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        capture(cls, "Events", EventAttribute, _action_wrapper)

    def __init__(self, **kwargs: Any) -> None:
        self.actions = {
            name: action
            for name, action in kwargs.items() if name in self.Events
        }
