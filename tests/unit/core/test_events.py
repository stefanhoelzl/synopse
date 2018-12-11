import pytest

from unittest.mock import MagicMock

from synopse.core.errors import AttributeValidationFailed
from synopse.core.events import EventHandler


class TestActionMixin:
    def test_action_is_callable(self, create_component_class):
        with_event = create_component_class(my_event=EventHandler())()
        assert callable(with_event.my_event)

    def test_do_noting_if_handler_is_none(self, create_component_class):
        with_event = create_component_class(my_event=EventHandler())()
        with_event.my_event(arg=3)

    def test_emit_event(self, create_component_class):
        event_handler = MagicMock()
        with_event = create_component_class(my_event=EventHandler())(
            my_event=event_handler
        )
        with_event.my_event(arg=3)
        event_handler.assert_called_once()
        event = event_handler.call_args[0][0]
        assert "my_event" == event.name
        assert with_event == event.emitter
        assert {"arg": 3} == event_handler.call_args[1]

    def test_event_handler_must_be_callable(self, create_component_class):
        with pytest.raises(AttributeValidationFailed):
            create_component_class(my_event=EventHandler())(
                my_event="not callable"
            )
