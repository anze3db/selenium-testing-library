from typing import Optional, Tuple, Union

from selenium.webdriver.common.by import By  # type: ignore
from typing_extensions import Literal


class ByOptions:
    CLASS_NAME: str = By.CLASS_NAME
    CSS_SELECTOR: str = By.CSS_SELECTOR
    ID: str = By.ID
    LINK_TEXT: str = By.LINK_TEXT
    PARTIAL_LINK_TEXT: str = By.PARTIAL_LINK_TEXT
    TAG_NAME: str = By.TAG_NAME
    XPATH: str = By.XPATH
    NAME: str = By.NAME
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
    BY = ByOptions.CSS_SELECTOR


class XPath(Locator):
    BY = ByOptions.XPATH


class Id(Locator):
    BY = ByOptions.ID


class Name(Locator):
    BY = ByOptions.NAME


class TagName(Locator):
    BY = ByOptions.TAG_NAME


class LinkText(Locator):
    BY = ByOptions.LINK_TEXT


class PartialLinkText(Locator):
    BY = ByOptions.PARTIAL_LINK_TEXT


class ClassName(Locator):
    BY = ByOptions.CLASS_NAME


class Role(Locator):
    BY = ByOptions.ROLE


class Text(Locator):
    BY = ByOptions.TEXT


class Placeholder(Locator):
    BY = ByOptions.PLACEHOLDER


class LabelText(Locator):
    BY = ByOptions.LABEL_TEXT

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
