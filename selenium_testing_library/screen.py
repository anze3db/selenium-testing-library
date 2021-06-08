from __future__ import annotations

from typing import Callable, List, Optional, TypeVar

from selenium.common.exceptions import TimeoutException  # type: ignore
from selenium.webdriver import Remote as Driver  # type: ignore
from selenium.webdriver.remote.webelement import WebElement  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore

from . import locators

Locator = locators.LocatorType

T = TypeVar("T")


class MultipleSuchElementsException(Exception):
    ...


class NoSuchElementException(Exception):
    ...


by_to_locator = {
    locators.By.CLASS_NAME: locators.ClassName,
    locators.By.CSS_SELECTOR: locators.Css,
    locators.By.ID: locators.Id,
    locators.By.LINK_TEXT: locators.LinkText,
    locators.By.PARTIAL_LINK_TEXT: locators.PartialLinkText,
    locators.By.TAG_NAME: locators.TagName,
    locators.By.XPATH: locators.XPath,
    locators.By.NAME: locators.Name,
    locators.By.TEXT: locators.Text,
    locators.By.ROLE: locators.Role,
    locators.By.PLACEHOLDER_TEXT: locators.PlaceholderText,
    locators.By.LABEL_TEXT: locators.LabelText,
    locators.By.ALT_TEXT: locators.AltText,
}


