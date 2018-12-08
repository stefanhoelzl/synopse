from typing import Optional, Dict

from .component import Component, Index


def _unmount(item: Component) -> None:
    item.unmount()


def _mount(item: Component, index: Optional[Index]) -> None:
    item.mount(index)


def _update(old: Component, new: Component) -> None:
    old.update(new.attributes)


def reconcile(index: Optional[Index],
              old: Optional[Component], new: Optional[Component]) \
        -> Optional[Component]:
    if new is None and old is not None:
        _unmount(old)
        return None

    if (old is None or old.__class__ != new.__class__) and new is not None:
        if old is not None:
            index = old.index
            _unmount(old)
        _mount(new, index)
        return new

    if old != new and old is not None and new is not None:
        _update(old, new)
    return old


def reconcile_dict(component: Component, old: Dict, new: Dict) -> None:
    pass
