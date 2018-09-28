"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable

from .attributes import Attribute
from .errors import RequiredAttributeMissing


def _attributes_of_namespace(namespace: Dict[str, Any]) -> Iterable[Attribute]:
    """Extracts the Attributes out of an namespace dict

    Args:
        namespace: namespace dict of an class

    Returns:
        yields every Attribute in the namespace
    """
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            if attribute.item is None:
                attribute.item = attribute_name
            yield attribute


class _Blueprint:
    """A Blueprint describes the structure of an unit"""
    AttributeDefinitions = ()

    def __init__(self: Any, **kwattrs: Dict[str, Any]) -> None:
        for attribute in self.AttributeDefinitions:
            if attribute.required and attribute.item not in kwattrs:
                raise RequiredAttributeMissing(attribute.item,
                                               type(self))
            setattr(self, attribute.item,
                    kwattrs.get(attribute.item, attribute.default))


def blueprint(name: str,
              bases: Tuple[type, ...],
              namespace: Dict[str, Any]) -> type:
    """metaclass to create a Blueprint"""
    namespace.update(
        AttributeDefinitions=tuple(_attributes_of_namespace(namespace)),
    )
    return type(name, (*bases, _Blueprint), namespace)
