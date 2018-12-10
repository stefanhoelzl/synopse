"""Attributes are used to define features of Components"""
import typing
from typing import Any, Optional, Dict, Union, Callable, Mapping, List
from collections import ChainMap
from dataclasses import dataclass, asdict

from synopse.helper.capture import capture

from .errors import RequiredAttributeMissing, AttributeValidationFailed


Validator = Callable[[Any], bool]


@dataclass
class Attribute:
    """Attribute defines a single value feature"""
    default: Any = None
    required: bool = False
    constructor: Optional[Callable[[Any], Any]] = None
    validator: Optional[Validator] = None
    position: Optional[Union[int, slice]] = None

    def asdict(self) -> Dict[str, Any]:
        """Returns the attribute as dict"""
        return asdict(self)

    def __getitem__(self, item: Union[int, slice]) -> "Attribute":
        self.position = item
        return self


class AttributeMixin:
    Attributes: typing.ChainMap[str, Attribute] = ChainMap()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        capture(cls, "Attributes", Attribute, _attribute_property)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.attributes = _extract_values(self.Attributes, *args, **kwargs)


def _attribute_property(name: str) -> property:
    def wrapper(self: AttributeMixin) -> Any:
        return self.attributes[name]
    return property(wrapper)


def _extract_values(attributes: Mapping[str, Attribute],
                    *posattrs: Any, **kwattrs: Any) -> Dict[str, Any]:
    values = {}
    for name, attr in attributes.items():
        value = _get_value(name, attr, list(posattrs), kwattrs)

        if attr.constructor is not None:
            value = attr.constructor(value)

        if attr.validator is not None and attr.validator(value) is False:
            raise AttributeValidationFailed(name, value)
        values[name] = value
    return values


def _get_value(name: str, attr: Attribute,
               posattrs: List[Any], kwattrs: Dict[str, Any]) -> Any:
    try:
        if attr.position is not None:
            value = posattrs[attr.position]
            return value
        return kwattrs[name]
    except (IndexError, KeyError):
        if attr.required:
            raise RequiredAttributeMissing(name)
        return attr.default
