"""Everything needed to build a Component class"""
from typing import Any, Dict, NamedTuple, Optional, Generic, TypeVar

from .attributes import AttributeMixin


ContentType = TypeVar("ContentType")


class Index(NamedTuple):
    """Index used to store the location of a component"""
    host: Any
    key: str
    position: Optional[int]


class Component(AttributeMixin, Generic[ContentType]):
    """A Component initialized as described with Attributes"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.index: Optional[Index] = None
        self._content: Optional[ContentType] = None

    @property
    def content(self) -> ContentType:
        """Guard to assure the component is mounted"""
        if self._content is None:
            raise RuntimeError("Component must be mounted")
        return self._content

    @content.setter
    def content(self, content: Optional[ContentType]) -> None:
        self._content = content

    def mount(self, index: Optional[Index] = None) -> None:
        """Mounts a component"""
        self.index = index
        self._content = self.structure()

    def structure(self) -> ContentType:
        """Describes the structure of the component"""
        raise NotImplementedError()

    def update(self, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Updates a component"""
        if attributes is not None:
            self.attributes = attributes

    def unmount(self) -> None:
        """Unmounts a component"""
        self.index = None
        self._content = None
