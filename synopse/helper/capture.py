from typing import Iterator, Tuple, Dict, Any, Callable, Optional


def _iter_captures(namespace: Dict[str, Any], capture_type: type) \
        -> Iterator[Tuple[str, Any]]:
    """Yields Attributes in an namespace dict"""
    for attribute_name, attribute in namespace.items():
        if isinstance(attribute, capture_type):
            yield attribute_name, attribute


Wrapper = Optional[Callable[[str], Any]]


def capture(cls: type, name: str, cap_type: type) \
        -> None:
    captures = {}
    for cap_name, capturing in _iter_captures(cls.__dict__, cap_type):
        captures[cap_name] = capturing
        if capturing.getter:
            setattr(cls, cap_name, capturing.getter(cap_name))
    setattr(cls, name, getattr(cls, name).new_child(captures))
