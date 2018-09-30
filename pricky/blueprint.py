"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable, Union

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
        self.current_structure: Dict[Key, "StructuredBlueprint"] = {}

    def structure(self) -> None:  # pylint: disable=no-self-use
        """Re-builds the structure with the current state"""
        return None


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
