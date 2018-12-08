from unittest.mock import MagicMock

import pytest

from synopse.component import Component, Index
from synopse.composite_component import CompositeComponent


@pytest.fixture
def create_component_class():
    def wrapper(**attributes):
        return type("ComponentToTest", (Component,), attributes)
    return wrapper


@pytest.fixture
def component(create_component_class):
    component = create_component_class()()
    component.layout = MagicMock()
    return component


@pytest.fixture
def composite_component():
    composite = CompositeComponent()
    composite.layout = MagicMock()
    return composite


@pytest.fixture
def index():
    return Index(None, "key", 0)
