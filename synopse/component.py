"""Everything needed to build a Component class"""
from typing import Any, Tuple, Dict, Iterable, Optional

from .attributes import Attribute, NamedAttribute
from .lifecycle import Lifecycle
from .structure import Structure, Definition


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            attribute_dict = attribute.asdict()
            attribute_dict.update(name=attribute_name)
            yield NamedAttribute(**attribute_dict)


class Component(Lifecycle):
    """A Component initialized as described with Attributes"""
    AttributeDefinitions: Tuple[NamedAttribute, ...] = ()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.AttributeDefinitions = tuple(_attributes_of_namespace(cls.__dict__))

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.structure_instance = Structure()
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
    def structure(self) -> Definition:
        """Returns a definition to rebuild the structure"""
        return None

    def update(self, target: Optional["Component"] = None) -> None:
        """Updates self to match another Component"""
        if target is not None:
            self._update_attributes(target)
        self.structure_instance.update(Structure(self.structure()))

    def _update_attributes(self, target: "Component") -> None:
        for attribute_definition in self.AttributeDefinitions:
            setattr(self, attribute_definition.name,
                    getattr(target, attribute_definition.name))
