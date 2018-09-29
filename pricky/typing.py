"""typing informations for pricky"""
from typing import Any, Callable, Dict, Tuple


Validator = Callable[[Any], bool]
KwAttrs = Dict[str, Any]
PosAttrs = Tuple[Any, ...]
