"""Everything needed to build a Component class"""
from typing import Any, Tuple, Dict, Iterable

from .attributes import Attribute, NamedAttribute


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            attribute_dict = attribute.asdict()
            attribute_dict.update(name=attribute_name)
            yield NamedAttribute(**attribute_dict)


class BaseComponent:
    """A Component initialized as described with Attributes"""
    AttributeDefinitions: Tuple[NamedAttribute, ...] = ()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.AttributeDefinitions = tuple(_attributes_of_namespace(cls.__dict__))

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for named_attribute in self.AttributeDefinitions:
            setattr(
                self, named_attribute.name,
                named_attribute.extract_value(*args, **kwargs)
            )

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        for attribute in self.AttributeDefinitions:
            if getattr(self, attribute.name) != getattr(other, attribute.name):
                return False
        return True

    @property
    def host(self) -> Any:
        """Host component"""
        raise NotImplementedError()

    def create(self) -> "BaseComponent":
        """Lifecycle method called when component is created"""
        raise NotImplementedError()

    def destroy(self) -> None:
        """Lifecycle method called when component gets destroyed"""
        raise NotImplementedError()

    def update(self, target: "BaseComponent") -> None:
        """Updates self to match another Component"""
        for attribute_definition in self.AttributeDefinitions:
            self.update_attribute(attribute_definition.name,
                                  getattr(target, attribute_definition.name))

    def update_attribute(self, name: str, value: Any) -> None:
        """Updates a single attribute"""
        setattr(self, name, value)
