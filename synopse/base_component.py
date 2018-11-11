"""Everything needed to build a Component class"""
from typing import Any, List, Dict, Iterable, Optional
from collections import namedtuple
from dataclasses import dataclass

from .attributes import Attribute, NamedAttribute


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            attribute_dict = attribute.asdict()
            attribute_dict.update(name=attribute_name)
            yield NamedAttribute(**attribute_dict)


def _attribute_property(name: str) -> property:
    def wrapper(self: "BaseComponent") -> Any:
        return self.attributes[name]
    return property(wrapper)


Index = namedtuple("Index", "host, slot, position")


class Patch:
    """Base class for patch"""
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


class BaseComponent:
    """A Component initialized as described with Attributes"""
    AttributeDefinitions: List[NamedAttribute] = []

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        definitions = []
        for attribute in _attributes_of_namespace(cls.__dict__):
            definitions.append(attribute)
            setattr(cls, attribute.name, _attribute_property(attribute.name))
        cls.AttributeDefinitions = cls.AttributeDefinitions + definitions

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.index: Optional[Index] = None
        self.attributes: Dict[str, Any] = {}

        for named_attribute in self.AttributeDefinitions:
            self.attributes[named_attribute.name] = \
                named_attribute.extract_value(*args, **kwargs)

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return bool(self.attributes == other.attributes)

    @property
    def native(self) -> Any:
        """Native component"""
        raise NotImplementedError()

    def mount(self) -> "BaseComponent":
        """Lifecycle method called when component is created"""
        raise NotImplementedError()

    def unmount(self) -> None:
        """Lifecycle method called when component gets destroyed"""
        raise NotImplementedError()

    def diff(self, **attributes: Any) -> Iterable[Patch]:
        """Yields difference as patches"""
        for attr_name, attr_value in attributes.items():
            if self.attributes.get(attr_name) != attr_value:
                yield from self.diff_attribute(attr_name, attr_value)

    def diff_attribute(self, name: str, value: Any) -> Iterable[Patch]:
        """Yields difference as patches"""
        yield SetAttribute(self, name, value)

    def update(self, **attributes: Any) -> None:
        """Updates a component"""
        for patch in self.diff(**attributes):
            patch.apply()
