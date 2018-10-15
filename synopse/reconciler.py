"""Reconciling two values"""

from typing import Any

Backend = Any


class Reconciler:
    """A Reconciler updates a old value to match a new value"""
    @staticmethod
    def reconcile(old: Any, new: Any) -> Any:
        """TODO"""
        if old == new:
            return old

        if old.__class__ == new.__class__:
            old.update(new)
            return old

        old.destroy()
        new.create()
        return new
