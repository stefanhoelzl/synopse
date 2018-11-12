"""Everything needed to build a Component class"""
from typing import Optional, Any, Iterator, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .base_component import Patch, Attributes, temporary_attributes
from .native_component import NativeComponent, Replace, IndexedComponent


Component = Union[NativeComponent, "CompositeComponent"]


@dataclass
class SetComponent(Patch):
    """Sets the Component for a CompositeComponent"""
    composite: "CompositeComponent"
    component: Component

    def apply(self) -> None:
        self.composite.component = self.component


class CompositeComponent(IndexedComponent, ABC):
    """TODO"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.component: Optional[Component] = None

    @property
    def native(self) -> Any:
        """Native component"""
        if self.component is None:
            return None
        if isinstance(self.component, NativeComponent):
            return self.component
        return self.component.native

    @abstractmethod
    def describe(self) -> Component:
        """TODO"""
        raise NotImplementedError()

    def mount(self) -> Any:
        self.component = self.describe()
        self.component.mount()

    def unmount(self) -> None:
        if self.component:
            self.component.unmount()
        self.component = None

    def diff(self, **attributes: Any) -> Iterator[Patch]:
        yield from super().diff(**attributes)
        yield from self._diff_component(attributes)

    def _diff_component(self, attributes: Attributes) -> Iterator[Patch]:
        if self.component is None:
            raise RuntimeError("Component must be mounted before to updating")

        with temporary_attributes(self, attributes):
            new_component = self.describe()

        if self.component.__class__ != new_component.__class__:
            yield Replace(self.component, new_component)
            yield SetComponent(self, new_component)
        elif self.component != new_component:
            yield from self.component.diff(**new_component.attributes)
