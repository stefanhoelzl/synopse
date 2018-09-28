"""Errors which can be raised when working with Blueprints"""


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
