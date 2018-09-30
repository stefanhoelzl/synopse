"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable
from .typing import KwAttrs, PosAttrs

from .attributes import Attribute, NamedAttribute


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            attribute_dict = attribute.asdict()
            attribute_dict.update(name=attribute_name)
            yield NamedAttribute(**attribute_dict)


class Blueprint:
    """A Blueprint describes the structure of an unit"""
    AttributeDefinitions: Tuple[NamedAttribute, ...] = ()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.AttributeDefinitions = tuple(_attributes_of_namespace(cls.__dict__))

    def __init__(self, *posattrs: PosAttrs, **kwattrs: KwAttrs) -> None:
        for named_attribute in self.AttributeDefinitions:
            setattr(
                self, named_attribute.name,
                named_attribute.extract_value(posattrs, kwattrs)
            )
