import pathlib

import pytest  # type: ignore
from selenium.webdriver.remote.webelement import WebElement  # type: ignore

from selenium_testing_library import (
    Locator,
    MultipleElementsReturned,
    NoElementsReturned,
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


@pytest.mark.skip("Not working yet")
def test_role(screen: Screen):
    screen.driver.get(get_file_path("form.html"))
    assert isinstance(screen.get_by_role("button"), WebElement)


def test_basic_functions(screen):
    IMG_LOC = Locator("img")
    A_LOC = Locator("a")
    F_LOC = Locator("footer")
    screen.driver.get(get_file_path("index.html"))

    assert isinstance(screen.get(IMG_LOC), WebElement)
    with pytest.raises(NoElementsReturned):
        screen.get(F_LOC)
    with pytest.raises(MultipleElementsReturned):
        screen.get(A_LOC)

    # test_query(selenium):

    assert isinstance(screen.query(IMG_LOC), WebElement)
    assert screen.query(F_LOC) is None
    with pytest.raises(MultipleElementsReturned):
        screen.query(A_LOC)

    # test_find(selenium):

    assert isinstance(screen.find(IMG_LOC), WebElement)
    with pytest.raises(NoElementsReturned):
        screen.find(F_LOC) is None
    with pytest.raises(MultipleElementsReturned):
        screen.find(A_LOC)

    # test_get_all(selenium):

    assert isinstance(screen.get_all(IMG_LOC)[0], WebElement)
    with pytest.raises(NoElementsReturned):
        screen.get_all(F_LOC)
    assert len(screen.get_all(A_LOC)) > 1

    # test_query_all(selenium):

    assert isinstance(screen.query_all(IMG_LOC)[0], WebElement)
    assert len(screen.query_all(F_LOC)) == 0
    assert len(screen.query_all(A_LOC)) > 1

    # test_find_all(selenium):

    assert isinstance(screen.find_all(IMG_LOC)[0], WebElement)
    with pytest.raises(NoElementsReturned):
        screen.find_all(F_LOC)
    assert len(screen.find_all(A_LOC)) > 1
