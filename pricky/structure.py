"""Structure"""
from typing import cast, Union, Any, Optional, Iterable, Tuple

Key = Union[int, str]
WithLifecycle = Any
StructureDefinition = Optional[Union[WithLifecycle,
                                     Iterable[WithLifecycle],
                                     "Structure"]]


class Structure(dict):
    """A Structure contains Blueprints accessible by Keys"""

    def __init__(self, structure_definition: StructureDefinition = None) -> None:
        if isinstance(structure_definition, dict):
            super().__init__(structure_definition)
        elif isinstance(structure_definition, Iterable):
            # WORKAROUND: mypy bug with inferencing type of enumeration()
            #  MYPY-230:  https://github.com/python/mypy/issues/230
            #  MYPY-5579: https://github.com/python/mypy/issues/5579
            typed_enumeration = cast(Iterable[Tuple[int, WithLifecycle]],
                                     enumerate(structure_definition))
            super().__init__({key: blueprint
                              for key, blueprint in typed_enumeration})
        elif structure_definition is not None:
            super().__init__({0: structure_definition})
        else:
            super().__init__()
