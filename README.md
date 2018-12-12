# synopse

A Framework for declarative programming

```python
from synopse.core import CompositeComponent
from synopse.ui.wx import WxApp, WxFrame, WxButton


class MovingCounterButton(CompositeComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def structure(self):
        return WxButton(
            label=self.counter,
            position=(0, self.counter),
            button=self.handler
        )

    def handler(self, *args, **kwargs):
        self.counter += 1


class MyFrame(CompositeComponent):

    def structure(self):
        return WxFrame(
            MovingCounterButton()
        )


WxApp(MyFrame()).start()

```
