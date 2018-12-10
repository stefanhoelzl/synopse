"""NativeComponent"""
from typing import Dict, Optional, Any, Iterator, Tuple

from .component import Component, Index
from .reconcile import reconcile_dicts


def _flattened_layout(layout: Dict) \
        -> Iterator[Tuple[str, Optional[int], Component]]:
    for key, child in layout.items():
        if isinstance(child, list):
            for pos, pos_child in enumerate(child):
                yield key, pos, pos_child
        else:
            yield key, None, child


class NativeComponent(Component[Dict]):
    """Native Component"""
    def layout(self) -> Dict:
        """Layout is described my its attributes"""
        return self.attributes

    def mount(self, index: Optional[Index] = None) -> None:
        """Mounts itself and all its children
        """
        super().mount(index)
        for key, pos, child in _flattened_layout(self.content):
            child.mount(Index(self, key, pos))

    def unmount(self) -> None:
        """Unmounts all children and itself.
        """
        for _, _, child in _flattened_layout(self.content):
            child.unmount()
        super().unmount()

    def update(self, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Updates itself and all its children"""
        super().update(attributes)
        # pylint: disable=attribute-defined-outside-init
        self.content = reconcile_dicts(self, self.content, self.layout())
