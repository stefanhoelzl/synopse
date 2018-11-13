"""Everything needed to build a Component class"""
from typing import Any, Iterator, Optional, TypeVar, Generic
from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass

from .base_component import BaseComponent, Patch


class Index(namedtuple("Index", "host, slot, position")):
    """Index of an Component"""
    host: "NativeComponent"
    slot: str
    position: Optional[int]


class IndexedComponent(BaseComponent, ABC):
    """Component with Index"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.index: Optional[Index] = None

    @abstractmethod
    def mount(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def unmount(self) -> None:
        raise NotImplementedError()


class NativeComponent(IndexedComponent, ABC):
    """Native Component"""
    @abstractmethod
    def mount(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def unmount(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def replace(self, index: Index, new: BaseComponent) -> None:
        """Replaces a subcomponent"""
        raise NotImplementedError()

    @abstractmethod
    def insert(self, item: BaseComponent, index: Index) -> None:
        """Inserts a new subcomponent"""
        raise NotImplementedError()

    @abstractmethod
    def remove(self, item: BaseComponent, index: Index) -> None:
        """Removes a subcomponent"""
        raise NotImplementedError()

    def diff_attribute(self, name: str, value: Any) -> Iterator[Patch]:
        yield from []


@dataclass
class Replace(Patch):
    """Replaces a component with another"""
    old: "IndexedComponent"
    new: BaseComponent

    @property
    def index(self) -> Index:
        """Index to replace"""
        if self.old.index is None:
            raise Exception("TODO")
        return self.old.index

    @property
    def host(self) -> NativeComponent:
        """Native host component where to replace"""
        return self.index.host

    def apply(self) -> None:
        pass


C = TypeVar('C', bound=BaseComponent)  # pylint: disable=invalid-name


class ComponentDiff(Generic[C]):
    """TODO"""

    def __init__(self, old: Optional[IndexedComponent],
                 new: Optional[C]) -> None:
        self.old = old
        self.new = new

    def __iter__(self) -> Iterator[Patch]:
        # pylint: disable=fixme
        # TODO: handle lists, original/changed is None, ...
        if self.old and self.new:
            yield from self.change(self.old, self.new)

    def change(self, old: IndexedComponent, new: C) -> Iterator[Patch]:
        """TODO"""
        if old.__class__ != new.__class__:
            yield from self.replace(old, new)
        elif not old == new:
            yield from old.diff(**new.attributes)

    # pylint: disable=no-self-use
    def replace(self, old: IndexedComponent, new: C) -> Iterator[Patch]:
        """TODO"""
        yield Replace(old, new)


class NativeComponentDiff(ComponentDiff[IndexedComponent]):
    """TODO"""
    def __init__(self, index: Index,
                 old: Optional[IndexedComponent],
                 new: Optional[IndexedComponent]) -> None:
        super().__init__(old, new)
        self.index = index
