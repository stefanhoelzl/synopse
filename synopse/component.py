"""Everything needed to build a Component class"""
from typing import Optional, Any
from .base_component import BaseComponent


class Component(BaseComponent):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.rendering: Optional[BaseComponent] = None

    def create(self) -> Any:
        self.rendering = self.render()
        return self.rendering.create()

    def destroy(self) -> None:
        if self.rendering:
            self.rendering.destroy()
        self.rendering = None

    def update(self, target: "BaseComponent") -> None:
        """Updates self to match another Component"""
        super().update(target)
        desired_rendering = self.render()
        if self.rendering != desired_rendering:
            self._update_rendering(desired_rendering)

    def _update_rendering(self, desired: "BaseComponent") -> None:
        if self.rendering.__class__ == desired.__class__:
            self.rendering.update(desired)  # type: ignore
        else:
            if self.rendering:
                self.rendering.destroy()
            self.rendering = desired
            self.rendering.create()
