# Selenium Testing Library

A Python Selenium framework inspired by [Testing Library](https://testing-library.com/).

```python
from selenium_testing_library import Screen
screen = Screen(driver)

screen.driver.get("https://google.com")
screen.find_by_role("textbox").send_keys("Snakes")
screen.get_by_text("Google Search").click()
assert screen.query_by_text("Images for snakes") is not None
```

Use it inside your page object classes

```python
from selenium_testing_library import Screen


class GooglePage:
    SEARCH_BOX = ""
    SEARCH_BTN = ""

    def __init__(self, driver):
        self.screen = Screen(driver)
    
    def search_for_snakes(self):
        self.screen.find_by_role("textbox").send_keys("Snakes")
        self.screen.get_by_text("Google Search").click()
```


## Local development

```shell
poetry install && poetry shell
# Run tests
pytest --driver Chrome --driver-path chromedriver
```