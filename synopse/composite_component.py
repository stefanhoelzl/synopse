"""Components composed of other components"""
from typing import Any, Optional, Dict

from .component import Component, Index
from .reconcile import reconcile


class CompositeComponent(Component[Component]):
    """TODO"""
    def mount(self, index: Optional[Index] = None) -> None:
        super().mount(index)
        self.content.mount(index)

    def unmount(self) -> None:
        self.content.unmount()
        super().unmount()

    def update(self, attributes: Optional[Dict[str, Any]] = None) -> None:
        super().update(attributes)
        self._content = reconcile(self.index, self.content, self.layout())

    def layout(self) -> Component:
        raise NotImplementedError()
