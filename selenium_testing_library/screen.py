from __future__ import annotations

from typing import Callable, Generator, List, Optional, TypeVar

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


class BaseResolver:
    def __init__(self, locator):
        self.locator = locator

    def find_elements(self, driver):
        return driver.find_elements(*self.locator)


class RoleResolver(BaseResolver):
    def __init__(self, locator):
        _, selector = locator
        self.locator = locators.XPath(f"//*[@role='{selector}']")


class TextResolver(BaseResolver):
    def __init__(self, locator):
        _, selector = locator
        self.locator = locators.XPath(f'//*[text() = "{selector}"]')


class PlaceholderTextResolver(BaseResolver):
    def __init__(self, locator):
        _, selector = locator
        self.locator = locators.XPath(f'//*[@placeholder = "{selector}"]')


class LabelTextResolver(BaseResolver):
    def __init__(self, locator):
        _, selector = locator
        self.locator = locators.XPath(f'//label[text() = "{selector}"]')

    def find_elements(self, driver):
        labels: WebElement = driver.find_elements(*self.locator)
        elements = []
        for label in labels:
            for_ = label.get_attribute("for")
            if for_ is not None:
                elements += driver.find_elements(*locators.Id(for_))
                continue
            id_ = label.get_attribute("id")
            if id_ is not None:
                elements += driver.find_elements(
                    *locators.Css(f"[aria-labelledby^='{id_}']")
                )
                continue
        return elements


class AltTextResolver(BaseResolver):
    def __init__(self, locator):
        _, selector = locator
        self.locator = locators.XPath(f'//*[@alt = "{selector}"]')


by_to_resolver = {
    locators.By.CLASS_NAME: BaseResolver,
    locators.By.CSS_SELECTOR: BaseResolver,
    locators.By.ID: BaseResolver,
    locators.By.LINK_TEXT: BaseResolver,
    locators.By.PARTIAL_LINK_TEXT: BaseResolver,
    locators.By.TAG_NAME: BaseResolver,
    locators.By.XPATH: BaseResolver,
    locators.By.NAME: BaseResolver,
    locators.By.TEXT: TextResolver,
    locators.By.ROLE: RoleResolver,
    locators.By.PLACEHOLDER_TEXT: PlaceholderTextResolver,
    locators.By.LABEL_TEXT: LabelTextResolver,
    locators.By.ALT_TEXT: AltTextResolver,
    locators.By.CLASS_NAME: BaseResolver,
}


class Screen:

    TEST_ID_ATTRIBUTE = "data-testid"
    WAIT_TIMEOUT = 1

    def __init__(self, driver: Driver):
        self.driver = driver

    def get_by(self, locator: Locator) -> WebElement:
        by, _ = locator
        resolver = by_to_resolver[by](locator)
        els = resolver.find_elements(self.driver)

        if not els:
            raise NoSuchElementException()

        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def query_by(self, locator: Locator) -> Optional[WebElement]:
        by, _ = locator
        resolver = by_to_resolver[by](locator)
        els = resolver.find_elements(self.driver)

        if not els:
            return None
        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def find_by(self, locator: Locator, *, timeout=5, poll_frequency=0.5) -> WebElement:
        by, _ = locator
        resolver = by_to_resolver[by](locator)

        try:
            els = self.wait_for(
                resolver.find_elements,
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException()
        if len(els) > 1:
            raise MultipleSuchElementsException()
        return els[0]

    def get_all_by(self, locator: Locator) -> List[WebElement]:
        by, _ = locator
        resolver = by_to_resolver[by](locator)
        els = resolver.find_elements(self.driver)
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
        by, _ = locator
        resolver = by_to_resolver[by](locator)

        try:
            return self.wait_for(
                resolver.find_elements,
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
