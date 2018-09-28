"""Errors which can be raised when working with Blueprints"""
from typing import Any


class BlueprintError(Exception):
    """Base exception for all Blueprint Errors"""
    pass


class RequiredAttributeMissing(BlueprintError):
    """Is raised when a required Attributed is missing"""
    def __init__(self, attribute_name: str, blueprint: type) -> None:
        super().__init__(
            "Required attribute '{}' for {} missing".format(
                attribute_name, blueprint.__name__
            )
        )


class AttributeValidationFailed(BlueprintError):
    """Is raised when an Attribute validation fails"""
    def __init__(self, attribute_name: str, attribute_value: Any,
                 blueprint: type) -> None:
        super().__init__(
            "Attribute validation for {} "
            "failed for Attribute '{}' with value '{}'".format(
                blueprint.__class__, attribute_name, attribute_value
            )
        )
