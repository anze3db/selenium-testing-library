from __future__ import annotations

from typing import Any, Callable, Generator, List, Optional, TypeVar

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


class Screen:

    TEST_ID_ATTRIBUTE = "data-testid"
    WAIT_TIMEOUT = 1

    def __init__(self, driver: Driver):
        self.driver = driver

    def get_by(self, locator: Locator) -> WebElement:

        by, selector = locator

        if by == locators.ByOptions.ROLE:
            return self.get_by_role(selector)
        elif by == locators.ByOptions.TEXT:
            return self.get_by_text(selector)
        elif by == locators.ByOptions.LABEL_TEXT:
            return self.get_by_label_text(selector)
        elif by == locators.ByOptions.PLACEHOLDER:
            return self.get_by_placeholder(selector)
        elif by == locators.ByOptions.ALT_TEXT:
            return self.get_by_alt_text(selector)

        els = self.driver.find_elements(*locator)

        if not els:
            raise NoSuchElementException()

        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def query_by(self, locator: Locator) -> Optional[WebElement]:

        by, selector = locator

        if by == locators.ByOptions.ROLE:
            return self.query_by_role(selector)
        elif by == locators.ByOptions.TEXT:
            return self.query_by_text(selector)
        elif by == locators.ByOptions.LABEL_TEXT:
            return self.query_by_label_text(selector)
        elif by == locators.ByOptions.PLACEHOLDER:
            return self.query_by_placeholder(selector)
        elif by == locators.ByOptions.ALT_TEXT:
            return self.query_by_alt_text(selector)

        els = self.driver.find_elements(*locator)
        if not els:
            return None
        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def find_by(self, locator: Locator, *, timeout=5, poll_frequency=0.5) -> WebElement:

        by, selector = locator

        if by == locators.ByOptions.ROLE:
            return self.find_by_role(selector)
        elif by == locators.ByOptions.TEXT:
            return self.find_by_text(selector)
        elif by == locators.ByOptions.LABEL_TEXT:
            return self.find_by_label_text(selector)
        elif by == locators.ByOptions.PLACEHOLDER:
            return self.find_by_placeholder(selector)
        elif by == locators.ByOptions.ALT_TEXT:
            return self.find_by_alt_text(selector)

        try:
            els = self.wait_for(
                EC.presence_of_all_elements_located(locator),
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException()
        if len(els) > 1:
            raise MultipleSuchElementsException()
        return els[0]

    def get_all_by(self, locator: Locator) -> List[WebElement]:

        by, selector = locator
        if by == locators.ByOptions.ROLE:
            return self.get_all_by_role(selector)
        elif by == locators.ByOptions.TEXT:
            return self.get_all_by_text(selector)
        elif by == locators.ByOptions.LABEL_TEXT:
            return list(self.get_all_by_label_text(selector))
        elif by == locators.ByOptions.PLACEHOLDER:
            return self.get_all_by_placeholder(selector)
        elif by == locators.ByOptions.ALT_TEXT:
            return self.get_all_by_alt_text(selector)

        els = self.driver.find_elements(*locator)
        if not els:
            raise NoSuchElementException()

        return els

    def query_all_by(self, locator: Locator) -> List[WebElement]:

        by, selector = locator

        if by == locators.ByOptions.ROLE:
            return self.query_all_by_role(selector)
        elif by == locators.ByOptions.TEXT:
            return self.query_all_by_text(selector)
        elif by == locators.ByOptions.LABEL_TEXT:
            return list(self.query_all_by_label_text(selector))
        elif by == locators.ByOptions.PLACEHOLDER:
            return self.query_all_by_placeholder(selector)
        elif by == locators.ByOptions.ALT_TEXT:
            return self.query_all_by_alt_text(selector)

        try:
            return self.get_all_by(locator)
        except NoSuchElementException:
            return []

    def find_all_by(
        self, locator: Locator, *, timeout=5, poll_frequency=0.5
    ) -> List[WebElement]:
        by, selector = locator

        if by == locators.ByOptions.ROLE:
            return self.find_all_by_role(selector)
        elif by == locators.ByOptions.TEXT:
            return self.find_all_by_text(selector)
        elif by == locators.ByOptions.LABEL_TEXT:
            return list(self.find_all_by_label_text(selector))
        elif by == locators.ByOptions.PLACEHOLDER:
            return self.find_all_by_placeholder(selector)
        elif by == locators.ByOptions.ALT_TEXT:
            return self.find_all_by_alt_text(selector)

        try:
            return self.wait_for(
                EC.presence_of_all_elements_located(locator),
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException()

    # By role
    def get_by_role(self, role) -> WebElement:
        locator = locators.XPath(f"//*[@role='{role}']")
        return self.get_by(locator)

    def query_by_role(self, role: str) -> Optional[WebElement]:
        locator = locators.XPath(f"//*[@role='{role}']")
        return self.get_by(locator)

    def find_by_role(self, role: str) -> WebElement:
        locator = locators.XPath(f"//*[@role='{role}']")
        return self.find_by(locator)

    def get_all_by_role(self, role) -> List[WebElement]:
        locator = locators.XPath(f"//*[@role='{role}']")
        return self.get_all_by(locator)

    def query_all_by_role(self, role: str) -> List[WebElement]:
        locator = locators.XPath(f"//*[@role='{role}']")
        return self.query_all_by(locator)

    def find_all_by_role(self, role: str) -> List[WebElement]:
        locator = locators.XPath(f"//*[@role='{role}']")
        return self.find_all_by(locator)

    # By text
    def get_by_text(self, text: str) -> WebElement:
        locator = locators.XPath(f'//*[text() = "{text}"]')
        return self.get_by(locator)

    def query_by_text(self, text: str) -> Optional[WebElement]:
        locator = locators.XPath(f'//*[text() = "{text}"]')
        return self.query_by(locator)

    def find_by_text(self, text: str) -> WebElement:
        locator = locators.XPath(f'//*[text() = "{text}"]')
        return self.find_by(locator)

    def get_all_by_text(self, text: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[text() = "{text}"]')
        return self.get_all_by(locator)

    def query_all_by_text(self, text: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[text() = "{text}"]')
        return self.query_all_by(locator)

    def find_all_by_text(self, text: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[text() = "{text}"]')
        return self.find_all_by(locator)

    # By placeholder
    def get_by_placeholder(self, value: str) -> WebElement:
        locator = locators.XPath(f'//*[@placeholder = "{value}"]')
        return self.get_by(locator)

    def query_by_placeholder(self, value: str) -> Optional[WebElement]:
        locator = locators.XPath(f'//*[@placeholder = "{value}"]')
        return self.query_by(locator)

    def find_by_placeholder(self, value: str) -> WebElement:
        locator = locators.XPath(f'//*[@placeholder = "{value}"]')
        return self.find_by(locator)

    def get_all_by_placeholder(self, value: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[@placeholder = "{value}"]')
        return self.get_all_by(locator)

    def query_all_by_placeholder(self, value: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[@placeholder = "{value}"]')
        return self.query_all_by(locator)

    def find_all_by_placeholder(self, value: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[@placeholder = "{value}"]')
        return self.find_all_by(locator)

    # By label text
    def get_by_label_text(self, text: str) -> WebElement:
        label: WebElement = self.get_by(locators.XPath(f'//label[text() = "{text}"]'))
        id_ = label.get_attribute("for")
        return self.get_by(locators.Id(id_))

    def query_by_label_text(self, text: str) -> Optional[WebElement]:
        try:
            return self.get_by_label_text(text)
        except NoSuchElementException:
            return None

    def find_by_label_text(self, text: str) -> WebElement:
        label: WebElement = self.find_by(locators.XPath(f'//label[text() = "{text}"]'))
        id_ = label.get_attribute("for")
        return self.get_by(locators.Id(id_))

    def get_all_by_label_text(self, text: str) -> Generator[WebElement, None, None]:
        labels: WebElement = self.get_all_by(
            locators.XPath(f'//label[text() = "{text}"]')
        )
        for label in labels:
            for_ = label.get_attribute("for")
            if for_ is not None:
                yield self.get_by(locators.Id(for_))
                continue
            id_ = label.get_attribute("id")
            if id_ is not None:
                yield self.query_by(locators.Css(f"[aria-label^='{id_}']"))
                continue

    def query_all_by_label_text(self, text: str) -> Generator[WebElement, None, None]:
        labels: WebElement = self.query_all_by(
            locators.XPath(f'//label[text() = "{text}"]')
        )
        for label in labels:
            id_ = label.get_attribute("for")
            yield self.get_by(locators.Id(id_))

    def find_all_by_label_text(self, text: str) -> Generator[WebElement, None, None]:
        labels: WebElement = self.find_all_by(
            locators.XPath(f'//label[text() = "{text}"]')
        )
        for label in labels:
            id_ = label.get_attribute("for")
            yield self.get_by(locators.Id(id_))

    # By alt text
    def get_by_alt_text(self, value: str) -> WebElement:
        locator = locators.XPath(f'//*[@alt = "{value}"]')
        return self.get_by(locator)

    def query_by_alt_text(self, value: str) -> Optional[WebElement]:
        locator = locators.XPath(f'//*[@alt = "{value}"]')
        return self.query_by(locator)

    def find_by_alt_text(self, value: str) -> WebElement:
        locator = locators.XPath(f'//*[@alt = "{value}"]')
        return self.find_by(locator)

    def get_all_by_alt_text(self, value: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[@alt = "{value}"]')
        return self.get_all_by(locator)

    def query_all_by_alt_text(self, value: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[@alt = "{value}"]')
        return self.query_all_by(locator)

    def find_all_by_alt_text(self, value: str) -> List[WebElement]:
        locator = locators.XPath(f'//*[@alt = "{value}"]')
        return self.find_all_by(locator)

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
