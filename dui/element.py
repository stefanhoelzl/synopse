"""Elements represent the lowest UI entities"""
from typing import Any


class Element:
    """A Element represents a simple UI entity by its type and properties"""
    def __init__(self, **properties: Any) -> None:
        self.__properties__ = properties
