"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable

from .attributes import Attribute
from .errors import RequiredAttributeMissing, AttributeValidationFailed


KW_ATTRS = Dict[str, Any]


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[Tuple[str, Attribute]]:
    """Extracts the Attributes out of an namespace dict

    Args:
        namespace: namespace dict of an class

    Returns:
        yields every Attribute in the namespace
    """
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            yield attribute_name, attribute


class _Blueprint:
    """A Blueprint describes the structure of an unit"""
    AttributeDefinitions: Dict[str, Attribute] = {}

    def __init__(self, **kwattrs: KW_ATTRS) -> None:
        for attribute_name, attribute in self.AttributeDefinitions.items():
            attribute_value = self._check_attribute(attribute,
                                                    attribute_name,
                                                    kwattrs)
            setattr(self, attribute_name, attribute_value)

    def _check_attribute(
            self, attribute: Attribute, name: str, kwattrs: KW_ATTRS) -> Any:
        value = kwattrs.get(name, attribute.default)
        self._check_attribute_required(attribute, name, kwattrs)
        self._check_attribute_validation(attribute, name, value)
        return value

    def _check_attribute_required(
            self, attribute: Attribute, name: str, kwattrs: KW_ATTRS) -> None:
        if attribute.required and name not in kwattrs:
            raise RequiredAttributeMissing(name, type(self))

    def _check_attribute_validation(
            self, attribute: Attribute, name: str, value: Any) -> None:
        if attribute.validator and attribute.validator(value) is False:
            raise AttributeValidationFailed(name, value, type(self))


def blueprint(name: str,
              bases: Tuple[type, ...],
              namespace: Dict[str, Any]) -> type:
    """metaclass to create a Blueprint"""
    namespace.update(
        AttributeDefinitions={
            name: definition
            for name, definition in _attributes_of_namespace(namespace)},
    )
    return type(name, (*bases, _Blueprint), namespace)
