"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable
from pricky.typing import KwAttrs, PosAttrs

from .attributes import Attribute, NamedAttribute


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Extracts the Attributes out of an namespace dict

    Args:
        namespace: namespace dict of an class

    Returns:
        yields every Attribute in the namespace as a NamedAttribute
    """
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            attribute_dict = attribute.asdict()
            attribute_dict.update(name=attribute_name)
            yield NamedAttribute(**attribute_dict)


class Blueprint:
    """A Blueprint describes the structure of an unit"""
    AttributeDefinitions: Tuple[NamedAttribute, ...] = ()

    def __init__(self, *posattrs: PosAttrs, **kwattrs: KwAttrs) -> None:
        for named_attribute in self.AttributeDefinitions:
            setattr(
                self, named_attribute.name,
                named_attribute.extract_value(posattrs, kwattrs)
            )


def blueprint(name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) \
        -> type:
    """metaclass to create a Blueprint"""
    namespace.update(
        AttributeDefinitions=tuple(_attributes_of_namespace(namespace)),
    )
    return type(name, (*bases, Blueprint), namespace)
