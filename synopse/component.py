"""Everything needed to build a Component class"""
from typing import Optional, Any, Iterator, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .base_component import Patch, Attributes, temporary_attributes
from .native_component import NativeComponent, Replace, IndexedComponent


RenderedComponent = Union[NativeComponent, "Component"]


@dataclass
class SetRendering(Patch):
    """Sets the rendered attribute for a Component"""
    component: "Component"
    rendering: RenderedComponent

    def apply(self) -> None:
        self.component.rendered = self.rendering


class Component(IndexedComponent, ABC):
    """TODO"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.rendered: Optional[RenderedComponent] = None

    @property
    def native(self) -> Any:
        """Native component"""
        if self.rendered is None:
            return None
        if isinstance(self.rendered, NativeComponent):
            return self.rendered
        return self.rendered.native

    @abstractmethod
    def render(self) -> RenderedComponent:
        """TODO"""
        raise NotImplementedError()

    def mount(self) -> Any:
        self.rendered = self.render()
        self.rendered.mount()

    def unmount(self) -> None:
        if self.rendered:
            self.rendered.unmount()
        self.rendered = None

    def diff(self, **attributes: Any) -> Iterator[Patch]:
        yield from super().diff(**attributes)
        yield from self._diff_rendering(attributes)

    def _diff_rendering(self, attributes: Attributes) -> Iterator[Patch]:
        if self.rendered is None:
            raise RuntimeError("Component must be mounted before to updating")

        with temporary_attributes(self, attributes):
            new_rendering = self.render()

        if self.rendered.__class__ != new_rendering.__class__:
            yield Replace(self.rendered, new_rendering)
            yield SetRendering(self, new_rendering)
        elif self.rendered != new_rendering:
            yield from self.rendered.diff(**new_rendering.attributes)
