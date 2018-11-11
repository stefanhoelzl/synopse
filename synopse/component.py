"""Everything needed to build a Component class"""
from typing import Optional, Any, Iterator
from dataclasses import dataclass

from .base_component import BaseComponent, Patch, Attributes, \
    temporary_attributes
from .native_component import Replace


@dataclass
class SetRendering(Patch):
    """Sets the rendered attribute for a Component"""
    component: "Component"
    rendering: "BaseComponent"

    def apply(self) -> None:
        self.component.rendered = self.rendering


class Component(BaseComponent):
    """TODO"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.rendered: Optional[BaseComponent] = None

    @property
    def native(self) -> Any:
        if self.rendered:
            return self.rendered.native
        return None

    def render(self) -> BaseComponent:
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
            raise Exception()

        with temporary_attributes(self, attributes):
            new_rendering = self.render()

        if self.rendered.__class__ != new_rendering.__class__:
            yield Replace(self.rendered, new_rendering)
            yield SetRendering(self, new_rendering)
        elif self.rendered != new_rendering:
            yield from self.rendered.diff(**new_rendering.attributes)
