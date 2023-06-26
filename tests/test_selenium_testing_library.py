import pathlib

import pytest  # type: ignore
from selenium.webdriver.remote.webelement import WebElement

from selenium_testing_library import (
    MultipleSuchElementsException,
    NoSuchElementException,
    Screen,
    Within,
    __version__,
    locators,
)


def test_version():
    assert __version__ == "2023.5"


@pytest.fixture()
def screen(session_selenium):
    return Screen(session_selenium)


def get_file_path(name):
    return "file://" + str(pathlib.Path(__file__).parent.absolute() / "pages" / name)


def test_by_text(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by_text("Email address"), WebElement)
    assert isinstance(screen.get_by_text("Email add", exact=False), WebElement)
    assert isinstance(screen.get_by_text("Dashboard", exact=False), WebElement)
    assert screen.query_by_text("address") is None
    assert isinstance(screen.query_by_text("address", exact=False), WebElement)
    assert len(screen.find_all_by_text("Item")) == 3
    assert len(screen.find_all_by_text("tem", exact=False)) == 3

    # Go through get with a text selector
    assert isinstance(screen.get_by(locators.Text("Email address")), WebElement)
    assert isinstance(
        screen.get_by(locators.Text("Email add", exact=False)), WebElement
    )
    assert screen.query_by(locators.Text("address")) is None
    assert screen.query_by(locators.Text("addrsdfsdess", exact=False)) is None
    assert len(screen.find_all_by(locators.Text("Ite", exact=False))) == 3


def test_by_text_extra(screen: Screen):
    screen.driver.get(get_file_path("extra.html"))
    assert isinstance(screen.get_by_text("We Are Not Men", selector="div"), WebElement)
    assert isinstance(
        screen.get_by_text("We Are Not Men", selector=".pclass"), WebElement
    )
    assert isinstance(screen.get_by_text("We Are Not Men", ignore="p,span"), WebElement)
    with pytest.raises(NoSuchElementException):
        screen.get_by_text("We Are Not Men", selector="#myid")
    assert screen.query_by_text("We Are Not Men", ignore="p,span,div") is None
    assert len(screen.find_all_by_text("We Are Not Men", ignore="span")) == 2
    assert len(screen.query_all_by_text("We Are Not Men", ignore="p")) == 2
    assert len(screen.get_all_by_text("We Are Not Men", ignore="div")) == 2


def test_by_label_text(screen: Screen):
    screen.driver.get(get_file_path("label.html"))
    username_fields = screen.get_all_by_label_text("Username")
    assert len(username_fields) == 5

    username_fields = screen.get_all_by_label_text("sername", exact=False)
    assert len(username_fields) == 5

    assert screen.query_by_label_text("Label Without Input") is None
    assert screen.query_by_label_text("el Without In", exact=False) is None

    screen.driver.get(get_file_path("form.html"))
    input_field = screen.get_by_label_text("Email address")
    assert isinstance(input_field, WebElement)
    assert input_field.tag_name == "input"
    assert input_field.get_attribute("type") == "email"

    input_field = screen.query_by_label_text("Password")
    assert input_field
    assert input_field.get_attribute("type") == "password"

    input_fields = list(screen.get_all_by_label_text("Same Label"))
    assert input_fields[0].get_attribute("type") == "text"
    assert input_fields[1].get_attribute("type") == "color"


def test_by_label_text_extra(screen: Screen):
    screen.driver.get(get_file_path("extra.html"))

    assert isinstance(
        screen.get_by_label_text("We Are Diva", selector="input"), WebElement
    )
    assert isinstance(
        screen.get_by_label_text("We Are Diva", selector="select"), WebElement
    )


