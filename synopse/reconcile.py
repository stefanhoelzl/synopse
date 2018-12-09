"""Reconciliation algorithms"""
from typing import Dict, List
from itertools import zip_longest


from .component import Component, Index


def reconcile() -> None:
    pass


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


def reconcile_list(host: Component, key: str, old: List, new: List) -> List:
    """Reconcile all components in given lists

    Each item in old and new at the same position are getting reconciled
    * only a item in new -> mount new at host given key at position
    * only a item in old -> unmount old
    * items in both      -> reconcile components
    """
    reconciled_list = []
    zipped = zip_longest(old, new, fillvalue=None)
    for ndx, (old_item, new_item) in enumerate(zipped):
        if old_item is None:
            reconciled_list.append(new_item)
            new_item.mount(Index(host, key, ndx))
        elif new_item is None:
            old_item.unmount()
        else:
            reconciled_list.append(reconcile_components(old_item, new_item))
    return reconciled_list
