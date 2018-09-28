"""Attributes are used to define features of Blueprints"""

from typing import Any, Optional


class Attribute:
    """Attribute defines a single value feature"""

    def __init__(self,
                 default: Any = None) -> None:
        """
        Args:
            default: default value of the attribute
        """
        self.item: Optional[str] = None
        self.default = default
