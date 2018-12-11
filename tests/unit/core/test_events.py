from unittest.mock import MagicMock

from synopse.core.component import Component
from synopse.core.events import EventAttribute


class TestActionMixin:
    def test_action_is_callable(self):
        class WithEvents(Component):
            my_event = EventAttribute()
        assert callable(WithEvents().my_event)

    def test_emit_event(self):
        event_handler = MagicMock()

        class WithEvents(Component):
            my_action = EventAttribute()
        with_event = WithEvents(my_action=event_handler)
        with_event.my_action(arg=3)
        event_handler.assert_called_once()
        event = event_handler.call_args[0][0]
        assert "my_action" == event.name
        assert with_event == event.emitter
        assert {"arg": 3} == event_handler.call_args[1]