class Screen:
    def __init__(self, driver: Driver):
        self.driver = driver

    def get_by(self, locator: Locator) -> WebElement:
        if not isinstance(locator, locators.Locator):
            by, selector = locator
            locator = by_to_locator[by](selector)
        els = locator.find_elements(self.driver)

        if not els:
            raise NoSuchElementException()

        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def query_by(self, locator: Locator) -> Optional[WebElement]:
        if not isinstance(locator, locators.Locator):
            by, selector = locator
            locator = by_to_locator[by](selector)
        els = locator.find_elements(self.driver)

        if not els:
            return None
        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def find_by(self, locator: Locator, *, timeout=5, poll_frequency=0.5) -> WebElement:
        if not isinstance(locator, locators.Locator):
            by, selector = locator
            locator = by_to_locator[by](selector)

        try:
            els = self.wait_for(
                locator.find_elements,
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException()
        if len(els) > 1:
            raise MultipleSuchElementsException()
        return els[0]

    def get_all_by(self, locator: Locator) -> List[WebElement]:
        if not isinstance(locator, locators.Locator):
            by, selector = locator
            locator = by_to_locator[by](selector)
        els = locator.find_elements(self.driver)
        if not els:
            raise NoSuchElementException()

        return els

    def query_all_by(self, locator: Locator) -> List[WebElement]:
        try:
            return self.get_all_by(locator)
        except NoSuchElementException:
            return []

    def find_all_by(
        self, locator: Locator, *, timeout=5, poll_frequency=0.5
    ) -> List[WebElement]:
        if not isinstance(locator, locators.Locator):
            by, selector = locator
            locator = by_to_locator[by](selector)

        try:
            return self.wait_for(
                locator.find_elements,
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException()

    # By role
    def get_by_role(self, role) -> WebElement:
        return self.get_by(locators.Role(role))

    def query_by_role(self, role: str) -> Optional[WebElement]:
        return self.get_by(locators.Role(role))

    def find_by_role(self, role: str) -> WebElement:
        return self.find_by(locators.Role(role))

    def get_all_by_role(self, role) -> List[WebElement]:
        return self.get_all_by(locators.Role(role))

    def query_all_by_role(self, role: str) -> List[WebElement]:
        return self.query_all_by(locators.Role(role))

    def find_all_by_role(self, role: str) -> List[WebElement]:
        return self.find_all_by(locators.Role(role))

    # By text
    def get_by_text(self, text: str) -> WebElement:
        return self.get_by(locators.Text(text))

    def query_by_text(self, text: str) -> Optional[WebElement]:
        return self.query_by(locators.Text(text))

    def find_by_text(self, text: str) -> WebElement:
        return self.find_by(locators.Text(text))

    def get_all_by_text(self, text: str) -> List[WebElement]:
        return self.get_all_by(locators.Text(text))

    def query_all_by_text(self, text: str) -> List[WebElement]:
        return self.query_all_by(locators.Text(text))

    def find_all_by_text(self, text: str) -> List[WebElement]:
        return self.find_all_by(locators.Text(text))

    # By placeholder
    def get_by_placeholder_text(self, value: str) -> WebElement:
        return self.get_by(locators.PlaceholderText(value))

    def query_by_placeholder_text(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.PlaceholderText(value))

    def find_by_placeholder_text(self, value: str) -> WebElement:
        return self.find_by(locators.PlaceholderText(value))

    def get_all_by_placeholder_text(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.PlaceholderText(value))

    def query_all_by_placeholder_text(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.PlaceholderText(value))

    def find_all_by_placeholder_text(self, value: str) -> List[WebElement]:
        return self.find_all_by(locators.PlaceholderText(value))

    # By label text
    def get_by_label_text(self, text: str) -> WebElement:
        return self.get_by(locators.LabelText(text))

    def query_by_label_text(self, text: str) -> Optional[WebElement]:
        return self.query_by(locators.LabelText(text))

    def find_by_label_text(self, text: str) -> WebElement:
        return self.find_by(locators.LabelText(text))

    def get_all_by_label_text(self, text: str) -> List[WebElement]:
        return self.get_all_by(locators.LabelText(text))

    def query_all_by_label_text(self, text: str) -> List[WebElement]:
        return self.query_all_by(locators.LabelText(text))

    def find_all_by_label_text(self, text: str) -> List[WebElement]:
        return self.find_all_by(locators.LabelText(text))

    # By alt text
    def get_by_alt_text(self, value: str) -> WebElement:
        return self.get_by(locators.AltText(value))

    def query_by_alt_text(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.AltText(value))

    def find_by_alt_text(self, value: str) -> WebElement:
        return self.find_by(locators.AltText(value))

    def get_all_by_alt_text(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.AltText(value))

    def query_all_by_alt_text(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.AltText(value))

    def find_all_by_alt_text(self, value: str) -> List[WebElement]:
        return self.find_all_by(locators.AltText(value))

    # By title
    def get_by_title(self, value: str) -> WebElement:
        return self.get_by(locators.Title(value))

    def query_by_title(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.Title(value))

    def find_by_title(self, value: str) -> WebElement:
        return self.find_by(locators.Title(value))

    def get_all_by_title(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.Title(value))

    def query_all_by_title(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.Title(value))

    def find_all_by_title(self, value: str) -> List[WebElement]:
        return self.find_all_by(locators.Title(value))

    # By test id
    def get_by_test_id(self, value: str) -> WebElement:
        return self.get_by(locators.TestId(value))

    def query_by_test_id(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.TestId(value))

    def find_by_test_id(self, value: str) -> WebElement:
        return self.find_by(locators.TestId(value))

    def get_all_by_test_id(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.TestId(value))

    def query_all_by_test_id(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.TestId(value))

    def find_all_by_test_id(self, value: str) -> List[WebElement]:
        return self.find_all_by(locators.TestId(value))

    # By display value
    def get_by_display_value(self, value: str) -> WebElement:
        return self.get_by(locators.DisplayValue(value))

    def query_by_display_value(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.DisplayValue(value))

    def find_by_display_value(self, value: str) -> WebElement:
        return self.find_by(locators.DisplayValue(value))

    def get_all_by_display_value(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.DisplayValue(value))

    def query_all_by_display_value(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.DisplayValue(value))

    def find_all_by_display_value(self, value: str) -> List[WebElement]:
        return self.find_all_by(locators.DisplayValue(value))

    # By css
    def get_by_css(self, value: str) -> WebElement:
        return self.get_by(locators.Css(value))

    def query_by_css(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.Css(value))

    def find_by_css(self, value: str) -> WebElement:
        return self.find_by(locators.Css(value))

    def get_all_by_css(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.Css(value))

    def query_all_by_css(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.Css(value))

    def find_all_by_css(self, value: str) -> List[WebElement]:
        return self.find_all_by(locators.Css(value))

    # By xpath
    def get_by_xpath(self, value: str) -> WebElement:
        return self.get_by(locators.XPath(value))

    def query_by_xpath(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.XPath(value))

    def find_by_xpath(self, value: str) -> WebElement:
        return self.find_by(locators.XPath(value))

    def get_all_by_xpath(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.XPath(value))

    def query_all_by_xpath(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.XPath(value))

    def find_all_by_xpath(self, value: str) -> List[WebElement]:
        return self.find_all_by(locators.XPath(value))

    def wait_for(
        self,
        method: Callable[[Driver], T],
        *,
        timeout=5,
        poll_frequency=0.5,
        ignored_exceptions=None,
    ) -> T:
        return WebDriverWait(
            self.driver,
            timeout=timeout,
            poll_frequency=poll_frequency,
            ignored_exceptions=ignored_exceptions,
        ).until(method)

    def wait_for_stale(self, element: WebElement, *, timeout=5, poll_frequency=0.5):
        return self.wait_for(
            EC.staleness_of(element), timeout=timeout, poll_frequency=poll_frequency
        )


class Within(Screen):
    def __init__(self, element: WebElement):
        self.driver = element


__all__ = [
    "Screen",
    "Within",
    "MultipleSuchElementsException",
    "NoSuchElementException",
    "locators",
]
