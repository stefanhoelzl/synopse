"""Attributes are used to define features of Blueprints"""
from typing import Any, Optional, Dict, Union, Callable

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


@dataclass
class NamedAttribute(Attribute):
    """Attribute with a name"""
    name: str = ""

    def extract_value(self, *posattrs: Any, **kwattrs: Any) -> Any:
        """Extracts the value out of a argument list or keyword arguments
        Determines whats to extract by position or field.
        """
        value = self._get_value(*posattrs, **kwattrs)
        # pylint: disable=not-callable
        if self.validator and self.validator(value) is False:
            raise AttributeValidationFailed(self.name, value)
        return value

    def _get_value(self, *posattrs: Any, **kwattrs: Any) -> Any:
        try:
            if self.position is not None:
                return posattrs[self.position]
            return kwattrs[self.name]
        except (IndexError, KeyError):
            if self.required:
                raise RequiredAttributeMissing(self.name)
            return self.default
