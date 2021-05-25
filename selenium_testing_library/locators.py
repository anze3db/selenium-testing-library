from typing import Optional, Tuple, Union

from selenium.webdriver.common.by import By as SeleniumBy  # type: ignore
from typing_extensions import Literal


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
    PLACEHOLDER = "placeholder"
    LABEL_TEXT = "label text"
    ALT_TEXT = "alt text"


class Locator:
    BY: Optional[str] = None

    def __init__(self, selector: str):
        self.selector = selector

    def __iter__(self):
        if self.BY is None:
            raise Exception

        yield self.BY
        yield self.selector


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


class Placeholder(Locator):
    BY = By.PLACEHOLDER


class LabelText(Locator):
    BY = By.LABEL_TEXT

class LabelText(Locator):
    BY = ByOptions.ALT_TEXT


LocatorType = Union[
    Tuple[
        Literal[
            "class name",
            "css selector",
            "id",
            "label text",
            "link text",
            "name",
            "partial link text",
            "placeholder",
            "role",
            "tag_name",
            "text",
            "xpath",
            "alt text",
        ],
        str,
    ],
    Locator,
]
