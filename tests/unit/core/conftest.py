from unittest.mock import MagicMock

import pytest

from synopse.core.component import Index
from synopse.core.composite_component import CompositeComponent


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
