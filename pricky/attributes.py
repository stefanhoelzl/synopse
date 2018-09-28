"""Attributes are used to define features of Blueprints"""

from typing import Any, Optional, Callable


class Attribute:
    """Attribute defines a single value feature"""

    def __init__(self,
                 default: Any = None,
                 required: bool = False,
                 validator: Optional[Callable] = None) -> None:
        """
        Args:
            default: default value of the attribute
            required: True if the attribute is required
        """
        self.item: Optional[str] = None
        self.default = default
        self.required = required
        self.validator = validator
