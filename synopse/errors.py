"""Errors which can be raised when working with Blueprints"""
from typing import Any


class BlueprintError(Exception):
    """Base exception for all Blueprint Errors"""
    pass


class RequiredAttributeMissing(BlueprintError):
    """Is raised when a required Attributed is missing"""
    def __init__(self, attribute_name: str) -> None:
        super().__init__(
            "Required attribute '{}' missing".format(
                attribute_name
            )
        )


class AttributeValidationFailed(BlueprintError):
    """Is raised when an Attribute validation fails"""
    def __init__(self, attribute_name: str, attribute_value: Any) -> None:
        super().__init__(
            "Validation failed for Attribute '{}' with value '{}'".format(
                attribute_name, attribute_value
            )
        )
