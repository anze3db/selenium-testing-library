# Selenium Testing Library

Slenium Testing Library (STL) is a Python library for Selenium inspired by the [Testing Library](https://testing-library.com/).

```python
from selenium import webdriver
from selenium_testing_library import Screen


screen = Screen(webdriver.Chrome())
screen.driver.get("http://www.google.com/ncr")
screen.get_by_text("Accept").click()
screen.get_by_role("combobox").send_keys("Dogs" + Keys.RETURN)
# Find waits until the results become available
screen.find_by_text("Dog - Wikipedia", timeout=5, poll_frequency=0.5)
assert screen.query_by_text("Cats") is None
```

## API Parity with Testing Library

### Queries

| Testing Library          | STL                     | Status      |
| ------------------------ | ----------------------- | ----------- |
| `getBy`                  | `get_by`                | 🟢 Done     |
| `queryBy`                | `query_by`              | 🟢 Done     |
| `findBy`                 | `find_by`               | 🟢 Done     |
| `getAllBy`               | `get_all_by`            | 🟢 Done     |
| `queryAllBy`             | `query_all_by`          | 🟢 Done     |
| `findAllBy`              | `find_all_by`           | 🟢 Done     |

Examples:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_testing_library import Screen, locators

screen = Screen(webdriver.Chrome())
screen.get_by(locators.Css(".my_class"))  # locator classes are a shorthand for (By.CSS_SELECTOR, ".my_class"). All Selenium By.* options are supported
screen.query_by((By.ID, "my_id")) # you can use regular tuples/lists if you want to
screen.find_by(locators.Text("My text"), timeout=5, poll_frequency=0.5) # locators for searching through text also work
```

| Testing Library          | STL                     | Status      |
| ------------------------ | ----------------------- | ----------- |
| `ByRole`                 | `by_role`               | ⚠️ Partial  |
| `ByLabelText`            | `by_label_text`         | ⚠️ Partial  |
| `ByPlaceholderText`      | `by_placeholder_text`   | ⚠️ Partial  |
| `ByText`                 | `by_text`               | ⚠️ Partial  |
| `ByDisplayValue`         | `by_display_value`      | ❌ Missing |
| `ByAltText`              | `by_alt_text`           | ⚠️ Partial  |
| `ByTitle`                | `by_title`              | ❌ Missing |
| `ByTestId`               | `by_test_id`            | ❌ Missing |

Examples:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_testing_library import Screen, locators

screen = Screen(webdriver.Chrome())
screen.query_by_role("role_name")
screen.get_by_label_text("label text")
screen.find_all_by_text("my text", timeout=5, poll_frequency=0.5)
screen.get_all_by_alt_text("alt text")
```

### User Actions

| Testing Library          | STL                     | Status          |
| ------------------------ | ----------------------- | --------------- |
| `fireEvent`              | `N/A`                   | ❌ Not Planned  |
| `fireEvent[eventName]`   | `N/A`                   | ❌ Not Planned  |
| `createEvent[eventName]` | `N/A`                   | ❌ Not Planned  |

There is currently no plan to support the event API of Testing Library. Use the methods on `WebElement` instead.

| Testing Library             | STL                     | Status        |
| --------------------------- | ----------------------- | ------------- |
| `waitFor`                   | `wait_for`              | 🟢 Done       |
| `waitForElementToBeRemoved` | `wait_for_stale`        | 🟢 Done       |

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

## Local development

```shell
poetry install && poetry shell
# Make sure `chromedriver` is in your PATH, download from https://chromedriver.chromium.org/downloads
# run tests:
pytest --selenium-headless
# run tests and display coverage info:
pytest --selenium-headless --cov=selenium_testing_library --cov-report html
```
