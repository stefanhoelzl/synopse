"""Everything needed to build a Component class"""
import typing
from typing import Any, Dict, Iterator, Tuple, Optional, NamedTuple
from abc import ABC, abstractmethod
from contextlib import contextmanager
from collections import ChainMap

from .attributes import Attribute, Attributes, extract_values


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterator[Tuple[str, Attribute]]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            yield attribute_name, attribute


def _attribute_property(name: str) -> property:
    def wrapper(self: "Component") -> Any:
        return self.attributes[name]
    return property(wrapper)


@contextmanager
def temporary_attributes(component: "Component", attributes: Attributes) \
        -> Iterator[None]:
    """Sets temporary attributes for a component"""
    backup = component.attributes
    component.attributes = attributes
    yield
    component.attributes = backup


class Component(ABC):
    """A Component initialized as described with Attributes"""
    Attributes: typing.ChainMap[str, Attribute] = ChainMap()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        attributes = {}
        for name, attribute in _attributes_of_namespace(cls.__dict__):
            attributes[name] = attribute
            setattr(cls, name, _attribute_property(name))
        cls.Attributes = cls.Attributes.new_child(attributes)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.attributes = extract_values(self.Attributes, *args, **kwargs)

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return bool(self.attributes == other.attributes)

    def mount(self) -> None:
        """Lifecycle method called when component is created"""
        pass

    def unmount(self) -> None:
        """Lifecycle method called when component gets destroyed"""
        pass

    @abstractmethod
    def layout(self) -> None:
        """Describes the layout of the component"""
        raise NotImplementedError()


class Index(NamedTuple):
    """Index used to localize a subcomponent"""
    key: str
    position: Optional[int]


class NativeComponent(Component, ABC):
    """Native Component"""
    @abstractmethod
    def insert(self,
               component: "NativeComponent",
               index: Optional[Index] = None) -> None:
        """TODO"""
        raise NotImplementedError()

    @abstractmethod
    def replace(self, index: Index, component: "NativeComponent") -> None:
        """TODO"""
        raise NotImplementedError()

    @abstractmethod
    def remove(self, index: Index) -> None:
        """TODO"""
        raise NotImplementedError()
