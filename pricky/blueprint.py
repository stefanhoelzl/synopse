"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable

from .attributes import Attribute
from .errors import RequiredAttributeMissing, AttributeValidationFailed


KwAttrs = Dict[str, Any]


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

    def __init__(self, **kwattrs: KwAttrs) -> None:
        for attribute in self.AttributeDefinitions:
            attribute_value = self._check_attribute(attribute, kwattrs)
            setattr(self, attribute.item, attribute_value)

    def _check_attribute(
            self, attribute: Attribute, kwattrs: KwAttrs) -> Any:
        value = kwattrs.get(attribute.item, attribute.default)
        self._check_attribute_required(attribute, kwattrs)
        self._check_attribute_validation(attribute, value)
        return value

    def _check_attribute_required(
            self, attribute: Attribute, kwattrs: KwAttrs) -> None:
        if attribute.required and attribute.item not in kwattrs:
            raise RequiredAttributeMissing(attribute.item,
                                           type(self))

    def _check_attribute_validation(
            self, attribute: Attribute, value: Any) -> None:
        if attribute.validator and attribute.validator(value) is False:
            raise AttributeValidationFailed(
                attribute.item, value, type(self))


def blueprint(name: str,
              bases: Tuple[type, ...],
              namespace: Dict[str, Any]) -> type:
    """metaclass to create a Blueprint"""
    namespace.update(
        AttributeDefinitions=tuple(_attributes_of_namespace(namespace)),
    )
    return type(name, (*bases, _Blueprint), namespace)
