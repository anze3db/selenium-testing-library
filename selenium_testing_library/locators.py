from typing import TYPE_CHECKING, Iterable, List, Union

from selenium.webdriver.common.by import By as SeleniumBy
from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from .screen import ElementsFinder


class By:
    CLASS_NAME: str = SeleniumBy.CLASS_NAME
    CSS_SELECTOR: str = SeleniumBy.CSS_SELECTOR
    ID: str = SeleniumBy.ID
    LINK_TEXT: str = SeleniumBy.LINK_TEXT
    PARTIAL_LINK_TEXT: str = SeleniumBy.PARTIAL_LINK_TEXT
    TAG_NAME: str = SeleniumBy.TAG_NAME
    XPATH: str = SeleniumBy.XPATH
    NAME: str = SeleniumBy.NAME
    # STL queries:
    ROLE = "role"
    TEXT = "text"
    PLACEHOLDER_TEXT = "placeholder text"
    LABEL_TEXT = "label text"
    ALT_TEXT = "alt text"
    TITLE = "title"
    TEST_ID = "test id"
    DISPLAY_VALUE = "display value"


class Locator:
    BY: str

    def __init__(self, selector: str, exact: bool = True):
        self.selector = selector
        self.exact = exact

    def __iter__(self):
        yield self.BY
        yield self.selector

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.selector}', exact={self.exact})"


class Css(Locator):
    BY = By.CSS_SELECTOR


class XPath(Locator):
    BY = By.XPATH


class Id(Locator):
    BY = By.ID


class Name(Locator):
    BY = By.NAME


class TagName(Locator):
    BY = By.TAG_NAME


class LinkText(Locator):
    BY = By.LINK_TEXT


class PartialLinkText(Locator):
    BY = By.PARTIAL_LINK_TEXT


class ClassName(Locator):
    BY = By.CLASS_NAME


class Role(Locator):
    BY = By.ROLE


class Text(Locator):
    BY = By.TEXT


class PlaceholderText(Locator):
    BY = By.PLACEHOLDER_TEXT


class LabelText(Locator):
    BY = By.LABEL_TEXT


class AltText(Locator):
    BY = By.ALT_TEXT


class Title(Locator):
    BY = By.TITLE


class TestId(Locator):
    BY = By.TITLE


class DisplayValue(Locator):
    BY = By.DISPLAY_VALUE


LocatorType = Union[
    Iterable[
        str,
    ],
    Locator,
]
