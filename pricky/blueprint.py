"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable, Union, Optional, cast

from .attributes import Attribute, NamedAttribute


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            attribute_dict = attribute.asdict()
            attribute_dict.update(name=attribute_name)
            yield NamedAttribute(**attribute_dict)


Key = Union[int, str]

Structure = Dict[Key, "StructuredBlueprint"]

StructureDefinition = Optional[Union["StructuredBlueprint",
                                     Iterable["StructuredBlueprint"],
                                     Structure]]


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
        self.current_structure: Structure = {}

    # pylint: disable=no-self-use
    def structure_definition(self) -> StructureDefinition:
        """Returns a definition to rebuild the structure"""
        return None

    def rebuild_structure(self) -> Structure:
        """Re-builds the structure with the current state"""
        structure_defintion = self.structure_definition()
        if isinstance(structure_defintion, dict):
            return structure_defintion
        elif isinstance(structure_defintion, StructuredBlueprint):
            return {0: structure_defintion}
        elif isinstance(structure_defintion, Iterable):
            # WORKAROUND: mypy bug with inferencing type of enumeration
            # MYPY-230:  https://github.com/python/mypy/issues/230
            # MYPY-5579: https://github.com/python/mypy/issues/5579
            typed_enumeration = cast(Iterable[Tuple[int, StructuredBlueprint]],
                                     enumerate(structure_defintion))
            return {key: blueprint for key, blueprint in typed_enumeration}
        return {}


class ChangeableBlueprint(StructuredBlueprint):
    """A Blueprint that can be changed"""
    def __setitem__(self, key: Key, child: StructuredBlueprint) -> None:
        """Inserts a Item"""
        pass

    def move_item(self, old: Key, new: Key) -> None:
        """Moves a item from one place to another"""
        pass

    def __delitem__(self, key: Key) -> None:
        """Deletes a item"""
        pass


class UpdateableBlueprint(ChangeableBlueprint):
    """A Blueprint that can be updated"""
    def update(self, target: StructuredBlueprint) -> None:
        """Updates self to match another Blueprint"""
        pass


class Blueprint(UpdateableBlueprint):
    """A Blueprint"""
