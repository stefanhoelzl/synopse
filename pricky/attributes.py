"""Attributes are used to define features of Blueprints"""

from typing import Any, Optional, Dict, Union
from pricky.typing import Validator, KwAttrs, PosAttrs


class Attribute:
    """Attribute defines a single value feature"""
    def __init__(self,
                 default: Any = None,
                 required: bool = False,
                 validator: Optional[Validator] = None,
                 position: Optional[Union[int, slice]] = None) -> None:
        """
        Args:
            default: default value of the attribute
            required: True if the attribute is required
            validator: function to validate the attribute value
        """
        self.default = default
        self.required = required
        self.validator = validator
        self.position = position

    @property
    def kwargs(self) -> Dict[str, Any]:
        """Dict with keyword arguments to create an identical Attribute"""
        init_fn = type(self).__init__
        kwargs_count = len(init_fn.__annotations__)-1
        kwargs = init_fn.__code__.co_varnames[-kwargs_count:]
        return {
            key: getattr(self, key, None) for key in kwargs
        }

    def __getitem__(self, item: int) -> "Attribute":
        self.position = item
        return self


class NamedAttribute(Attribute):
    """Attribute with a name"""
    def __init__(self, name: str, attribute: Attribute) -> None:
        super().__init__(**attribute.kwargs)
        self.name = name

    def extract_value(
            self, posattrs: PosAttrs, kwattrs: KwAttrs) -> Any:
        """Extracts the value out of a argument list or keyword arguments
        Determines whats to extract by position or field.
        """
        try:
            if self.position is not None:
                return posattrs[self.position]
            return kwattrs[self.name]
        except (IndexError, KeyError):
            raise ValueError()
