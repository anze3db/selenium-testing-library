import json
from pathlib import Path
from typing import Any, Callable, Generic, List, Optional, TypeVar, Union

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

testing_library = (Path(__file__).parent / Path("main.js")).read_text()

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

    def execute_script(self, script: str, *args) -> List[WebElement]:
        ...


DriverType = TypeVar("DriverType", bound=ElementsFinder)


class Screen(Generic[DriverType]):
    def __init__(self, driver: DriverType):
        self.driver = driver
        self._finder: ElementsFinder = driver

    def _find_elements(self, locator: Locator) -> List[WebElement]:
        loc = self._ensure_locator(locator)
        if not isinstance(
            loc,
            (
                locators.Role,
                locators.Text,
                locators.PlaceholderText,
                locators.LabelText,
                locators.AltText,
                locators.Title,
                locators.TestId,
                locators.DisplayValue,
            ),
        ):
            return self._finder.find_elements(*loc)
        script_to_run = loc._testing_library_js_str()
        try:
            # Optimistically run the query, if __stl__ isn't defined on the page we'll get a JavaScript exception
            return self._finder.execute_script(script_to_run)
        except WebDriverException:
            # We assume that the error was `__stl__ is not defined` so we add __stl__ to the DOM and run the command again
            return self._finder.execute_script(f"{testing_library};{script_to_run}")

    def _ensure_locator(self, locator: Locator) -> locators.Locator:
        if isinstance(locator, locators.Locator):
            return locator
        by, selector = locator
        return by_to_locator[by](selector)

    def get_by(self, locator: Locator) -> WebElement:
        els = self._find_elements(locator)

        if not els:
            raise NoSuchElementException(self._get_no_element_message(locator))

        if len(els) > 1:
            raise MultipleSuchElementsException(
                self._get_multiple_elements_message(locator, els)
            )

        return els[0]

    def query_by(self, locator: Locator) -> Optional[WebElement]:
        els = self._find_elements(locator)

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
        try:
            els = self.wait_for(
                lambda _: self._find_elements(locator),
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
        els = self._find_elements(locator)
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
        try:
            return self.wait_for(
                lambda _: self._find_elements(locator),
                timeout=timeout,
                poll_frequency=poll_frequency,
            )
        except TimeoutException:
            raise NoSuchElementException(self._get_no_element_message(locator))

    ## Testing Library Selectors
    # By role
    def get_by_role(
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
    ) -> WebElement:
        return self.get_by(
            locators.Role(
                role,
                exact=exact,
                hidden=hidden,
                name=name,
                description=description,
                selected=selected,
                checked=checked,
                pressed=pressed,
                current=current,
                expanded=expanded,
                queryFallbacks=queryFallbacks,
                level=level,
            )
        )

    def query_by_role(
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
    ) -> Optional[WebElement]:
        return self.get_by(
            locators.Role(
                role,
                exact=exact,
                hidden=hidden,
                name=name,
                description=description,
                selected=selected,
                checked=checked,
                pressed=pressed,
                current=current,
                expanded=expanded,
                queryFallbacks=queryFallbacks,
                level=level,
            )
        )

    def find_by_role(
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
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.Role(
                role,
                exact=exact,
                hidden=hidden,
                name=name,
                description=description,
                selected=selected,
                checked=checked,
                pressed=pressed,
                current=current,
                expanded=expanded,
                queryFallbacks=queryFallbacks,
                level=level,
            ),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_role(
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
    ) -> List[WebElement]:
        return self.get_all_by(
            locators.Role(
                role,
                exact=exact,
                hidden=hidden,
                name=name,
                description=description,
                selected=selected,
                checked=checked,
                pressed=pressed,
                current=current,
                expanded=expanded,
                queryFallbacks=queryFallbacks,
                level=level,
            )
        )

    def query_all_by_role(
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
    ) -> List[WebElement]:
        return self.query_all_by(
            locators.Role(
                role,
                exact=exact,
                hidden=hidden,
                name=name,
                description=description,
                selected=selected,
                checked=checked,
                pressed=pressed,
                current=current,
                expanded=expanded,
                queryFallbacks=queryFallbacks,
                level=level,
            )
        )

    def find_all_by_role(
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
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Role(
                role,
                exact=exact,
                hidden=hidden,
                name=name,
                description=description,
                selected=selected,
                checked=checked,
                pressed=pressed,
                current=current,
                expanded=expanded,
                queryFallbacks=queryFallbacks,
                level=level,
            ),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By text
    def get_by_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        ignore: Union[str, bool] = "script, style",
    ) -> WebElement:
        return self.get_by(
            locators.Text(text, selector=selector, exact=exact, ignore=ignore)
        )

    def query_by_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        ignore: Union[str, bool] = "script, style",
    ) -> Optional[WebElement]:
        return self.query_by(
            locators.Text(text, selector=selector, exact=exact, ignore=ignore)
        )

    def find_by_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        ignore: Union[str, bool] = "script, style",
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.Text(text, selector=selector, exact=exact, ignore=ignore),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        ignore: Union[str, bool] = "script, style",
    ) -> List[WebElement]:
        return self.get_all_by(
            locators.Text(text, selector=selector, exact=exact, ignore=ignore)
        )

    def query_all_by_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        ignore: Union[str, bool] = "script, style",
    ) -> List[WebElement]:
        return self.query_all_by(
            locators.Text(text, selector=selector, exact=exact, ignore=ignore)
        )

    def find_all_by_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        ignore: Union[str, bool] = "script, style",
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Text(text, selector=selector, exact=exact, ignore=ignore),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By placeholder
    def get_by_placeholder_text(self, text: str, *, exact: bool = True) -> WebElement:
        return self.get_by(locators.PlaceholderText(text, exact=exact))

    def query_by_placeholder_text(
        self, text: str, *, exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.PlaceholderText(text, exact=exact))

    def find_by_placeholder_text(
        self,
        text: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.PlaceholderText(text, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_placeholder_text(
        self, text: str, *, exact: bool = True
    ) -> List[WebElement]:
        return self.get_all_by(locators.PlaceholderText(text, exact=exact))

    def query_all_by_placeholder_text(
        self, text: str, *, exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(locators.PlaceholderText(text, exact=exact))

    def find_all_by_placeholder_text(
        self,
        text: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.PlaceholderText(text, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By label text
    def get_by_label_text(
        self, text: str, *, selector: str = "*", exact: bool = True
    ) -> WebElement:
        return self.get_by(locators.LabelText(text, selector=selector, exact=exact))

    def query_by_label_text(
        self, text: str, *, selector: str = "*", exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.LabelText(text, selector=selector, exact=exact))

    def find_by_label_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.LabelText(text, selector=selector, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_label_text(
        self, text: str, *, selector: str = "*", exact: bool = True
    ) -> List[WebElement]:
        return self.get_all_by(locators.LabelText(text, selector=selector, exact=exact))

    def query_all_by_label_text(
        self, text: str, *, selector: str = "*", exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(
            locators.LabelText(text, selector=selector, exact=exact)
        )

    def find_all_by_label_text(
        self,
        text: str,
        *,
        selector: str = "*",
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.LabelText(text, selector=selector, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By alt text
    def get_by_alt_text(self, text: str, *, exact: bool = True) -> WebElement:
        return self.get_by(locators.AltText(text, exact=exact))

    def query_by_alt_text(
        self, text: str, *, exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.AltText(text, exact=exact))

    def find_by_alt_text(
        self,
        text: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.AltText(text, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_alt_text(self, text: str, *, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.AltText(text, exact=exact))

    def query_all_by_alt_text(
        self, text: str, *, exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(locators.AltText(text, exact=exact))

    def find_all_by_alt_text(
        self,
        text: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.AltText(text, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By title
    def get_by_title(self, title: str, *, exact: bool = True) -> WebElement:
        return self.get_by(locators.Title(title, exact=exact))

    def query_by_title(self, title: str, *, exact: bool = True) -> Optional[WebElement]:
        return self.query_by(locators.Title(title, exact=exact))

    def find_by_title(
        self,
        title: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.Title(title, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_title(self, title: str, *, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.Title(title, exact=exact))

    def query_all_by_title(self, title: str, *, exact: bool = True) -> List[WebElement]:
        return self.query_all_by(locators.Title(title, exact=exact))

    def find_all_by_title(
        self,
        title: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Title(title, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By test id
    def get_by_test_id(self, text: str, *, exact: bool = True) -> WebElement:
        return self.get_by(locators.TestId(text, exact=exact))

    def query_by_test_id(
        self, text: str, *, exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.TestId(text, exact=exact))

    def find_by_test_id(
        self,
        text: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.TestId(text, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_test_id(self, text: str, *, exact: bool = True) -> List[WebElement]:
        return self.get_all_by(locators.TestId(text, exact=exact))

    def query_all_by_test_id(
        self, text: str, *, exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(locators.TestId(text, exact=exact))

    def find_all_by_test_id(
        self,
        text: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.TestId(text, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By display value
    def get_by_display_value(self, value: str, *, exact: bool = True) -> WebElement:
        return self.get_by(locators.DisplayValue(value, exact=exact))

    def query_by_display_value(
        self, value: str, *, exact: bool = True
    ) -> Optional[WebElement]:
        return self.query_by(locators.DisplayValue(value, exact=exact))

    def find_by_display_value(
        self,
        value: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> WebElement:
        return self.find_by(
            locators.DisplayValue(value, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_display_value(
        self, value: str, *, exact: bool = True
    ) -> List[WebElement]:
        return self.get_all_by(locators.DisplayValue(value, exact=exact))

    def query_all_by_display_value(
        self, value: str, *, exact: bool = True
    ) -> List[WebElement]:
        return self.query_all_by(locators.DisplayValue(value, exact=exact))

    def find_all_by_display_value(
        self,
        value: str,
        *,
        exact: bool = True,
        timeout: float = 5,
        poll_frequency: float = 0.5,
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.DisplayValue(value, exact=exact),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    ## Selenium Selectors
    # By css
    def get_by_css(self, css: str) -> WebElement:
        return self.get_by(locators.Css(css))

    def query_by_css(self, css: str) -> Optional[WebElement]:
        return self.query_by(locators.Css(css))

    def find_by_css(
        self, css: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.Css(css), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_css(self, css: str) -> List[WebElement]:
        return self.get_all_by(locators.Css(css))

    def query_all_by_css(self, css: str) -> List[WebElement]:
        return self.query_all_by(locators.Css(css))

    def find_all_by_css(
        self, css: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Css(css), timeout=timeout, poll_frequency=poll_frequency
        )

    # By xpath
    def get_by_xpath(self, xpath: str) -> WebElement:
        return self.get_by(locators.XPath(xpath))

    def query_by_xpath(self, xpath: str) -> Optional[WebElement]:
        return self.query_by(locators.XPath(xpath))

    def find_by_xpath(
        self, xpath: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.XPath(xpath), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_xpath(self, xpath: str) -> List[WebElement]:
        return self.get_all_by(locators.XPath(xpath))

    def query_all_by_xpath(self, xpath: str) -> List[WebElement]:
        return self.query_all_by(locators.XPath(xpath))

    def find_all_by_xpath(
        self, xpath: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.XPath(xpath), timeout=timeout, poll_frequency=poll_frequency
        )

    # By id
    def get_by_id(self, id: str) -> WebElement:
        return self.get_by(locators.Id(id))

    def query_by_id(self, id: str) -> Optional[WebElement]:
        return self.query_by(locators.Id(id))

    def find_by_id(
        self, id: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.Id(id), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_id(self, id: str) -> List[WebElement]:
        return self.get_all_by(locators.Id(id))

    def query_all_by_id(self, id: str) -> List[WebElement]:
        return self.query_all_by(locators.Id(id))

    def find_all_by_id(
        self, id: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Id(id), timeout=timeout, poll_frequency=poll_frequency
        )

    # By name
    def get_by_name(self, name: str) -> WebElement:
        return self.get_by(locators.Name(name))

    def query_by_name(self, name: str) -> Optional[WebElement]:
        return self.query_by(locators.Name(name))

    def find_by_name(
        self, name: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.Name(name), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_name(self, name: str) -> List[WebElement]:
        return self.get_all_by(locators.Name(name))

    def query_all_by_name(self, name: str) -> List[WebElement]:
        return self.query_all_by(locators.Name(name))

    def find_all_by_name(
        self, name: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.Name(name), timeout=timeout, poll_frequency=poll_frequency
        )

    # By tag name
    def get_by_tag_name(self, name: str) -> WebElement:
        return self.get_by(locators.TagName(name))

    def query_by_tag_name(self, name: str) -> Optional[WebElement]:
        return self.query_by(locators.TagName(name))

    def find_by_tag_name(
        self, name: str, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.TagName(name), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_tag_name(self, name: str) -> List[WebElement]:
        return self.get_all_by(locators.TagName(name))

    def query_all_by_tag_name(self, name: str) -> List[WebElement]:
        return self.query_all_by(locators.TagName(name))

    def find_all_by_tag_name(
        self, name: str, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.TagName(name), timeout=timeout, poll_frequency=poll_frequency
        )

    # By link text
    def get_by_link_text(self, value: str) -> WebElement:
        return self.get_by(locators.LinkText(value))

    def query_by_link_text(self, value: str) -> Optional[WebElement]:
        return self.query_by(locators.LinkText(value))

    def find_by_link_text(
        self, value: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.LinkText(value), timeout=timeout, poll_frequency=poll_frequency
        )

    def get_all_by_link_text(self, value: str) -> List[WebElement]:
        return self.get_all_by(locators.LinkText(value))

    def query_all_by_link_text(self, value: str) -> List[WebElement]:
        return self.query_all_by(locators.LinkText(value))

    def find_all_by_link_text(
        self, value: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.LinkText(value), timeout=timeout, poll_frequency=poll_frequency
        )

    # By partial text
    def get_by_partial_link_text(self, text: str) -> WebElement:
        return self.get_by(locators.PartialLinkText(text))

    def query_by_partial_link_text(self, text: str) -> Optional[WebElement]:
        return self.query_by(locators.PartialLinkText(text))

    def find_by_partial_link_text(
        self, text: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.PartialLinkText(text),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_partial_link_text(self, text: str) -> List[WebElement]:
        return self.get_all_by(locators.PartialLinkText(text))

    def query_all_by_partial_link_text(self, text: str) -> List[WebElement]:
        return self.query_all_by(locators.PartialLinkText(text))

    def find_all_by_partial_link_text(
        self, text: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.PartialLinkText(text),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    # By class name
    def get_by_class_name(self, name: str) -> WebElement:
        return self.get_by(locators.ClassName(name))

    def query_by_class_name(self, name: str) -> Optional[WebElement]:
        return self.query_by(locators.ClassName(name))

    def find_by_class_name(
        self, name: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> WebElement:
        return self.find_by(
            locators.ClassName(name),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def get_all_by_class_name(self, name: str) -> List[WebElement]:
        return self.get_all_by(locators.ClassName(name))

    def query_all_by_class_name(self, name: str) -> List[WebElement]:
        return self.query_all_by(locators.ClassName(name))

    def find_all_by_class_name(
        self, name: str, *, timeout: float = 5, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        return self.find_all_by(
            locators.ClassName(name),
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for(
        self,
        method: Callable[[DriverType], T],
        *,
        timeout: float = 5,
        poll_frequency: float = 0.5,
        ignored_exceptions: Optional[bool] = None,
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
        self._finder: ElementsFinder = element.parent

    def _find_elements(self, locator: Locator) -> List[WebElement]:
        loc = self._ensure_locator(locator)
        ex = "true" if loc.exact else "false"
        escaped_selector = json.dumps(loc.selector)

        if not isinstance(
            loc,
            (
                locators.Role,
                locators.Text,
                locators.PlaceholderText,
                locators.LabelText,
                locators.AltText,
                locators.Title,
                locators.TestId,
                locators.DisplayValue,
            ),
        ):
            return self.element.find_elements(*loc)

        script_to_run = loc._testing_library_js_str().replace(
            "(document", "(arguments[0]"
        )
        try:
            return self.element.parent.execute_script(
                script_to_run,
                self.element,
            )
        except WebDriverException:
            return self.element.parent.execute_script(
                f"{testing_library};{script_to_run}",
                self.element,
            )

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
