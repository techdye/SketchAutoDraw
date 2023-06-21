import pyautogui

import backend.draw


def test__mouse_click_position():
    screen_width, screen_height = pyautogui.size()

    backend.draw._mouse_click_position((screen_width // 2, screen_height // 2))
    assert pyautogui.position() == (screen_width // 2, screen_height // 2)

    backend.draw._mouse_click_position((screen_width // 2.01, screen_height // 2.01), (screen_width // 2, screen_height // 2))
    assert pyautogui.position() == (screen_width // 2, screen_height // 2)