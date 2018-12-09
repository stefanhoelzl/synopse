"""Everything needed to build a Component class"""
import typing
from typing import Any, Dict, Iterator, Tuple, NamedTuple, Optional, \
    Generic, TypeVar
from collections import ChainMap

from .attributes import Attribute, extract_values


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


ContentType = TypeVar("ContentType")


class Index(NamedTuple):
    """Index used to store the location of a component"""
    host: Any
    key: str
    position: Optional[int]


class Component(Generic[ContentType]):
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
        self.index: Optional[Index] = None
        self._content: Optional[ContentType] = None

    @property
    def content(self) -> ContentType:
        """Guard to assure the component is mounted"""
        if self._content is None:
            raise RuntimeError("Component must be mounted")
        return self._content

    @content.setter
    def content(self, content: Optional[ContentType]) -> None:
        self._content = content

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return bool(self.attributes == other.attributes)

    def mount(self, index: Optional[Index] = None) -> None:
        """Mounts a component"""
        self.index = index
        self._content = self.layout()

    def layout(self) -> ContentType:
        """Describes the layout of the component"""
        raise NotImplementedError()

    def update(self, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Updates a component"""
        if attributes is not None:
            self.attributes = attributes

    def unmount(self) -> None:
        """Unmounts a component"""
        self.index = None
        self._content = None
