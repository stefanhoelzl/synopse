"""Everything needed to build a Component class"""
from typing import Optional, Any, Iterator, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .base_component import Patch, Attributes, temporary_attributes
from .native_component import NativeComponent, IndexedComponent, \
    ComponentDiff


Component = Union["CompositeComponent", NativeComponent]


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
        with temporary_attributes(self, attributes):
            new_component = self.describe()

        yield from CompositeComponentDiff(self, new_component)


@dataclass
class SetComponent(Patch):
    """Sets the Component for a CompositeComponent"""
    composite: CompositeComponent
    component: Component

    def apply(self) -> None:
        self.composite.component = self.component


class CompositeComponentDiff(ComponentDiff[Component]):
    """TODO"""
    def __init__(self, composite_component: CompositeComponent,
                 new: Component) -> None:
        super().__init__(composite_component.component, new)
        self.composite = composite_component

    def replace(self, old: IndexedComponent, new: Component) -> Iterator[Patch]:
        """TODO"""
        yield from super().replace(old, new)
        yield SetComponent(self.composite, new)
