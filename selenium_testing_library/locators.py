import json
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, List, Union

from selenium.webdriver.common.by import By as SeleniumBy
from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from .screen import ElementsFinder


testing_library = Path(__file__).parent / Path("dist/main.js").read_text()


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
        self.escaped_selector = self._escape_selector(selector)
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
        return json.dumps(selector)

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
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByRole({self.escaped_selector}, {{exact: {ex}}});"
        )


class Text(Locator):
    BY = By.TEXT

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByText({self.escaped_selector}, {{exact: {ex}}});"
        )


class PlaceholderText(Locator):
    BY = By.PLACEHOLDER_TEXT

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByPlaceholderText({self.escaped_selector}, {{exact: {ex}}});"
        )


class LabelText(Locator):
    BY = By.LABEL_TEXT

    def find_elements(self, finder: "ElementsFinder"):
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByLabelText({self.escaped_selector}, {{exact: {ex}}});"
        )


class AltText(Locator):
    BY = By.ALT_TEXT

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByAltText({self.escaped_selector}, {{exact: {ex}}});"
        )


class Title(Locator):
    BY = By.TITLE

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByTitle({self.escaped_selector}, {{exact: {ex}}});"
        )


class TestId(Locator):
    BY = By.TITLE

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByTestId({self.escaped_selector}, {{exact: {ex}}});"
        )


class DisplayValue(Locator):
    BY = By.DISPLAY_VALUE

    def find_elements(self, finder: "ElementsFinder") -> List[WebElement]:
        ex = "true" if self.exact else "false"
        return finder.execute_script(
            f"{testing_library};return screen.queryAllByDisplayValue({self.escaped_selector}, {{exact: {ex}}});"
        )


LocatorType = Union[
    Iterable[
        str,
    ],
    Locator,
]
