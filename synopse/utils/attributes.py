from typing import Any, Callable, Optional

from synopse.core.attributes import Attribute


class _AttributeWithConstructor(Attribute):
    _constructor: Optional[Callable[[Any], Any]] = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.constructor = self._constructor


class IntAttribute(_AttributeWithConstructor):
    @staticmethod
    def _constructor(value: Any) -> int:
        if isinstance(value, int):
            return value
        return int(value, 0)


class FloatAttribute(_AttributeWithConstructor):
    _constructor = float


class StrAttribute(_AttributeWithConstructor):
    _constructor = str
