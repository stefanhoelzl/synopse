"""Errors which can be raised when working with Components"""
from typing import Any


class ComponentError(Exception):
    """Base exception for all Component Errors"""
    pass


class RequiredAttributeMissing(ComponentError):
    """Is raised when a required Attributed is missing"""
    def __init__(self, attribute_name: str) -> None:
        super().__init__(
            "Required attribute '{}' missing".format(
                attribute_name
            )
        )


class AttributeValidationFailed(ComponentError):
    """Is raised when an Attribute validation fails"""
    def __init__(self, attribute_name: str, attribute_value: Any) -> None:
        super().__init__(
            "Validation failed for Attribute '{}' with value '{}'".format(
                attribute_name, attribute_value
            )
        )
