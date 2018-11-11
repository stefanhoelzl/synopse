"""Everything needed to build a Component class"""
from typing import Any, List, Dict, Iterable

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
        self.attributes: Dict[str, Any] = {}

        for named_attribute in self.AttributeDefinitions:
            self.attributes[named_attribute.name] = \
                named_attribute.extract_value(*args, **kwargs)

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return bool(self.attributes == other.attributes)

    @property
    def host(self) -> Any:
        """Host component"""
        raise NotImplementedError()

    def mount(self) -> "BaseComponent":
        """Lifecycle method called when component is created"""
        raise NotImplementedError()

    def unmount(self) -> None:
        """Lifecycle method called when component gets destroyed"""
        raise NotImplementedError()
