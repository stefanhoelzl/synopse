"""Everything needed to build a Component class"""
from typing import Any, Tuple, Dict, Iterable, List

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
    ChildrenContainer: List["BaseComponent"] = []

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

    # pylint: disable=no-self-use
    def render(self) -> "BaseComponent":
        """Returns a Component"""
        raise NotImplementedError()

    def create(self) -> Any:
        raise NotImplementedError()

    def destroy(self) -> None:
        raise NotImplementedError()

    def update(self, target: "BaseComponent") -> None:
        """Updates self to match another Component"""
        for attribute_definition in self.AttributeDefinitions:
            setattr(self, attribute_definition.name,
                    getattr(target, attribute_definition.name))
