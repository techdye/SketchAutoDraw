import json
from pathlib import Path
from time import sleep

import pyautogui
import pytest

import backend.draw


# Stop moving your mouse when the program is launched.

@pytest.fixture
def colors_near():
    SETTINGS_FILE = Path(__file__).parents[1] / "data" / "settings.json"

    with open(SETTINGS_FILE, "r") as f:
        return [tuple(i) for i in json.load(f)["pixels"]]


def test__mouse_click_position():
    screen_width, screen_height = pyautogui.size()

    sleep(0.5)

    backend.draw._mouse_click_position((screen_width // 2, screen_height // 2))
    assert pyautogui.position() == (screen_width // 2, screen_height // 2)

    backend.draw._mouse_click_position((screen_width // 2.01, screen_height // 2.01),
                                       (screen_width // 2, screen_height // 2))
    assert pyautogui.position() == (screen_width // 2, screen_height // 2)


def test__range_by_colors(colors_near):
    colors = backend.draw._range_by_colors(
        values=[(57, 57, 59), (255, 255, 255), (160, 112, 74)],
        colors=colors_near)

    assert colors == [[(57, 57, 59), (), ()], [(), (), ()], [(), (), (160, 112, 74)], [(), (), ()], [(), (), ()],
                      [(), (), ()], [(), (), ()], [(), (), ()], [(), (), ()], [(), (), ()]]


def test__range_by_colors_by_line(colors_near):
    colors = backend.draw._range_by_colors_by_line(
        values=[[(57, 57, 59), (255, 255, 255)], [(255, 255, 255), (160, 112, 74)]],
        colors=colors_near)

    assert colors == [[[(57, 57, 59), ()], [(), ()], [(), ()], [(), ()], [(), ()], [(), ()], [(), ()], [(), ()],
                       [(), ()], [(), ()]], [[(), ()], [(), ()], [(), (160, 112, 74)], [(), ()], [(), ()], [(), ()],
                                             [(), ()], [(), ()], [(), ()], [(), ()]]]
