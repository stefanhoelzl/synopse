import pytest

from synopse.core.component import Component


@pytest.fixture
def create_component_class():
    def wrapper(**attributes):
        return type("ComponentToTest", (Component,), attributes)
    return wrapper
