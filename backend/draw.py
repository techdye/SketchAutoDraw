import json
from pathlib import Path
from typing import Tuple, List

import pyautogui


def _mouse_click_position(*args: Tuple[int, int]):
    for pos in args:
        pyautogui.click(button='left', x=pos[0], y=pos[1])


def _range_by_colors(colors: List[Tuple[int, int, int]], *args) -> list[list[tuple[int, int, int]]]:
    colors_list = [[], [], [], [], [], [], [], [], [], []]

    for i in args:
        index = colors.index(tuple(i))

        if index != 10:
            colors_list[index].append(tuple(i))

        for count, color in enumerate(colors_list):
            if index != count:
                colors_list[count].append(())

    return colors_list





def draw(pos1: int = (100, 100), pos2: int = (200, 200), distance: int = 5, *colors_list):



if __name__ == "__main__":
    SETTINGS_FILE = Path(__file__).parents[1] / "data" / "settings.json"

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

        pixels_near = [tuple(i) for i in settings["pixels"]]

    _mouse_click_position((50, 50))

    print(list(_range_by_colors(pixels_near, *[[244, 236, 67], [255, 255, 255]])))

