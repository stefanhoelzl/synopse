"""NativeComponent"""
from typing import Dict, Optional, Any

from .component import Component, Index
from .reconcile import reconcile


def _flattened_layout(layout):
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
        return self.attributes

    def mount(self, index: Optional[Index] = None) -> None:
        super().mount(index)
        if index:
            index.host.insert(index.key, index.position, self)
        for key, pos, child in _flattened_layout(self.content):
            child.mount(Index(self, key, pos))

    def unmount(self) -> None:
        for key, pos, child in _flattened_layout(self.content):
            child.unmount()
        if self.index:
            self.index.host.remove(self.index.key, self.index.position, self)
        super().unmount()

    def update(self, attributes: Optional[Dict[str, Any]] = None):
        super().update(attributes)
        layout = self.layout()
        for key, pos, child in _flattened_layout(self.content):
            self.content[key] = reconcile(
                Index(self, key, pos), self.content[key], layout.get(key)
            )
