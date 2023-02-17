import pytest  # type: ignore
from selenium import webdriver  # type: ignore


def pytest_addoption(parser):
    parser.addoption(
        "--selenium-headless",
        action="store_true",
        help="Run the browser in headless mode",
    )


@pytest.fixture(scope="session")
def session_selenium(request):
    headless = request.config.getoption("--selenium-headless")
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("headless")
    return webdriver.Chrome(options=chrome_options)
