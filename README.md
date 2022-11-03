# Selenium Testing Library

[![PyPI version](https://badge.fury.io/py/selenium-testing-library.svg)](https://badge.fury.io/py/selenium-testing-library)
[![test](https://github.com/anze3db/selenium-testing-library/actions/workflows/main.yml/badge.svg)](https://github.com/anze3db/selenium-testing-library/actions/workflows/main.yml) [![codecov](https://codecov.io/gh/anze3db/selenium-testing-library/branch/main/graph/badge.svg?token=L1M7HO3DL7)](https://codecov.io/gh/anze3db/selenium-testing-library)

Selenium Testing Library (STL) is a Python library implementing [Testing-Library](https://testing-library.com/) in Selenium.

## Dependencies

- Python 3.7, 3.8, 3.9, 3.10, 3.11
- [`selenium`](https://pypi.org/project/selenium/) >= 3.0.0, [`typing-extensions`](https://pypi.org/project/typing-extensions/) >= 4.0.0
## Installation

```
pip install selenium-testing-library
```

## Quick Start

```python
from selenium import webdriver
from selenium_testing_library import Screen

driver = webdriver.Chrome()
driver.open('https://google.com/')

screen = Screen(driver)
search_input = screen.find_by_title("Search")
search.send_keys("Dogs")
search_button = screen.find_by_text("Google Search")
search_button.click()
screen.wait_for_stale(search_button)
```

## Finding elements

STL implements the [Queries API](https://testing-library.com/docs/queries/about) from the Testing Library. The Testing Library queries `get_by`, `query_by`, `find_by`, and the multiple element equivalents `get_all_by`, `query_all_by`, `find_all_by` are used in places where you would normally use Selenium's `find_element` and `find_elements` functions.

 The difference between the different queries (`get_by`, `query_by`, `find_by`) is whether the query will throw an error if the element was not found (`get_by`), return `None` (`query_by`) or block, wait and retry until the element is found (`find_by`).

 * `get_by` returns the element matched and throws an exception if zero or more than one element matches. This is the main function that we should be using to locate elements on a page.
 * `query_by` returns the element matched or `None` if no element match. It throws an exception if more than one element matches. Mostly used for asserting that an element is **not** present: `assert not screen.query_by_text("not on page")`.
 * `find_by` behaves like `get_by`, but uses a `WebDriverWait` to wait until the element is present in the DOM.
 * `get_all_by` returns a list of elements matched. It raises an exception if no elements match.
 * `query_all_by` returns a list of elements matched. It returns an empty list when no elements match.
 * `find_all_by` behaves like `get_all_by`, but uses a `WebDriverWait` to wait until the elements are present in the DOM.

 When an element is found the queries return a Selenium [`WebElement`](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement) or a list containing Selenium [WebElement](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement)s when using `get_all_by`, `query_all_by`, `find_all_by`.

The queries accept a tuple containing the [By class identifier](https://selenium-python.readthedocs.io/api.html#locate-elements-by) and the search query, so they can be used with XPath, Css or any other native Selenium selector:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_testing_library import Screen

screen = Screen(webdriver.Chrome())
screen.get_by((By.CSS, ".my_class")) # Will throw an exception if the element is not found
screen.query_by((By.ID, "my_id")) # you can use regular tuples as if you were using Selenium's find_element()
screen.find_by((By.XPATH, "//div"), timeout=5, poll_frequency=0.5) # locators for searching through text also work
```

## Locator Classes

For convenience Locator classes can be used instead of the tuples:

```python
from selenium import webdriver
from selenium_testing_library import Screen, locators

screen = Screen(webdriver.Chrome())
screen.get_by(locators.Css(".my_class")) # Will throw an exception if the element is not found
screen.query_by(locators.Id("my_id")) # you can use regular tuples as if you were using Selenium's find_element()
screen.find_by(locators.XPath("//div"), timeout=5, poll_frequency=0.5) # locators for searching through text also work
```

## Testing Library Selectors

Besides all the Selenium native By selectors, the queries also support Testing Library's selectors:
 * [Role](https://testing-library.com/docs/queries/byrole)
 * [LabelText](https://testing-library.com/docs/queries/bylabeltext)
 * [PlaceholderText](https://testing-library.com/docs/queries/byplaceholdertext)
 * [Text](https://testing-library.com/docs/queries/bytext)
 * [DisplayValue](https://testing-library.com/docs/queries/bydisplayvalue)
 * [AltText](https://testing-library.com/docs/queries/byalttext)
 * [Title](https://testing-library.com/docs/queries/bytitle)
 * [TestId](https://testing-library.com/docs/queries/bytestid)

```python
from selenium import webdriver
from selenium_testing_library import Screen, locators

screen = Screen(webdriver.Chrome())
screen.get_by(locators.Text("My Text"))
screen.query_by(locators.Role("button", pressed=True))
screen.find_by(locators.TestId("my-test"), timeout=5, poll_frequency=0.5) # locators for searching through text also work
```
## Helper functions

For convenience helper functions on the screen class are available to avoid instantiating locator classes all over the place:

[`screen.get_by_role(role_name)`](https://testing-library.com/docs/queries/byrole) Queries for elements with the given role.
[`screen.get_by_label_text(text)`](https://testing-library.com/docs/queries/bylabeltext) Queries for label elements that match the text string and return the corresponding input element.
[`screen.get_by_placeholder_text(text)`](https://testing-library.com/docs/queries/byplaceholdertext) Queries elements with the matching placeholder attribute.
[`screen.get_by_text(text)`](https://testing-library.com/docs/queries/bytext) Queries elements where the content matches the provided text.
[`screen.get_by_display_value(value)`](https://testing-library.com/docs/queries/bydisplayvalue) Queries inputs, textareas, or selects with matching display value.
[`screen.get_by_alt_text(text)`](https://testing-library.com/docs/queries/byalttext) Queries elements with the matching alt attribute.
`screen.get_by_title(text)` Queries elements with the matching title attribute.
`screen.get_by_test_id(value)` Queries elements matching the `data-testid` value.
`screen.get_by_css(css)` Queries elements matching the specified css selector.
`screen.get_by_xpath(xpath)` Queries elements matching the specified xpath selector.

There are also `query_by_*`, `find_by_*`, `get_all_by_*`, `query_all_by_*`, `find_all_by_*`  equivalents.

**Note:** The selenium project has removed the `find_element_by_*` and `find_elements_by_*` helper functions in the [Selenium 4.3.0](https://github.com/SeleniumHQ/selenium/releases/tag/selenium-4.3.0) release, so I just want to state that the `screen` helper functions will never be deprecated or removed.

Examples:

```python
from selenium import webdriver
from selenium_testing_library import Screen

screen = Screen(webdriver.Chrome())
screen.query_by_role("role_name")
screen.get_by_label_text("label text")
screen.find_all_by_text("my text", timeout=5, poll_frequency=0.5)
screen.get_all_by_alt_text("alt text")
```

## Wait functions

`wait_for(condition_function)` Waits until the condition function returns a truthy value.
`wait_for_stale(element)` Waits until the element is removed from the DOM.

Examples:

```python
from selenium import webdriver
from selenium_testing_library import Screen, locators

screen = Screen(webdriver.Chrome())

# Wait for the element to be clickable:
element = screen.get_by_text("Submit")
screen.wait_for(lambda _: element.is_enabled(), timeout=5, poll_frequency=0.5)
# Wait for the element to be removed from the page:
screen.wait_for_stale(element)
```

## Querying within elements

`Within(element)` Used to limit the query to the children of the provided element

Example:

```python
from selenium import webdriver
from selenium_testing_library import Screen, Within

screen = Screen(webdriver.Chrome())
parent_element = screen.get_by_css(".container")
Within(parent_element).get_by_title("My title inside the container")
```

# Contributing

Setting up a local development environment

```shell
git clone https://github.com/anze3db/selenium-testing-library.git && cd selenium-testing-library
poetry install && poetry shell
# Make sure `chromedriver` is in your PATH, download from https://chromedriver.chromium.org/downloads
# run tests:
pytest --selenium-headless
# run tests and display coverage info:
pytest --selenium-headless --cov=selenium_testing_library --cov-report html

# To test on multiple Python versions make sure that py37, py38, py39 are
# installed on your system and available through python3.7, python3.8,
# python3.9. (Use pyenv and add the pyenv shims to your path
# `export PATH=$(pyenv root)/shims:$PATH`). Then run tox:
tox
```

# Releasing a new version

```shell
bumpver update --tag-num  # Wait and see if the CI is green
poetry build && poetry publish
```
