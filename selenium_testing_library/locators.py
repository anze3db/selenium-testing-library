import json
from typing import TYPE_CHECKING, Iterable, Optional, Union

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

    def __init__(self, selector: str, *, exact: bool = True):
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

    def __init__(
        self,
        role: str,
        *,
        exact: bool = True,
        hidden: bool = False,
        name: Optional[str] = None,
        description: Optional[str] = None,
        selected: Optional[bool] = None,
        checked: Optional[bool] = None,
        pressed: Optional[bool] = None,
        current: Optional[Union[bool, str]] = None,
        expanded: Optional[bool] = None,
        queryFallbacks: Optional[bool] = None,
        level: Optional[int] = None,
    ):
        self.role = role
        self.exact = exact
        self.hidden = hidden
        self.name = name
        self.description = description
        self.selected = selected
        self.checked = checked
        self.pressed = pressed
        self.current = current
        self.expanded = expanded
        self.queryFallbacks = queryFallbacks
        self.level = level

    def __repr__(self):
        return f"""{self.__class__.__name__}(
    '{self.role}',
    exact={self.exact},
    hidden={self.hidden},
    name={self.name},
    description={self.description},
    selected={self.selected},
    checked={self.checked},
    pressed={self.pressed},
    current={self.current},
    expanded={self.expanded},
    queryFallbacks={self.queryFallbacks},
    level={self.level},
)"""

    def _testing_library_js_str(self):
        res = f"return __stl__.queryAllByRole(document, {json.dumps(self.role)}, {{ "
        res += f"exact: {json.dumps(self.exact)},"
        res += f"hidden: {json.dumps(self.hidden)},"
        if self.name is not None:
            res += f"name: {json.dumps(self.name)},"
        if self.description is not None:
            res += f"description: {json.dumps(self.description)},"
        if self.selected is not None:
            res += f"selected: {json.dumps(self.selected)},"
        if self.checked is not None:
            res += f"checked: {json.dumps(self.checked)},"
        if self.pressed is not None:
            res += f"pressed: {json.dumps(self.pressed)},"
        if self.current is not None:
            res += f"current: {json.dumps(self.current)},"
        if self.expanded is not None:
            res += f"expanded: {json.dumps(self.expanded)},"
        if self.queryFallbacks is not None:
            res += f"queryFallbacks: {json.dumps(self.queryFallbacks)},"
        if self.level is not None:
            res += f"level: {json.dumps(self.level)},"
        res += "});"
        return res


class Text(Locator):
    BY = By.TEXT

    def __init__(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        ignore: Union[str, bool] = "script, style",
    ):
        self.text = text
        self.selector = selector
        self.exact = exact
        self.ignore = ignore

    def __repr__(self):
        return f"""{self.__class__.__name__}(
    '{self.text}',
    selector='{self.selector}',
    exact={self.exact},
    ignore='{self.ignore}',
)"""

    def _testing_library_js_str(self):
        return f"return __stl__.queryAllByText(document, {json.dumps(self.text)}, {{selector: {json.dumps(self.selector)}, exact: {json.dumps(self.exact)}, ignore: {json.dumps(self.ignore)}}});"


class PlaceholderText(Locator):
    BY = By.PLACEHOLDER_TEXT

    def __init__(
        self,
        text: str,
        *,
        exact: bool = True,
    ):
        self.text = text
        self.exact = exact

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.text}', exact={self.exact})"

    def _testing_library_js_str(self):
        return f"return __stl__.queryAllByPlaceholderText(document, {json.dumps(self.text)}, {{exact: {json.dumps(self.exact)}}});"


class LabelText(Locator):
    BY = By.LABEL_TEXT

    def __init__(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
    ):
        self.text = text
        self.selector = selector
        self.exact = exact

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.text}', selector={self.selector}, exact={self.exact})"

    def _testing_library_js_str(self):
        return f"return __stl__.queryAllByLabelText(document, {json.dumps(self.text)}, {{selector: {json.dumps(self.selector)}, exact: {json.dumps(self.exact)}}});"


class AltText(Locator):
    BY = By.ALT_TEXT

    def __init__(
        self,
        text: str,
        *,
        exact: bool = True,
    ):
        self.text = text
        self.exact = exact

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.text}', exact={self.exact})"

    def _testing_library_js_str(self):
        return f"return __stl__.queryAllByAltText(document, {json.dumps(self.text)}, {{exact: {json.dumps(self.exact)}}});"


class Title(Locator):
    BY = By.TITLE

    def __init__(
        self,
        title: str,
        *,
        exact: bool = True,
    ):
        self.title = title
        self.exact = exact

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.title}', exact={self.exact})"

    def _testing_library_js_str(self):
        return f"return __stl__.queryAllByTitle(document, {json.dumps(self.title)}, {{exact: {json.dumps(self.exact)}}});"


class TestId(Locator):
    BY = By.TITLE

    def __init__(
        self,
        text: str,
        *,
        exact: bool = True,
    ):
        self.text = text
        self.exact = exact

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.text}', exact={self.exact})"

    def _testing_library_js_str(self):
        return f"return __stl__.queryAllByTestId(document, {json.dumps(self.text)}, {{exact: {json.dumps(self.exact)}}});"


class DisplayValue(Locator):
    BY = By.DISPLAY_VALUE

    def __init__(
        self,
        value: str,
        *,
        exact: bool = True,
    ):
        self.value = value
        self.exact = exact

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.value}', exact={self.exact})"

    def _testing_library_js_str(self):
        return f"return __stl__.queryAllByDisplayValue(document, {json.dumps(self.value)}, {{exact: {json.dumps(self.exact)}}});"


LocatorType = Union[
    Iterable[
        str,
    ],
    Locator,
]
