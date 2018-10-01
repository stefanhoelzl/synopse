"""Structure"""
from typing import Union, Any, Optional, Iterable, List, Dict, Set

from .lifecycle import Lifecycle

Key = Union[int, str]
Item = Lifecycle
Definition = Union[Optional[Item], Iterable[Optional[Item]]]


# WORKAROUND: recursive type definition needed
#  MYPY-731: https://github.com/python/mypy/issues/731
def _flatten(iterable: Iterable) -> Iterable:
    for item in iterable:
        if isinstance(item, Iterable):
            yield from _flatten(item)
        else:
            yield item


class Structure:
    """A Structure contains Blueprints accessible by Keys"""
    def __init__(self, *args: Definition, **kwargs: Optional[Item]) -> None:
        self._positional_children: List[Item] = [
            arg for arg in _flatten(args) if arg is not None
        ]
        self._keyword_children: Dict[str, Item] = {
            k: v for k, v in kwargs.items() if v is not None
        }

    def _asdict(self) -> Dict[Key, Item]:
        complete_dict: Dict[Key, Item] = {}
        complete_dict.update({k: v for k, v in self._keyword_children.items()})
        complete_dict.update({
            k: v for k, v in enumerate(self._positional_children)
        })
        return complete_dict

    def __repr__(self) -> str:
        return self._asdict().__repr__()

    def __eq__(self, other: Any) -> bool:
        return self._asdict().__eq__(other)

    def __getitem__(self, key: Key) -> Optional[Item]:
        if isinstance(key, int):
            try:
                return self._positional_children[key]
            except IndexError:
                return None
        return self._keyword_children.get(key)

    def __setitem__(self, key: Key, value: Lifecycle) -> None:
        """Sets a value for a key

        Special cases when accessing positional keys:
        * If key == len(positionals): value is appended
        * If key is in use: value is inserted before
        """
        value.mount()
        if isinstance(key, int):
            if key < len(self._positional_children):
                self._positional_children.insert(key, value)
            elif key == len(self._positional_children):
                self._positional_children.append(value)
            else:
                raise IndexError("{} index out of range".format(
                    self.__class__.__name__
                ))
        else:
            self._keyword_children[key] = value

    def __delitem__(self, key: Key) -> None:
        value = self[key]
        if value is not None:
            value.unmount()

        if isinstance(key, int):
            del self._positional_children[key]
        else:
            del self._keyword_children[key]

    def keys(self) -> Set[Key]:
        """Set of keys defined in this Structure"""
        positional_keys = range(len(self._positional_children))
        return set(self._keyword_children.keys()) | set(positional_keys)
