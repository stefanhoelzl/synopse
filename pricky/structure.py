"""Structure"""
from typing import Union, Any, Optional, Iterable, List, Dict, Set

Key = Union[int, str]
StructureItem = Any
StructureDefinition = Optional[Union[StructureItem,
                                     Iterable[StructureItem],
                                     Dict[str, StructureItem]]]


class Structure():
    """A Structure contains Blueprints accessible by Keys"""

    def __init__(self, structure_definition: StructureDefinition = None) -> None:
        self._positional_children: List[StructureItem] = []
        self._keyword_children: Dict[str, StructureItem] = {}
        self._init_with_structure_definition(structure_definition)

    def _init_with_structure_definition(
            self, structure_definition: StructureDefinition) -> None:
        if isinstance(structure_definition, dict):
            positionals = structure_definition.pop("__positional__", ())
            self._positional_children = list(positionals)

            self._keyword_children.update(
                {str(key): item for key, item in structure_definition.items()}
            )
        elif structure_definition is None:
            self._keyword_children.update({})
        elif isinstance(structure_definition, Iterable):
            self._positional_children = list(structure_definition)
        else:
            self._positional_children.append(structure_definition)

    def __eq__(self, other: Any) -> bool:
        complete_dict: Dict[Key, StructureItem] = {}
        complete_dict.update({k: v for k, v in self._keyword_children.items()})
        complete_dict.update({
            k: v for k, v in enumerate(self._positional_children)
        })
        return complete_dict.__eq__(other)

    def __getitem__(self, key: Key) -> StructureItem:
        if isinstance(key, int):
            try:
                return self._positional_children[key]
            except IndexError:
                return None
        return self._keyword_children.get(key)

    def __setitem__(self, key: Key, value: StructureItem) -> None:
        if isinstance(key, int):
            if key == len(self._positional_children):
                self._positional_children.append(value)
        else:
            self._keyword_children[key] = value

    def __delitem__(self, key: Key) -> None:
        if isinstance(key, int):
            del self._positional_children[key]
        else:
            del self._keyword_children[key]

    def keys(self) -> Set[Key]:
        """Set of keys defined in this Structure"""
        return set(self._keyword_children.keys()) \
               | set(range(len(self._positional_children)))
