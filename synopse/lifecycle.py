"""Describes the Lifecycle of Blueprints"""


class Lifecycle:
    """A Lifecycle of a Blueprint"""
    def mount(self) -> None:
        """Called when inserted into a Structure"""
        pass

    def unmount(self) -> None:
        """Called when deleted from a structure"""
        pass