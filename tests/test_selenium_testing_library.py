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


def test_by_text(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by_text("Email address"), WebElement)
    assert screen.query_by_text("address") is None
    assert len(screen.find_all_by_text("Item")) == 3

    # Go through get with a text selector
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by(locators.Text("Email address")), WebElement)
    assert screen.query_by(locators.Text("address")) is None
    assert len(screen.find_all_by(locators.Text("Item"))) == 3


def test_by_label_text(screen: Screen):
    screen.driver.get(get_file_path("label.html"))
    username_fields = screen.get_all_by_label_text("Username")
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


def test_by_placeholder_text(screen: Screen):
    funcs = (
        screen.get_by_placeholder_text,
        screen.query_by_placeholder_text,
        screen.find_by_placeholder_text,
    )
    screen.driver.get(get_file_path("index.html"))
    for fun in funcs:
        assert isinstance(fun("My Placeholder"), WebElement)

    list_funcs = (
        screen.get_all_by_placeholder_text,
        screen.query_all_by_placeholder_text,
        screen.find_all_by_placeholder_text,
    )
    for fun in list_funcs:
        items = fun("My Placeholder")
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


@pytest.mark.skip("Not implemented yet")
def test_by_xpath(screen: Screen):
    pass


def test_by_role(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_role,
        screen.query_by_role,
        screen.find_by_role,
    )
    screen.driver.get(get_file_path("index.html"))
    for fun in funcs:
        isinstance(fun("My Role Input"), WebElement)

    list_funcs = (
        screen.get_all_by_role,
        screen.query_all_by_role,
        screen.find_all_by_role,
    )
    for fun in list_funcs:
        items = fun("My Role Input")
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_text_index(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_text,
        screen.query_by_text,
        screen.find_by_text,
    )
    screen.driver.get(get_file_path("index.html"))
    for fun in funcs:
        isinstance(fun("My Text Input"), WebElement)

    list_funcs = (
        screen.get_all_by_text,
        screen.query_all_by_text,
        screen.find_all_by_text,
    )
    for fun in list_funcs:
        items = fun("My Text Input")
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


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
        Within(el).find_all_by(locators.Css("img"), timeout=0.01, poll_frequency=0.005)


def test_parameter_types(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    screen.get_by(locators.Css("img"))
    screen.get_by(("css selector", "img"))
    screen.get_by([locators.By.CSS_SELECTOR, "img"])
    screen.get_by(iter([locators.By.CSS_SELECTOR, "img"]))
    screen.get_by(v for v in [locators.By.CSS_SELECTOR, "img"])


IMG_LOC = locators.Css("img")
A_LOC = locators.Css("a")
F_LOC = locators.Css("footer")


def test_basic_functions(screen: Screen):

    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.get_by(IMG_LOC), WebElement)
    with pytest.raises(NoSuchElementException):
        screen.get_by(F_LOC)
    with pytest.raises(MultipleSuchElementsException):
        screen.get_by(A_LOC)


def test_query(screen: Screen):
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.query_by(IMG_LOC), WebElement)
    assert screen.query_by(F_LOC) is None
    with pytest.raises(MultipleSuchElementsException):
        screen.query_by(A_LOC)


def test_find(screen: Screen):
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.find_by(IMG_LOC), WebElement)
    with pytest.raises(NoSuchElementException):
        screen.find_by(F_LOC, timeout=0.01, poll_frequency=0.005) is None
    with pytest.raises(MultipleSuchElementsException):
        screen.find_by(A_LOC, timeout=0.01, poll_frequency=0.005)


def test_get_all_by(screen: Screen):
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.get_all_by(IMG_LOC)[0], WebElement)
    with pytest.raises(NoSuchElementException):
        screen.get_all_by(F_LOC)
    assert len(screen.get_all_by(A_LOC)) > 1


def test_query_all(screen: Screen):
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.query_all_by(IMG_LOC)[0], WebElement)
    assert len(screen.query_all_by(F_LOC)) == 0
    assert len(screen.query_all_by(A_LOC)) > 1


def test_find_all(screen: Screen):
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.find_all_by(IMG_LOC)[0], WebElement)
    with pytest.raises(NoSuchElementException):
        screen.find_all_by(F_LOC, timeout=0.01, poll_frequency=0.005)
    assert len(screen.find_all_by(A_LOC)) > 1
