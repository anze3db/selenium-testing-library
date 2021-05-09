from __future__ import annotations

from typing import List, Tuple
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Remote as Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Locator: Tuple[str, str]


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
    #     return self.element.get_property()

    # def send_keys(self, keys)
    #     return self.element.send_keys

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
    def __init__(
        self,
        driver: Driver,
    ):
        self.driver = driver
        self.waiter = WebDriverWait(self.driver, 1)

    def get(self, locator: Tuple[str, str]):
        els = self.driver.find_elements(*locator)

        if not els:
            raise Exception("No element matched")

        if len(els) > 1:
            raise Exception("more than 1 element")

        return Element(els[0], self.driver)

    def query(self, locator: Tuple[str, str]):
        els = self.driver.find_elements(*locator)
        if not els:
            return None
        if len(els) > 1:
            raise Exception("more than 1 element")

        return Element(els[0], self.driver)

    def find(self, locator: Tuple[str, str]):
        els = self.waiter.until(
            EC.presence_of_all_elements_located(locator), self.driver
        )
        if not els:
            raise Exception("No elements")
        if len(els) > 1:
            raise Exception("More than 1 element")
        return Element(els[0], self.driver)

    def get_all(self, locator: Tuple[str, str]):
        els = list(
            Element(el, self.driver) for el in self.driver.find_elements(*locator)
        )
        if not els:
            raise Exception("No elements matched")

        return els

    def query_all(self, locator: Tuple[str, str]):
        try:
            return self.get_all(locator)
        except:
            return []

    def find_all(self, locator: Tuple[str, str]):
        els = list(
            Element(el, self.driver)
            for el in self.waiter.until(EC.presence_of_all_elements_located(locator))
        )
        if not els:
            raise Exception()

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


class Locator:
    def __init__(self, css_selector: str):
        self.value = css_selector

    def __iter__(self):
        yield By.CSS_SELECTOR
        yield self.value


class LocatorXPath:
    def __init__(self, xpath_selector: str):
        self.value = xpath_selector

    def __iter__(self):
        yield By.XPATH
        yield self.value


__all__ = ["Element", "Page", "Locator", "LocatorXPath"]