def test_by_alt_text(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    assert isinstance(screen.get_by_alt_text("Some Image"), WebElement)
    assert isinstance(screen.get_by_alt_text("Some", exact=False), WebElement)

    screen.driver.get(get_file_path("form.html"))
    assert len(screen.find_all_by_alt_text("img2 alt")) == 2
    assert len(screen.find_all_by_alt_text("2 alt", exact=False)) == 2
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
        assert isinstance(fun("My Placeholder"), WebElement)  # type: ignore
        assert isinstance(fun("My Place", exact=False), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_placeholder_text,
        screen.query_all_by_placeholder_text,
        screen.find_all_by_placeholder_text,
    )
    for fun in list_funcs:
        items = fun("My Placeholder")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)

        items = fun("My Place", exact=False)  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_role(screen: Screen):
    funcs = (
        screen.get_by_role,
        screen.query_by_role,
        screen.find_by_role,
    )
    screen.driver.get(get_file_path("role.html"))
    for fun in funcs:
        isinstance(fun("dialog"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_role,
        screen.query_all_by_role,
        screen.find_all_by_role,
    )
    for fun in list_funcs:
        items = fun("dialog")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_role_extra(screen: Screen):
    screen.driver.get(get_file_path("extra.html"))
    assert len(screen.get_all_by_role("button", hidden=True)) == 2
    assert len(screen.get_all_by_role("button")) == 1

    assert len(screen.get_all_by_role("tab", selected=True)) == 1
    assert len(screen.get_all_by_role("tab", selected=False)) == 2

    assert len(screen.get_all_by_role("checkbox", checked=True)) == 1
    assert len(screen.get_all_by_role("checkbox", checked=False)) == 2

    assert len(screen.get_all_by_role("link", current=True)) == 1
    assert len(screen.get_all_by_role("link", current=False)) == 2

    screen.driver.get(get_file_path("extra_role.html"))

    assert len(screen.get_all_by_role("button", pressed=True)) == 1
    assert len(screen.get_all_by_role("button", pressed=False)) == 1

    assert len(screen.get_all_by_role("link", expanded=False)) == 1

    assert len(screen.get_all_by_role("switch")) == 1
    assert len(screen.query_all_by_role("checkbox")) == 0
    assert len(screen.query_all_by_role("checkbox", queryFallbacks=True)) == 1

    assert screen.get_by_role("heading", level=3).text == "Heading Level Three"
    assert len(screen.get_all_by_role("heading", level=2)) == 2

    assert screen.get_by_role(
        "alertdialog", description="Your session is about to expire"
    )

    assert screen.get_by_role("input", name="Submit Me")


def test_by_text_index(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_text,
        screen.query_by_text,
        screen.find_by_text,
    )
    screen.driver.get(get_file_path("index.html"))
    for fun in funcs:
        isinstance(fun("My Text Input"), WebElement)  # type: ignore
        isinstance(fun("Text Input", exact=False), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_text,
        screen.query_all_by_text,
        screen.find_all_by_text,
    )
    for fun in list_funcs:
        items = fun("My Text Input")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)

        items = fun("Text Input", exact=False)  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_label_text_index(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_label_text,
        screen.query_by_label_text,
        screen.find_by_label_text,
    )
    for fun in funcs:
        isinstance(fun("My Label Text"), WebElement)  # type: ignore
        isinstance(fun("Label Text", exact=False), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_label_text,
        screen.query_all_by_label_text,
        screen.find_all_by_label_text,
    )
    for fun in list_funcs:
        items = fun("My Label Text")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)

        items = fun("Label Text", exact=False)  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_alt_text_index(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_alt_text,
        screen.query_by_alt_text,
        screen.find_by_alt_text,
    )
    for fun in funcs:
        isinstance(fun("Some Image"), WebElement)  # type: ignore
        isinstance(fun("me Image", exact=False), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_alt_text,
        screen.query_all_by_alt_text,
        screen.find_all_by_alt_text,
    )
    for fun in list_funcs:
        items = fun("Some Image")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)

        items = fun("Some Ima", exact=False)  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_title(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_title,
        screen.query_by_title,
        screen.find_by_title,
    )
    for fun in funcs:
        isinstance(fun("Some Title"), WebElement)  # type: ignore
        isinstance(fun("Some Tit", exact=False), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_title,
        screen.query_all_by_title,
        screen.find_all_by_title,
    )
    for fun in list_funcs:
        items = fun("Some Title")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)

        items = fun("Some T", exact=False)  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_test_id(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_test_id,
        screen.query_by_test_id,
        screen.find_by_test_id,
    )
    for fun in funcs:
        isinstance(fun("Some Test Id"), WebElement)  # type: ignore
        isinstance(fun("Some Test", exact=False), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_test_id,
        screen.query_all_by_test_id,
        screen.find_all_by_test_id,
    )
    for fun in list_funcs:
        items = fun("Some Test Id")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)
        items = fun("Some Test", exact=False)  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_display_value(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_display_value,
        screen.query_by_display_value,
        screen.find_by_display_value,
    )
    for fun in funcs:
        isinstance(fun("Input Display Value"), WebElement)  # type: ignore
        isinstance(fun("Input Display", exact=False), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_display_value,
        screen.query_all_by_display_value,
        screen.find_all_by_display_value,
    )
    for fun in list_funcs:
        items = fun("Input Display Value")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)

        items = fun("Input Display", exact=False)  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)

    els = screen.get_all_by_display_value("All Display Value")
    assert len(els) == 3

    els = screen.get_all_by_display_value("All Display", exact=False)
    assert len(els) == 3


