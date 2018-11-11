"""Everything needed to build a Component class"""
from typing import Any, Dict, Iterator, Tuple
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass

from .attributes import Attribute, extract_values


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterator[Tuple[str, Attribute]]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            yield attribute_name, attribute


def _attribute_property(name: str) -> property:
    def wrapper(self: "BaseComponent") -> Any:
        return self.attributes[name]
    return property(wrapper)


Attributes = Dict[str, Any]


@contextmanager
def temporary_attributes(component: "BaseComponent", attributes: Attributes) \
        -> Iterator[None]:
    """Sets temporary attributes for a component"""
    backup = component.attributes
    component.attributes = attributes
    yield
    component.attributes = backup


class Patch(ABC):
    """Base class for patch"""
    @abstractmethod
    def apply(self) -> None:
        """applies a patch"""
        raise NotImplementedError()


@dataclass
class SetAttribute(Patch):
    """Sets a attribute of a component"""
    component: "BaseComponent"
    name: str
    value: Any

    def apply(self) -> None:
        self.component.attributes[self.name] = self.value


class BaseComponent(ABC):
    """A Component initialized as described with Attributes"""
    Attributes: Dict[str, Attribute] = {}

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        attributes = {}
        for name, attribute in _attributes_of_namespace(cls.__dict__):
            attributes[name] = attribute
            setattr(cls, name, _attribute_property(name))
        cls.Attributes = {**cls.Attributes, **attributes}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.attributes = extract_values(self.Attributes, *args, **kwargs)

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return bool(self.attributes == other.attributes)

    @abstractmethod
    def mount(self) -> None:
        """Lifecycle method called when component is created"""
        raise NotImplementedError()

    @abstractmethod
    def unmount(self) -> None:
        """Lifecycle method called when component gets destroyed"""
        raise NotImplementedError()

    def diff(self, **attributes: Any) -> Iterator[Patch]:
        """Yields difference as patches"""
        for attr_name, attr_value in attributes.items():
            if self.attributes.get(attr_name) != attr_value:
                yield from self.diff_attribute(attr_name, attr_value)

    def diff_attribute(self, name: str, value: Any) -> Iterator[Patch]:
        """Yields difference as patches"""
        yield SetAttribute(self, name, value)

    # pylint: disable=fixme
    # TODO: check when attributes are not complete
    def update(self, **attributes: Any) -> None:
        """Updates a component"""
        for patch in self.diff(**attributes):
            patch.apply()
