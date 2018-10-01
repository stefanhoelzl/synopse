"""Structure"""
from typing import Union, Any, Optional, Sequence, List, Dict, Set

from .lifecycle import Lifecycle

Key = Union[int, str]
StructureItem = Optional[Lifecycle]
StructureDefinition = Optional[Union[StructureItem,
                                     Sequence[StructureItem],
                                     Dict[str, StructureItem]]]


class Structure:
    """A Structure contains Blueprints accessible by Keys"""

    def __init__(self,
                 structure_definition: StructureDefinition = None) -> None:
        self._positional_children: List[StructureItem] = []
        self._keyword_children: Dict[str, StructureItem] = {}
        self._init_with_structure_definition(structure_definition)

    def _init_with_structure_definition(
            self, structure_definition: StructureDefinition) -> None:
        if isinstance(structure_definition, dict):
            positionals = structure_definition.pop("__positional__", ())
            self._positional_children = list(positionals)  # type: ignore

            self._keyword_children.update(
                {key: item for key, item in structure_definition.items()}
            )
        elif structure_definition is None:
            self._keyword_children.update({})
        elif isinstance(structure_definition, Sequence):
            self._positional_children = list(structure_definition)
        else:
            self._positional_children.append(structure_definition)

    def _asdict(self) -> Dict[Key, StructureItem]:
        complete_dict: Dict[Key, StructureItem] = {}
        complete_dict.update({k: v for k, v in self._keyword_children.items()})
        complete_dict.update({
            k: v for k, v in enumerate(self._positional_children)
        })
        return complete_dict

    def __repr__(self) -> str:
        return self._asdict().__repr__()

    def __eq__(self, other: Any) -> bool:
        return self._asdict().__eq__(other)

    def __getitem__(self, key: Key) -> StructureItem:
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
