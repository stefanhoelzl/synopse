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
        self.structure_instance: Structure = Structure()
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
        self._update_structure(Structure(self.structure()))

    def _update_attributes(self, target: "Component") -> None:
        for attribute_definition in self.AttributeDefinitions:
            setattr(self, attribute_definition.name,
                    getattr(target, attribute_definition.name))

    def _update_structure(self, desired_structure: Structure) -> None:
        key_offset = 0
        for key in self.structure_instance.keys() | desired_structure.keys():
            new = desired_structure[key]
            key = key - key_offset if isinstance(key, int) else key
            old = self.structure_instance[key]

            if new is None:
                del self.structure_instance[key]
                key_offset += 1 if isinstance(key, int) else 0
            elif old is None:
                self.structure_instance[key] = new
            elif old.__class__ != new.__class__:
                del self.structure_instance[key]
                self.structure_instance[key] = new
            elif old != new:
                old.update(new)