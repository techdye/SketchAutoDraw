import pyautogui


def _mouse_click_position(*args: tuple[int, int]):
    for pos in args:
        pyautogui.click(button='left', x=pos[0], y=pos[1])


def _range_by_colors(colors: list[tuple[int, int, int]], values) -> list[list[tuple[int, int, int]]]:
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


def draw(start_position: tuple[int, int], distance: int, values,
         positions_x: list, position_y: int, colors: list):
    position = start_position
    pixels = _range_by_colors_by_line(colors=colors,
                                      values=values)

    for i in pixels:
        _draw_one_line(position, distance, i, positions_x, position_y, colors)

        position = (position[0], position[1] + distance)
