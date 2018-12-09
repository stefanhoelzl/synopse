"""Reconciliation algorithms"""
from typing import Dict

from .component import Component


def reconcile(old: Component, new: Component) \
        -> Component:
    """Reconciles two Components"""
    if old.__class__ != new.__class__:
        old.unmount()
        new.mount(old.index)
        return new

    if old != new:
        old.update(new.attributes)
    return old


def reconcile_dict(host: Component, old: Dict, new: Dict) -> None:
    """Reconciles all components for two given dictionaries"""
    assert host
    assert old
    assert new
