"""Reconciliation algorithms"""
from typing import Dict, List, Optional, Union
from itertools import zip_longest


from .component import Component, Index


Reconcileable = Union[None, Component, List]


def reconcile(host: Component, key: str, position: Optional[int],
              old: Reconcileable, new: Reconcileable) -> Reconcileable:
    """Dispatches to the matching reconciliation algorithm"""
    if old is None and new is not None:
        return _mounted(host, key, position, new)

    if new is None and old is not None:
        return _unmounted(host, key, old)

    if isinstance(old, list) != isinstance(new, list):
        _unmounted(host, key, old)
        return _mounted(host, key, None, new)

    if isinstance(old, list) and isinstance(new, list):
        return reconcile_list(host, key, old, new)

    if isinstance(old, Component) and isinstance(new, Component):
        return reconcile_components(old, new)

    return None


def _mounted(host: Component, key: str, position: Optional[int],
             reconcileable: Reconcileable) -> Reconcileable:
    if isinstance(reconcileable, list):
        return reconcile_list(host, key, [], reconcileable)
    if reconcileable is not None:
        reconcileable.mount(Index(host, key, position))
    return reconcileable


def _unmounted(host: Component, key: str, reconcileable: Reconcileable) \
        -> Reconcileable:
    if isinstance(reconcileable, list):
        return reconcile_list(host, key, reconcileable, [])
    if reconcileable is not None:
        reconcileable.unmount()
    return None


def reconcile_components(old: Component, new: Component) \
        -> Component:
    """Reconciles two Components

    * old and new are different classes:
        old gets unmounted and new gets mounted using the old index.
        returning new

    * component attributes are not equal:
        old gets updated with attributes of new
        returning updated old

    * components are equal
        returning old
    """
    if old.__class__ != new.__class__:
        old.unmount()
        new.mount(old.index)
        return new

    if old.attributes != new.attributes:
        old.update(new.attributes)
    return old


def reconcile_dicts(host: Component, old: Dict, new: Dict) -> Dict:
    """Reconciles all components in given dictionaries

    * Items in new but not in old get mounted under the given host.
    * Items in new and old gets reconciled.
    * Items not in new but in the old gets unmounted.
    """
    reconciled_dict = {}
    for key, new_child in new.items():
        reconciled = reconcile(host, key, None, old.pop(key, None), new_child)
        if reconciled is not None:
            reconciled_dict[key] = reconciled
    for key, old_child in old.items():
        _unmounted(host, key, old_child)
    return reconciled_dict


def reconcile_list(host: Component, key: str, old: List, new: List) -> List:
    """Reconcile all components in given lists

    Each item in old and new at the same position are getting reconciled
    * only a item in new -> mount new at host given key at position
    * only a item in old -> unmount old
    * items in both      -> reconcile components
    """
    zipped = zip_longest(old, new, fillvalue=None)
    reconciled_list = [
        reconcile(host, key, ndx, old_item, new_item)
        for ndx, (old_item, new_item) in enumerate(zipped)
    ]
    return [r for r in reconciled_list if r is not None]
