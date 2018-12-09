"""Reconciliation algorithms"""
from typing import Dict

from .component import Component, Index


def reconcile_components(old: Component, new: Component) \
        -> Component:
    """Reconciles two Components

    If old and new are different classes,
    the old gets unmounted and the new gets mounted using the old index.

    If classes are equal but components are not
    the old gets updated with new attributes
    """
    if old.__class__ != new.__class__:
        old.unmount()
        new.mount(old.index)
        return new

    if old != new:
        old.update(new.attributes)
    return old


def reconcile_dicts(host: Component, old: Dict, new: Dict) -> Dict:
    """Reconciles all components for two given dictionaries

    Components not in the new dict but in the old gets unmounted.

    New components get mounted.

    Different components under the same key are reconciled.
    """
    reconciled_dict = {}
    for key, item in new.items():
        if key not in old:
            reconciled_dict[key] = item
            item.mount(Index(host, key, None))
        else:
            item = old.pop(key)
            reconciled_dict[key] = reconcile_components(item, new[key])
    for item in old.values():
        item.unmount()
    return reconciled_dict
