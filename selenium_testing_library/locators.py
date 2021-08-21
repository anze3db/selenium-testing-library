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

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        return finder.find_elements(*self)

    def _exact_or_not(self, operator):
        escaped_selector = self._escape_selector(self.selector)
        if self.exact:
            return f"{operator} = {escaped_selector}"
        return f"contains({operator}, {escaped_selector})"

    def _escape_selector(self, selector: str) -> str:
        if '"' in selector and "'" in selector:
            selector = selector.replace('"', '", \'"\',"')
            return f'concat("{selector}")'
        elif '"' in selector:
            return f"'{selector}'"
        return f'"{selector}"'

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

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        return finder.find_elements(*XPath(f".//*[{self._exact_or_not('@role')}]"))


class Text(Locator):
    BY = By.TEXT

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        return finder.find_elements(*XPath(f'.//*[{self._exact_or_not("text()")}]'))


class PlaceholderText(Locator):
    BY = By.PLACEHOLDER_TEXT

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        return finder.find_elements(
            *XPath(f'.//*[{self._exact_or_not("@placeholder")}]')
        )


class LabelText(Locator):
    BY = By.LABEL_TEXT

    def find_elements(self, finder: "ElementsFinder"):
        labels = finder.find_elements(
            *XPath(f'.//label[{self._exact_or_not("text()")}]')
        )
        elements = []
        for label in labels:
            for_ = label.get_attribute("for")
            if for_ is not None:
                elements += finder.find_elements(*Id(for_))
                continue
            id_ = label.get_attribute("id")
            if id_:
                elements += finder.find_elements(*Css(f"[aria-labelledby='{id_}']"))
                continue
        return elements


class AltText(Locator):
    BY = By.ALT_TEXT

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        return finder.find_elements(*XPath(f'.//*[{self._exact_or_not("@alt")}]'))


class Title(Locator):
    BY = By.TITLE

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        return finder.find_elements(*XPath(f'.//*[{self._exact_or_not("@title")}]'))


class TestId(Locator):
    BY = By.TITLE

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        return finder.find_elements(
            *XPath(f'.//*[{self._exact_or_not("@data-testid")}]')
        )


class DisplayValue(Locator):
    BY = By.DISPLAY_VALUE

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        els = finder.find_elements(
            *XPath(f".//*[self::input or self::textarea or self::select]")
        )
        if self.exact:
            return [el for el in els if self.selector == el.get_attribute("value")]
        return [el for el in els if self.selector in el.get_attribute("value")]


LocatorType = Union[
    Iterable[
        str,
    ],
    Locator,
]
