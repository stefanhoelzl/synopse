"""Everything needed to build a Blueprint class"""
from typing import Any, Tuple, Dict, Iterable

from .attributes import Attribute, NamedAttribute
from .errors import RequiredAttributeMissing, AttributeValidationFailed


KW_ATTRS = Dict[str, Any]
POS_ATTRS = Tuple[Any, ...]


def _attributes_of_namespace(namespace: Dict[str, Any]) \
        -> Iterable[NamedAttribute]:
    """Extracts the Attributes out of an namespace dict

    Args:
        namespace: namespace dict of an class

    Returns:
        yields every Attribute in the namespace
    """
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, Attribute):
            yield NamedAttribute(attribute_name, attribute)


class _Blueprint:
    """A Blueprint describes the structure of an unit"""
    AttributeDefinitions: Tuple[NamedAttribute, ...] = ()

    def __init__(self, *posattrs: POS_ATTRS, **kwattrs: KW_ATTRS) -> None:
        for named_attribute in self.AttributeDefinitions:
            attribute_value = self._check_and_get_attribute_value(
                named_attribute, posattrs, kwattrs)
            setattr(self, named_attribute.name, attribute_value)

    def _check_and_get_attribute_value(
            self, attribute: NamedAttribute,
            posattrs: POS_ATTRS, kwattrs: KW_ATTRS) -> Any:
        value = self._get_attribute_value(attribute, posattrs, kwattrs)
        return self._validate_attribute_value(attribute, attribute.name, value)

    def _get_attribute_value(
            self, attribute: NamedAttribute,
            posattrs: POS_ATTRS, kwattrs: KW_ATTRS) -> Any:
        try:
            return attribute.extract_value(posattrs, kwattrs)
        except ValueError:
            if attribute.required:
                raise RequiredAttributeMissing(attribute.name, type(self))
            return attribute.default

    def _validate_attribute_value(
            self, attribute: Attribute, name: str, value: Any) -> Any:
        if attribute.validator and attribute.validator(value) is False:
            raise AttributeValidationFailed(name, value, type(self))
        return value


def blueprint(name: str,
              bases: Tuple[type, ...],
              namespace: Dict[str, Any]) -> type:
    """metaclass to create a Blueprint"""
    namespace.update(
        AttributeDefinitions=tuple(_attributes_of_namespace(namespace)),
    )
    return type(name, (*bases, _Blueprint), namespace)
