"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable

from .attributes import Attribute, NamedAttribute
from .structure import Structure, StructureDefinition


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            attribute_dict = attribute.asdict()
            attribute_dict.update(name=attribute_name)
            yield NamedAttribute(**attribute_dict)


class Blueprint:
    """A Blueprint initialized as described with Attributes"""
    AttributeDefinitions: Tuple[NamedAttribute, ...] = ()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.AttributeDefinitions = tuple(_attributes_of_namespace(cls.__dict__))

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.structure: Structure = Structure()
        for named_attribute in self.AttributeDefinitions:
            setattr(
                self, named_attribute.name,
                named_attribute.extract_value(*args, **kwargs)
            )

    def __eq__(self, other: Any) -> bool:
        if type(other) != type(self):  # pylint: disable=unidiomatic-typecheck
            return False
        for attribute in self.AttributeDefinitions:
            if getattr(self, attribute.name) != getattr(other, attribute.name):
                return False
        return True

    # pylint: disable=no-self-use
    def structure_definition(self) -> StructureDefinition:
        """Returns a definition to rebuild the structure"""
        return None

    def update(self, target: "Blueprint") -> None:
        """Updates self to match another Blueprint"""
        self._update_attributes(target)
        target_structure = Structure(target.structure_definition())
        compareables = (
            (key, self.structure.get(key), target_structure.get(key))
            for key in set(self.structure.keys()) | set(target_structure.keys())
        )
        for key, old, new in compareables:
            if new is None:
                del self.structure[key]
            elif old is None:
                self.structure[key] = new
            elif type(old) != type(new):  # pylint: disable=unidiomatic-typecheck
                del self.structure[key]
                self.structure[key] = new

    def _update_attributes(self, target: "Blueprint") -> None:
        for attribute_definition in self.AttributeDefinitions:
            setattr(self, attribute_definition.name,
                    getattr(target, attribute_definition.name))
