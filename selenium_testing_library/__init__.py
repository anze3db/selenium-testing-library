from .screen import (
    Element,
    Screen,
    NoElementsReturned,
    MultipleElementsReturned,
)


class Locator:
    def __init__(self, css_selector: str):
        self.value = css_selector

    def __iter__(self):
        yield "css selector"
        yield self.value


__version__ = "0.0.1"
