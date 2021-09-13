from typing import Any, Callable, Generic, List, Optional, TypeVar

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing_extensions import Protocol

from . import locators

Locator = locators.LocatorType

T = TypeVar("T")


class MultipleSuchElementsException(WebDriverException):
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


class ElementsFinder(Protocol):
    def find_elements(
        self, by: str = locators.By.ID, value: Optional[str] = None
    ) -> List[WebElement]:
        ...


DriverType = TypeVar("DriverType", bound=ElementsFinder)


class Screen(Generic[DriverType]):
    def __init__(self, driver: DriverType):
        self.driver = driver
        self._finder: ElementsFinder = driver

    def _ensure_locator(self, locator: Locator) -> locators.Locator:
        if isinstance(locator, locators.Locator):
            return locator
        by, selector = locator
        return by_to_locator[by](selector)

    def get_by(self, locator: Locator) -> WebElement:
        loc = self._ensure_locator(locator)
        els = loc.find_elements(self._finder)

        if not els:
            raise NoSuchElementException(self._get_no_element_message(locator))

        if len(els) > 1:
            raise MultipleSuchElementsException(
                self._get_multiple_elements_message(locator, els)
            )

        return els[0]

    def query_by(self, locator: Locator) -> Optional[WebElement]:
        loc = self._ensure_locator(locator)
        els = loc.find_elements(self._finder)

        if not els:
            return None
        if len(els) > 1:
            raise MultipleSuchElementsException(
                self._get_multiple_elements_message(locator, els)
            )

        return els[0]

    def find_by(
        self, locator: Locator, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        loc = self._ensure_locator(locator)
        try:
            els = self.wait_for(
                loc.find_elements,
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException(self._get_no_element_message(locator))
        if len(els) > 1:
            raise MultipleSuchElementsException(
                self._get_multiple_elements_message(locator, els)
            )
        return els[0]

    def get_all_by(self, locator: Locator) -> List[WebElement]:
        loc = self._ensure_locator(locator)
        els = loc.find_elements(self._finder)
        if not els:
            raise NoSuchElementException(self._get_no_element_message(locator))

        return els

    def query_all_by(self, locator: Locator) -> List[WebElement]:
        try:
            return self.get_all_by(locator)
        except NoSuchElementException:
            return []

    def find_all_by(
        self, locator: Locator, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        loc = self._ensure_locator(locator)

        try:
            return self.wait_for(
                loc.find_elements,
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException(self._get_no_element_message(locator))

    # By role
    def get_by_role(self, role: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.Role(role, exact))

    def query_by_role(self, role: str, exact: bool = True) -> Optional[WebElement]:
        return self.get_by(locators.Role(role, exact))

    def find_by_role(
        self,
        role: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.Role(role, exact), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_role(self, role: str, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.Role(role, exact))

    def query_all_by_role(self, role: str, exact: bool = True) -> List[WebElement]:
        return self.query_all_by(locators.Role(role, exact))

    def find_all_by_role(
        self,
        role: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Role(role, exact), timeout=timeout, poll_frequency=poll_frequency
        )

    # By text
    def get_by_text(self, text: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.Text(text, exact))

    def query_by_text(self, text: str, exact: bool = True) -> Optional[WebElement]:
        return self.query_by(locators.Text(text, exact))

    def find_by_text(
        self,
        text: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.Text(text, exact), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_text(self, text: str, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.Text(text, exact))

    def query_all_by_text(self, text: str, exact: bool = True) -> List[WebElement]:
        return self.query_all_by(locators.Text(text, exact))

    def find_all_by_text(
        self,
        text: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Text(text, exact), timeout=timeout, poll_frequency=poll_frequency
        )

    # By placeholder
    def get_by_placeholder_text(self, value: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.PlaceholderText(value, exact))

    def query_by_placeholder_text(
        self, value: str, exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.PlaceholderText(value, exact))

    def find_by_placeholder_text(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.PlaceholderText(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_placeholder_text(
        self, value: str, exact: bool = True
    ) -> List[WebElement]:
        return self.get_all_by(locators.PlaceholderText(value, exact))

    def query_all_by_placeholder_text(
        self, value: str, exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(locators.PlaceholderText(value, exact))

    def find_all_by_placeholder_text(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.PlaceholderText(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By label text
    def get_by_label_text(self, text: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.LabelText(text, exact))

    def query_by_label_text(
        self, text: str, exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.LabelText(text, exact))

    def find_by_label_text(
        self,
        text: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.LabelText(text, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_label_text(self, text: str, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.LabelText(text, exact))

    def query_all_by_label_text(
        self, text: str, exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(locators.LabelText(text, exact))

    def find_all_by_label_text(
        self,
        text: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.LabelText(text, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By alt text
    def get_by_alt_text(self, value: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.AltText(value, exact))

    def query_by_alt_text(self, value: str, exact: bool = True) -> Optional[WebElement]:
        return self.query_by(locators.AltText(value, exact))

    def find_by_alt_text(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.AltText(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_alt_text(self, value: str, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.AltText(value, exact))

    def query_all_by_alt_text(self, value: str, exact: bool = True) -> List[WebElement]:
        return self.query_all_by(locators.AltText(value, exact))

    def find_all_by_alt_text(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.AltText(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By title
    def get_by_title(self, value: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.Title(value, exact))

    def query_by_title(self, value: str, exact: bool = True) -> Optional[WebElement]:
        return self.query_by(locators.Title(value, exact))

    def find_by_title(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.Title(value, exact), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_title(self, value: str, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.Title(value, exact))

    def query_all_by_title(self, value: str, exact: bool = True) -> List[WebElement]:
        return self.query_all_by(locators.Title(value, exact))

    def find_all_by_title(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Title(value, exact), timeout=timeout, poll_frequency=poll_frequency
        )

    # By test id
    def get_by_test_id(self, value: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.TestId(value, exact))

    def query_by_test_id(self, value: str, exact: bool = True) -> Optional[WebElement]:
        return self.query_by(locators.TestId(value, exact))

    def find_by_test_id(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.TestId(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_test_id(self, value: str, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.TestId(value, exact))

    def query_all_by_test_id(self, value: str, exact: bool = True) -> List[WebElement]:
        return self.query_all_by(locators.TestId(value, exact))

    def find_all_by_test_id(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.TestId(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By display value
    def get_by_display_value(self, value: str, exact: bool = True) -> WebElement:
        return self.get_by(locators.DisplayValue(value, exact))

    def query_by_display_value(
        self, value: str, exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.DisplayValue(value, exact))

    def find_by_display_value(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.DisplayValue(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_display_value(
        self, value: str, exact: bool = True
    ) -> List[WebElement]:
        return self.get_all_by(locators.DisplayValue(value, exact))

    def query_all_by_display_value(
        self, value: str, exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(locators.DisplayValue(value, exact))

    def find_all_by_display_value(
        self,
        value: str,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.DisplayValue(value, exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By css
    def get_by_css(self, value: str) -> WebElement:
        return self.get_by(locators.Css(value))

    def query_by_css(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.Css(value))

    def find_by_css(
        self, value: str, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.Css(value), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_css(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.Css(value))

    def query_all_by_css(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.Css(value))

    def find_all_by_css(
        self, value: str, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Css(value), timeout=timeout, poll_frequency=poll_frequency
        )

    # By xpath
    def get_by_xpath(self, value: str) -> WebElement:
        return self.get_by(locators.XPath(value))

    def query_by_xpath(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.XPath(value))

    def find_by_xpath(
        self, value: str, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.XPath(value), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_xpath(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.XPath(value))

    def query_all_by_xpath(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.XPath(value))

    def find_all_by_xpath(
        self, value: str, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.XPath(value), timeout=timeout, poll_frequency=poll_frequency
        )

    def wait_for(
        self,
        method: Callable[[DriverType], T],
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

    def wait_for_stale(
        self, element: WebElement, *, timeout: float = 5, poll_frequency: float = 0.5
    ):
        return self.wait_for(
            EC.staleness_of(element), timeout=timeout, poll_frequency=poll_frequency
        )

    def _get_no_element_message(self, locator: Locator):
        return f"No element found with locator {locator}"

    def _get_multiple_elements_message(self, locator: Locator, els: List[WebElement]):
        el_str = ""
        for i, el in enumerate(els):
            el_str += f"{i}. {' '.join(el.get_attribute('outerHTML').splitlines())}\n"
        raise MultipleSuchElementsException(
            f"{len(els)} elements found with locator {locator}:\n{el_str}"
        )


class Within(Screen[WebElement]):
    def __init__(self, element: WebElement):
        self.element = element
        self._finder: ElementsFinder = element

    def wait_for(
        self,
        method: Callable[[WebElement], T],
        *,
        timeout: float = 5,
        poll_frequency: float = 0.5,
        ignored_exceptions: Optional[Any] = None,
    ) -> T:
        return WebDriverWait(
            self.element,
            timeout=timeout,
            poll_frequency=poll_frequency,
            ignored_exceptions=ignored_exceptions,
        ).until(method)

    def _get_no_element_message(self, locator: Locator):
        return f"No element found with locator {locator}:\n{self.element.get_attribute('outerHTML')}"


__all__ = [
    "Screen",
    "Within",
    "MultipleSuchElementsException",
    "NoSuchElementException",
    "locators",
]
