"""Describes the Lifecycle of Blueprints"""
from typing import Any


class Lifecycle:
    """A Lifecycle of a Blueprint"""
    def mount(self) -> None:
        """Called when inserted into a Structure"""
        pass

    def update(self, target: Any = None) -> None:
        """Called when updated"""
        pass

    def unmount(self) -> None:
        """Called when deleted from a structure"""
        pass
