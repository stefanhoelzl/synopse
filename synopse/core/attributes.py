"""Attributes are used to define features of Components"""
from typing import Any, Optional, Dict, Union, Callable, Mapping

from dataclasses import dataclass, asdict
from .errors import RequiredAttributeMissing, AttributeValidationFailed


Validator = Callable[[Any], bool]


@dataclass
class Attribute:
    """Attribute defines a single value feature"""
    default: Any = None
    required: bool = False
    validator: Optional[Validator] = None
    position: Optional[Union[int, slice]] = None

    def asdict(self) -> Dict[str, Any]:
        """Returns the attribute as dict"""
        return asdict(self)

    def __getitem__(self, item: Union[int, slice]) -> "Attribute":
        self.position = item
        return self


def extract_values(attributes: Mapping[str, Attribute],
                   *posattrs: Any, **kwattrs: Any) -> Dict[str, Any]:
    """Extracts the value out of a argument list or keyword arguments
    Determines whats to extract by position or field.
    """
    values = {}
    for name, attr in attributes.items():
        value = _get_value(name, attr, posattrs, kwattrs)
        # pylint: disable=not-callable
        if attr.validator and attr.validator(value) is False:
            raise AttributeValidationFailed(name, value)
        values[name] = value
    return values


def _get_value(name: str, attr: Attribute, posattrs: Any, kwattrs: Any) -> Any:
    try:
        if attr.position is not None:
            return posattrs[attr.position]
        return kwattrs[name]
    except (IndexError, KeyError):
        if attr.required:
            raise RequiredAttributeMissing(name)
        return attr.default
