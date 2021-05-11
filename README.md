# Selenium Testing Library

A Python Selenium framework inspired by [Testing Library](https://testing-library.com/).

```python
from selenium import webdriver
from selenium_testing_library import Screen


screen = Screen(webdriver.Chrome())
screen.driver.get("http://www.google.com/ncr")
screen.get_by_text("Aceito").click()
screen.get_by_role("combobox").send_keys("Dogs" + screen.Keys.RETURN)
# Find waits until the results become available
screen.find_by_text("Dog - Wikipedia")
assert screen.query_by_text("Cats") is None
```

## Local development

```shell
poetry install && poetry shell
# Download the chromedriver and run the tests
pytest --driver Chrome --driver-path chromedriver
```
