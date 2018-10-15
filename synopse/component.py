"""Everything needed to build a Component class"""
from typing import Optional, Any
from .base_component import BaseComponent
from .reconciler import Reconciler


class Component(BaseComponent):
    """TODO"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.rendered: Optional[BaseComponent] = None

    def render(self) -> "Component":
        """TODO"""
        raise NotImplementedError()

    def create(self) -> Any:
        self.rendered = self.render()
        return self.rendered.create()

    def destroy(self) -> None:
        if self.rendered:
            self.rendered.destroy()
        self.rendered = None

    def update(self, target: "BaseComponent") -> None:
        """Updates self to match another Component"""
        super().update(target)
        self.rendered = Reconciler.reconcile(self.rendered, self.render())
