"""NativeComponent"""
from typing import Dict, Optional, Any, Iterator, Tuple

from .component import Component, Index
from .reconcile import reconcile_dict


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
    def insert(self, key: str, position: Optional[int],
               component: "NativeComponent") -> None:
        """TODO"""
        raise NotImplementedError()

    def remove(self, key: str, position: Optional[int],
               component: "NativeComponent") -> None:
        """TODO"""
        raise NotImplementedError()

    def layout(self) -> Dict:
        """Layout is described my its attributes"""
        return self.attributes

    def mount(self, index: Optional[Index] = None) -> None:
        """Mounts itself and all its children

        If an index is provided, the components inserts itself into the host.
        """
        super().mount(index)
        if index:
            index.host.insert(index.key, index.position, self)
        for key, pos, child in _flattened_layout(self.content):
            child.mount(Index(self, key, pos))

    def unmount(self) -> None:
        """Unmounts all children and itself.

        If the component has an index,
        the components removes itself from the host
        """
        for _, _, child in _flattened_layout(self.content):
            child.unmount()
        if self.index:
            self.index.host.remove(self.index.key, self.index.position, self)
        super().unmount()

    def update(self, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Updates itself and all its children"""
        super().update(attributes)
        reconcile_dict(self, self.content, self.layout())
