import json
from pathlib import Path
from typing import Tuple, List

from pynput import mouse
import pyautogui


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed:
            print(f'Pressed Left Click at {x} at {y}')
        return False  # Returning False if you need to stop the program when Left clicked.


def _mouse_click_position(*args: Tuple[int, int]):
    for pos in args:
        pyautogui.click(button='left', x=pos[0], y=pos[1])


def _range_by_colors(colors: List[Tuple[int, int, int]], values) -> list[list[tuple[int, int, int]]]:
    colors_list = [[], [], [], [], [], [], [], [], [], []]

    for i in values:
        index = colors.index(i)

        if index != 10:
            colors_list[index].append(i)

        for count, color in enumerate(colors_list):
            if index != count:
                colors_list[count].append(())

    return colors_list


def _range_by_colors_by_line(colors: list[tuple[int, int, int]], values) -> list[list[list[tuple[int, int, int]]]]:
    return [_range_by_colors(colors, i) for i in values]


def _draw_one_line(start_position: tuple[int, int], distance: int, values: list[list[tuple[int, int, int]]],
                   positions_x: list, position_y: int, colors: list):
    position = start_position
    color = 0

    for i in values:
        color += 1
        last_col = []

        for col in i:
            if col == ():
                position = (position[0] + distance, position[1])
                continue

            if col != last_col:
                _mouse_click_position((positions_x[colors.index(col)], position_y))
                last_col = col

            _mouse_click_position(position)


            position = (position[0] + distance, position[1])

        position = start_position


if __name__ == "__main__":
    SETTINGS_FILE = Path(__file__).parents[1] / "data" / "settings.json"

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

        pixels_near: list = [tuple(i) for i in settings["pixels"]]
        positions_x: list = settings["positions_x"]
        print(positions_x)

        position_y: int = settings["position_y"]

    print(positions_x)

    _draw_one_line(
        start_position=(500, 500),
        distance=12,
        values=_range_by_colors(pixels_near, [(57, 57, 59), (57, 57, 59), (255, 123, 60), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59), (57, 57, 59)]),
        positions_x=positions_x,
        position_y=position_y,
        colors=pixels_near)
