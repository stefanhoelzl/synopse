"""Everything needed to build a Component class"""
from typing import Any, Iterator
from dataclasses import dataclass

from .base_component import BaseComponent, Patch, Index


@dataclass
class Replace(Patch):
    """Replaces a component with another"""
    old: "BaseComponent"
    new: "BaseComponent"

    def apply(self) -> None:
        pass


class NativeComponent(BaseComponent):
    """Native Component"""
    def mount(self) -> Any:
        raise NotImplementedError()

    def unmount(self) -> None:
        raise NotImplementedError()

    def replace(self, old: BaseComponent, new: BaseComponent) -> None:
        """Replaces a subcomponent"""
        pass

    def insert(self, item: BaseComponent, index: Index) -> None:
        """Inserts a new subcomponent"""
        pass

    def remove(self, item: BaseComponent, index: Index) -> None:
        """Removes a subcomponent"""
        pass

    def diff_attribute(self, name: str, value: Any) -> Iterator[Patch]:
        pass
