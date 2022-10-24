# Selenium Testing Library

[![PyPI version](https://badge.fury.io/py/selenium-testing-library.svg)](https://badge.fury.io/py/selenium-testing-library)
[![test](https://github.com/anze3db/selenium-testing-library/actions/workflows/main.yml/badge.svg)](https://github.com/anze3db/selenium-testing-library/actions/workflows/main.yml) [![codecov](https://codecov.io/gh/anze3db/selenium-testing-library/branch/main/graph/badge.svg?token=L1M7HO3DL7)](https://codecov.io/gh/anze3db/selenium-testing-library)

Slenium Testing Library (STL) is a Python library for Selenium inspired by [Testing-Library](https://testing-library.com/).

## Dependencies

- Python 3.7, 3.8, 3.9, 3.10, 3.11
- Selenium > 3.0.0

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

`get_by` returns the element matched and throws an exception if zero or more than one elements matched. This is the main function that we should be using to locate elements on a page.

`query_by` returns the element matched or `None` if no element matched. It throws and exception if more than 1 elements matched. Mostly used for asserting that an element is **not** present: `assert not screen.query_by_text("not on page")`.

`find_by` behaves like `get_by`, but uses a `WebDriverWait` to wait until the element is present in the DOM.

`get_all_by` returns a list of elements matched. It raises an exception if no elements matched.

`query_all_by` returns a list of elements matched. It returns an empty list when no elements matched.

`find_all_by` behaves like `get_all_by`, but uses a `WebDriverWait` to wait until the elements jare present in the DOM.

Examples:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_testing_library import Screen

screen = Screen(webdriver.Chrome())
screen.query_by((By.ID, "my_id")) # you can use regular tuples as if you were using Selenium's find_element()
screen.find_by((By.XPATH, "//div"), timeout=5, poll_frequency=0.5) # locators for searching through text also work
screen.get_by((By.CSS, ".my_class")) # Will throw an exception if the element is not found
```

For a more detail description check out the [Testing-Library](https://testing-library.com/docs/queries/about)'s documentation.

## Helper functions

`get_by_role(role_name)` Queries for elements by given role. Does not currently support default roles.
`get_by_label_text(text)` Queries for label elements that match the the text string and returns the corresponding input element.
`get_by_placeholder_text(text)` Queries elements with the matching placeholder attribute.
`get_by_text(text)` Queries elements where the content matches the provided text.
`get_by_display_value(value)` Queries inputs, textareas, or selects with matching display value.
`get_by_alt_text(text)` Queries elements with the matching alt attribute.
`get_by_title(text)` Queries elements with the matching title attribute.
`get_by_test_id(value)` Queries elements matching the `data-testid` value.
`get_by_css(css)` Queries elements matching the specified css selector.
`get_by_xpath(xpath)` Queries elements matching the specified xpath selector.

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

## Locators

Locators are utility classes that simplify writing (By.XXX, selector) tuples. They can be used even when using native selenium functions `driver.find_element(locators.Id("my_id"))`.

Available locators:

`Css`, `XPath`, `Id`, `Name`, `TagName`, `LinkText`, `PartialLinkText`, `ClassName`, `Role`, `Text`, `PlaceholderText`, `LabelText`, `AltText`, `Title`, `TestId`, `DisplayValu`

Examples:

```python
from selenium import webdriver
from selenium_testing_library import Screen, locators

screen.query_by(locators.Id("my_id"))
screen.find_by(locators.XPath("//div"), timeout=5, poll_frequency=0.5)
screen.get_by(locators.Css(".my_class"))
screen.get_all_by(locators.Text("my text"))
screen.get_by(locators.LinkText("my link text"))
screen.query_all_by(locators.ClassName("my-class-name"))
```

## Wait functions

`wait_for(condition_function)` Waits until condition function returns a truthy value.
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
