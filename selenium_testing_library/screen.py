from __future__ import annotations
from enum import Enum
from typing import List, NewType, Tuple, Iterable
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # type: ignore
from selenium.webdriver import Remote as Driver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.remote.webelement import WebElement  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore


class ByOptions(Enum):
    CLASS_NAME: str = By.CLASS_NAME
    CSS_SELECTOR: str = By.CSS_SELECTOR
    ID: str = By.ID
    LINK_TEXT: str = By.LINK_TEXT
    PARTIAL_LINK_TEXT: str = By.PARTIAL_LINK_TEXT
    TAG_NAME: str = By.TAG_NAME
    XPATH: str = By.XPATH


ByType = NewType("ByType", ByOptions)

Locator = Tuple[ByType, str]


class MultipleElementsReturned(Exception):
    ...


class NoElementsReturned(Exception):
    ...


class Element:
    def __init__(self, element: WebElement, driver: Driver):
        self.element = element
        self.driver = driver
        self.waiter = WebDriverWait(self.driver, 5)

    def click(self):
        self.element.click()
        return self

    def clear(self):
        self.element.clear()
        return self

    # def get_attribute(self, name: str):
    #     return self.element.get_attribute(name)

    # def get_property(self, name: str):
    #     return self.element.get_property(name)

    # def send_keys(self, keys):
    #     return self.element.send_keys(keys)

    def wait_until_selected(self):
        self.waiter.until(EC.element_to_be_selected(self.element))
        return self

    def wait_until_stale(self):
        self.waiter.until(EC.staleness_of(self.element))
        return self

    def wait_until_visible(self):
        self.waiter.until(EC.visibility_of(self.element))
        return self


class Screen:

    TEST_ID_ATTRIBUTE = "data-testid"
    WAIT_TIMEOUT = 1

    def __init__(
        self,
        driver: Driver,
    ):
        self.driver = driver
        self.waiter = WebDriverWait(self.driver, self.WAIT_TIMEOUT)

    def get(self, locator: Locator):
        els = self.driver.find_elements(*locator)

        if not els:
            raise NoElementsReturned("No elements returned")

        if len(els) > 1:
            raise MultipleElementsReturned("Multiple elements returned")

        return Element(els[0], self.driver)

    def query(self, locator: Locator):
        els = self.driver.find_elements(*locator)
        if not els:
            return None
        if len(els) > 1:
            raise MultipleElementsReturned("Multiple elements returned")

        return Element(els[0], self.driver)

    def find(self, locator: Locator):
        try:
            els = self.waiter.until(
                EC.presence_of_all_elements_located(locator), self.driver
            )
        except TimeoutException:
            # TODO: Should this be a different kind of an exception?
            raise NoElementsReturned("No elements returned")
        if not els:
            raise NoElementsReturned("No elements returned")
        if len(els) > 1:
            raise MultipleElementsReturned("Multiple elements returned")
        return Element(els[0], self.driver)

    def get_all(self, locator: Locator):
        els = list(
            Element(el, self.driver) for el in self.driver.find_elements(*locator)
        )
        if not els:
            raise NoElementsReturned("No elements returned")

        return els

    def query_all(self, locator: Locator):
        try:
            return self.get_all(locator)
        except NoElementsReturned:
            return []

    def find_all(self, locator: Locator):
        try:
            els = list(
                Element(el, self.driver)
                for el in self.waiter.until(
                    EC.presence_of_all_elements_located(locator)
                )
            )
        except TimeoutException:
            # TODO: Should this be a different kind of an exception?
            raise NoElementsReturned("No elements returned")
        if not els:
            raise NoElementsReturned("No elements returned")

        return els

    # By role
    def get_by_role(self, role):
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.get(locator)

    def query_by_role(self, role: str):
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.get(locator)

    def find_by_role(self, role: str):
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.find(locator)

    def get_all_by_role(self, role):
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.get_all(locator)

    def query_all_by_role(self, role: str):
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.query_all(locator)

    def find_all_by_role(self, role: str):
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.find_all(locator)

    # By text
    def get_by_text(self, text: str):
        locator = (By.XPATH, f'//*[contains(text(), "{text}")]')
        return self.get(locator)

    def query_by_text(self, text: str):
        locator = (By.XPATH, f'//*[contains(text(), "{text}")]')
        return self.query(locator)

    def find_by_text(self, text: str):
        locator = (By.XPATH, f'//*[contains(text(), "{text}")]')
        return self.find(locator)

    def get_all_by_text(self, text: str):
        locator = (By.XPATH, f'//*[contains(text(), "{text}")]')
        return self.get_all(locator)

    def query_all_by_text(self, text: str):
        locator = (By.XPATH, f'//*[contains(text(), "{text}")]')
        return self.query_all(locator)

    def find_all_by_text(self, text: str):
        locator = (By.XPATH, f'//*[contains(text(), "{text}")]')
        return self.find_all(locator)

    # By value
    def get_by_value(self, value: str):
        locator = (By.XPATH, f'//*[contains(value(), "{value}")]')
        self.get(locator)

    def query_by_value(self, value: str):
        locator = (By.XPATH, f'//*[contains(value(), "{value}")]')
        self.query(locator)

    def find_by_value(self, value: str):
        locator = (By.XPATH, f'//*[contains(value(), "{value}")]')
        self.find(locator)

    def get_all_by_value(self, value: str):
        locator = (By.XPATH, f'//*[contains(value(), "{value}")]')
        self.get_all(locator)

    def query_all_by_value(self, value: str):
        locator = (By.XPATH, f'//*[contains(value(), "{value}")]')
        self.query_all(locator)

    def find_all_by_value(self, value: str):
        locator = (By.XPATH, f'//*[contains(value(), "{value}")]')
        self.find_all(locator)


__all__ = ["Screen"]
