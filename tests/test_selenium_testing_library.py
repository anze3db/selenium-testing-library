import pathlib

import pytest  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from selenium.webdriver.remote.webelement import WebElement  # type: ignore

from selenium_testing_library import (
    MultipleSuchElementsException,
    NoSuchElementException,
    Screen,
    __version__,
)


def test_version():
    assert __version__ == "0.0.1"


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("headless")
    return chrome_options


@pytest.fixture
def screen(selenium):
    return Screen(selenium)


def get_file_path(name):
    return "file://" + str(pathlib.Path(__file__).parent.absolute() / "pages" / name)


def test_get_by_text(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by_text("Email address"), WebElement)
    assert screen.query_by_text("address") is None
    assert len(screen.find_all_by_text("Item")) == 3


def test_get_by_label_text(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    input_field = screen.get_by_label_text("Email address")
    assert isinstance(input_field, WebElement)
    assert input_field.tag_name == "input"
    assert input_field.get_attribute("type") == "email"

    input_field = screen.query_by_label_text("Password")
    assert input_field.get_attribute("type") == "password"

    input_fields = list(screen.get_all_by_label_text("Same Label"))
    assert input_fields[0].get_attribute("type") == "text"
    assert input_fields[1].get_attribute("type") == "color"


@pytest.mark.skip("Not fully working yet")
def test_role(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by_role("button"), WebElement)


def test_basic_functions(screen):
    IMG_LOC = (By.CSS_SELECTOR, "img")
    A_LOC = (By.CSS_SELECTOR, "a")
    F_LOC = (By.CSS_SELECTOR, "footer")
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.get(IMG_LOC), WebElement)
    with pytest.raises(NoSuchElementException):
        screen.get(F_LOC)
    with pytest.raises(MultipleSuchElementsException):
        screen.get(A_LOC)

    # test_query(selenium):

    assert isinstance(screen.query(IMG_LOC), WebElement)
    assert screen.query(F_LOC) is None
    with pytest.raises(MultipleSuchElementsException):
        screen.query(A_LOC)

    # test_find(selenium):

    assert isinstance(screen.find(IMG_LOC), WebElement)
    with pytest.raises(NoSuchElementException):
        screen.find(F_LOC) is None
    with pytest.raises(MultipleSuchElementsException):
        screen.find(A_LOC)

    # test_get_all(selenium):

    assert isinstance(screen.get_all(IMG_LOC)[0], WebElement)
    with pytest.raises(NoSuchElementException):
        screen.get_all(F_LOC)
    assert len(screen.get_all(A_LOC)) > 1

    # test_query_all(selenium):

    assert isinstance(screen.query_all(IMG_LOC)[0], WebElement)
    assert len(screen.query_all(F_LOC)) == 0
    assert len(screen.query_all(A_LOC)) > 1

    # test_find_all(selenium):

    assert isinstance(screen.find_all(IMG_LOC)[0], WebElement)
    with pytest.raises(NoSuchElementException):
        screen.find_all(F_LOC)
    assert len(screen.find_all(A_LOC)) > 1
