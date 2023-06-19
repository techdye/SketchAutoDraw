from typing import Tuple

import pyautogui


def _mouse_click_position(*args: Tuple[int, int]):
    for pos in args:
        pyautogui.click(button='left', x=pos[0], y=pos[1])


if __name__ == "__main__":
    _mouse_click_position((50, 50))