def test_by_css(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_css,
        screen.query_by_css,
        screen.find_by_css,
    )
    for fun in funcs:
        isinstance(fun(".mycss"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_css,
        screen.query_all_by_css,
        screen.find_all_by_css,
    )
    for fun in list_funcs:
        items = fun(".mycss")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_xpath(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_xpath,
        screen.query_by_xpath,
        screen.find_by_xpath,
    )
    for fun in funcs:
        isinstance(fun("//div[@class = 'mycss']"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_xpath,
        screen.query_all_by_xpath,
        screen.find_all_by_xpath,
    )
    for fun in list_funcs:
        items = fun("//div[@class = 'mycss']")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_id(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_id,
        screen.query_by_id,
        screen.find_by_id,
    )
    for fun in funcs:
        isinstance(fun("myid"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_id,
        screen.query_all_by_id,
        screen.find_all_by_id,
    )
    for fun in list_funcs:
        items = fun("myid")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_name(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_name,
        screen.query_by_name,
        screen.find_by_name,
    )
    for fun in funcs:
        isinstance(fun("myname"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_name,
        screen.query_all_by_name,
        screen.find_all_by_name,
    )
    for fun in list_funcs:
        items = fun("myname")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_tag_name(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_tag_name,
        screen.query_by_tag_name,
        screen.find_by_tag_name,
    )
    for fun in funcs:
        isinstance(fun("button"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_tag_name,
        screen.query_all_by_tag_name,
        screen.find_all_by_tag_name,
    )
    for fun in list_funcs:
        items = fun("button")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_link_text(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_link_text,
        screen.query_by_link_text,
        screen.find_by_link_text,
    )
    for fun in funcs:
        isinstance(fun("Link 1"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_link_text,
        screen.query_all_by_link_text,
        screen.find_all_by_link_text,
    )
    for fun in list_funcs:
        items = fun("Link 1")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_partial_link_text(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_partial_link_text,
        screen.query_by_partial_link_text,
        screen.find_by_partial_link_text,
    )
    for fun in funcs:
        isinstance(fun("nk 1"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_partial_link_text,
        screen.query_all_by_partial_link_text,
        screen.find_all_by_partial_link_text,
    )
    for fun in list_funcs:
        items = fun("nk 1")  # type: ignore
        assert isinstance(items, list)
        assert isinstance(items[0], WebElement)


def test_by_class_name(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by_class_name,
        screen.query_by_class_name,
        screen.find_by_class_name,
    )
    for fun in funcs:
        isinstance(fun("mycss"), WebElement)  # type: ignore

    list_funcs = (
        screen.get_all_by_class_name,
        screen.query_all_by_class_name,
        screen.find_all_by_class_name,
    )
    for fun in list_funcs:
        items = fun("mycss")  # type: ignore
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

    Within(el).get_by_text("Hello")
    with pytest.raises(NoSuchElementException):
        Within(el).get_by_text("Password")


def test_parameter_types(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    funcs = (
        screen.get_by,
        screen.get_all_by,
        screen.query_by,
        screen.query_all_by,
        # screen.find_by, # TODO: Figure out why mypy complains
        # screen.find_all_by,
    )
    for fun in funcs:
        fun(locators.Css("img"))
        fun(("css selector", "img"))
        fun([locators.By.CSS_SELECTOR, "img"])
        fun(iter([locators.By.CSS_SELECTOR, "img"]))
        fun(v for v in [locators.By.CSS_SELECTOR, "img"])

    screen.find_by(("css selector", "img"))
    screen.find_all_by(("css selector", "img"))


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


def test_wait_for_stale(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    img = screen.get_by(locators.Css("img"))
    screen.driver.get(get_file_path("index.html"))
    screen.wait_for_stale(img)


def test_no_elements_error(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    with pytest.raises(NoSuchElementException) as excinfo:
        screen.get_by(locators.Css("section"))
    message = str(excinfo.value)
    assert "No element found with locator Css('section', exact=True)" in message


def test_no_elements_error_within(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    parent = screen.get_by_css("main")
    with pytest.raises(NoSuchElementException) as excinfo:
        Within(parent).get_by(locators.Css("section"))
    message = str(excinfo.value)
    assert "No element found with locator Css('section', exact=True)" in message
    assert "</body></html>" not in message
    assert "<main>" in message
    assert "</main>" in message
    assert "</body></html>" not in message


def test_multiple_elements_error(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    with pytest.raises(MultipleSuchElementsException) as excinfo:
        screen.get_by(locators.Css("div"))
    message = str(excinfo.value)
    assert "7 elements found with locator Css('div', exact=True)" in message
    assert "0. <div>             <h1>My Text Input</h1>" in message
    assert (
        '1. <div>                 <a href="https://example.com/">Link 1</a>' in message
    )


def test_quote_escaping(screen: Screen):
    screen.driver.get(get_file_path("bugs.html"))
    screen.get_by_text('Hello "world"')
    screen.get_by_text("Hello 'world'")
    screen.get_by_text("Hello `world`")
    screen.get_by_text("Hello\" `world` '!'")
    screen.get_by_text("\"Hello' `world` '!\"")


def test_log_testing_playground_url(screen: Screen):
    screen.driver.get(get_file_path("index.html"))
    url = screen.log_testing_playground_url()
    assert url is not None
    assert "https://testing-playground.com/#markup=" in url

    url = screen.log_testing_playground_url(screen.get_by_tag_name("main"))
    assert url is not None
    assert "https://testing-playground.com/#markup=" in url

    url = screen.log_testing_playground_url(screen.get_by_id("myid"))
    assert url is None
