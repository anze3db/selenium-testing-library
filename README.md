# Selenium Testing Library

Slenium Testing Library (STL) is a Python library for Selenium inspired by [Testing Library](https://testing-library.com/).

```python
from selenium import webdriver
from selenium_testing_library import Screen


screen = Screen(webdriver.Chrome())
screen.driver.get("http://www.google.com/ncr")
screen.get_by_text("Accept").click()
screen.get_by_role("combobox").send_keys("Dogs" + Keys.RETURN)
# Find waits until the results become available
screen.find_by_text("Dog - Wikipedia")
assert screen.query_by_text("Cats") is None
```

## Query API Parity

| Testing Library          | STL                     | Status      |
| ------------------------ | ----------------------- | ----------- |
| `ByRole`                 | `by_role`               | ⚠️ Partial  |
| `ByLabelText`            | `by_label_text`         | ⚠️ Partial  |
| `ByPlaceholderText`      | `by_placeholder_text`   | ⚠️ Partial  |
| `ByText`                 | `by_text`               | ⚠️ Partial  |
| `ByDisplayValue`         | `by_display_value`      | ❌ Missing |
| `ByAltText`              | `by_al_text`            | ❌ Missing |
| `ByTitle`                | `by_title`              | ❌ Missing |
| `ByTestId`               | `by_test_id`            | ❌ Missing |

## Local development

```shell
poetry install && poetry shell
# Make sure `chromedriver` is in your PATH
pytest --headless
```
