"""Attributes are used to define features of Blueprints"""
from typing import Any, Optional, Dict, Union

from dataclasses import dataclass, asdict

from pricky.typing import Validator, KwAttrs, PosAttrs


@dataclass
class Attribute:
    """Attribute defines a single value feature"""
    default: Any = None
    required: bool = False
    validator: Optional[Validator] = None
    position: Optional[Union[int, slice]] = None
    container: bool = False

    @property
    def kwargs(self) -> Dict[str, Any]:
        """Dict with keyword arguments to create an identical Attribute"""
        init_fn = type(self).__init__
        kwargs_count = len(init_fn.__annotations__)-1
        kwargs = init_fn.__code__.co_varnames[-kwargs_count:]
        return {
            key: getattr(self, key, None) for key in kwargs
        }

    def asdict(self) -> Dict[str, Any]:
        """Returns the attribute as dict"""
        return asdict(self)

    def __getitem__(self, item: Union[int, slice]) -> "Attribute":
        if isinstance(item, slice):
            self.container = True
        self.position = item
        return self


@dataclass
class NamedAttribute(Attribute):
    """Attribute with a name"""
    name: str = ""

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
