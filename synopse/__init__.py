"""synopse"""

__author__ = "Stefan Hoelzl"
__license__ = "MIT"
__version__ = "0.1.0"


from .errors import RequiredAttributeMissing, AttributeValidationFailed
from .attributes import Attribute

from .component import Component
from .native_component import NativeComponent
from .composite_component import CompositeComponent
