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


class BlueprintDescription:
    """A Blueprint initialized as described with Attributes"""
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


class StructuredBlueprint(BlueprintDescription):
    """A Blueprint holding a structure"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.structure: Structure = Structure()

    # pylint: disable=no-self-use
    def structure_definition(self) -> StructureDefinition:
        """Returns a definition to rebuild the structure"""
        return None


class UpdateableBlueprint(StructuredBlueprint):
    """A Blueprint that can be updated"""
    def update(self, target: StructuredBlueprint) -> None:
        """Updates self to match another Blueprint"""
        self._update_attributes(target)

    def _update_attributes(self, target: BlueprintDescription) -> None:
        for attribute_definition in self.AttributeDefinitions:
            setattr(self, attribute_definition.name,
                    getattr(target, attribute_definition.name))


class Blueprint(UpdateableBlueprint):
    """A Blueprint"""
