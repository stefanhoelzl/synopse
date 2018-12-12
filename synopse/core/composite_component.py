"""Components composed of other components"""
from typing import Any, Optional, Dict

from .component import Component, Index
from .reconcile import reconcile_components


class CompositeComponent(Component[Component]):
    """TODO"""
    def mount(self, index: Optional[Index] = None) -> None:
        """Mounts itself and its composite"""
        super().mount(index)
        self.content.mount(index)

    def unmount(self) -> None:
        """Unmounts itself and its composite"""
        self.content.unmount()
        super().unmount()

    def update(self, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Updates itself and its composite"""
        super().update(attributes)
        # pylint: disable=attribute-defined-outside-init
        self.content = reconcile_components(self.content, self.structure())

    def structure(self) -> Component:
        """Describes the structure of the component"""
        raise NotImplementedError()
