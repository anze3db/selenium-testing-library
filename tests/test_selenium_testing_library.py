import pathlib

import pytest  # type: ignore
from selenium.webdriver.remote.webelement import WebElement  # type: ignore

from selenium_testing_library import (
    MultipleSuchElementsException,
    NoSuchElementException,
    Screen,
    Within,
    __version__,
    locators,
)


def test_version():
    assert __version__ == "0.0.1"


@pytest.fixture()
def screen(session_selenium):
    return Screen(session_selenium)


def get_file_path(name):
    return "file://" + str(pathlib.Path(__file__).parent.absolute() / "pages" / name)


def test_get_by_text(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by_text("Email address"), WebElement)
    assert screen.query_by_text("address") is None
    assert len(screen.find_all_by_text("Item")) == 3

    # Go through get with a text selector
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by(locators.Text("Email address")), WebElement)
    assert screen.query_by(locators.Text("address")) is None
    assert len(screen.find_all_by(locators.Text("Item"))) == 3


def test_get_by_label_text(screen: Screen):
    screen.driver.get(get_file_path("label.html"))
    username_fields = list(screen.get_all_by_label_text("Username"))
    assert len(username_fields) == 2  # TODO: Should be 5

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

def test_by_alt_text(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    assert isinstance(screen.get_by_alt_text("Some Image"), WebElement)

    screen.driver.get(get_file_path("form.html"))
    assert len(screen.find_all_by_alt_text("img2 alt")) == 2
    with pytest.raises(MultipleSuchElementsException):
        screen.query_by_alt_text("img2 alt")


@pytest.mark.skip("Not fully working yet")
def test_role(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by_role("button"), WebElement)


def test_within(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    el = screen.get_by(locators.Css("#subsection"))
    Within(el).get_by(locators.Css("input"))
    assert Within(el).query_by(locators.Css("label")) is None
    Within(el).find_by(locators.Css("input"))

    assert len(Within(el).get_all_by(locators.Css("div"))) == 3
    assert len(Within(el).query_all_by(locators.Css("div"))) == 3
    assert len(Within(el).find_all_by(locators.Css("div"))) == 3

    assert len(Within(el).query_all_by(locators.Css("img"))) == 0

    with pytest.raises(NoSuchElementException):
        Within(el).get_all_by(locators.Css("img"))

    with pytest.raises(NoSuchElementException):
        Within(el).find_all_by(locators.Css("img"))


def test_basic_functions(screen):
    IMG_LOC = locators.Css("img")
    A_LOC = locators.Css("a")
    F_LOC = locators.Css("footer")
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.get_by(IMG_LOC), WebElement)
    with pytest.raises(NoSuchElementException):
        screen.get_by(F_LOC)
    with pytest.raises(MultipleSuchElementsException):
        screen.get_by(A_LOC)

    # test_query(selenium):

    assert isinstance(screen.query_by(IMG_LOC), WebElement)
    assert screen.query_by(F_LOC) is None
    with pytest.raises(MultipleSuchElementsException):
        screen.query_by(A_LOC)

    # test_find(selenium):

    assert isinstance(screen.find_by(IMG_LOC), WebElement)
    with pytest.raises(NoSuchElementException):
        screen.find_by(F_LOC) is None
    with pytest.raises(MultipleSuchElementsException):
        screen.find_by(A_LOC)

    # test_get_all_by(selenium):

    assert isinstance(screen.get_all_by(IMG_LOC)[0], WebElement)
    with pytest.raises(NoSuchElementException):
        screen.get_all_by(F_LOC)
    assert len(screen.get_all_by(A_LOC)) > 1

    # test_query_all(selenium):

    assert isinstance(screen.query_all_by(IMG_LOC)[0], WebElement)
    assert len(screen.query_all_by(F_LOC)) == 0
    assert len(screen.query_all_by(A_LOC)) > 1

    # test_find_all(selenium):

    assert isinstance(screen.find_all_by(IMG_LOC)[0], WebElement)
    with pytest.raises(NoSuchElementException):
        screen.find_all_by(F_LOC)
    assert len(screen.find_all_by(A_LOC)) > 1
