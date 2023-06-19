from PIL import Image
import requests
from io import BytesIO
from pathlib import Path
import json
import logging

import numpy as np

url: str = "https://static.wikia.nocookie.net/among-us-wiki/images/4/43/Orange.png/revision/latest/thumbnail/width/360/height/360?cb=20211122214800"


def _get_image_online(url: str) -> Image:
    """
    Getting an image online.
    :param url: The url
    :return: The image
    """
    response = requests.get(url)

    logging.debug(f"Getting an image online : {url}")
    return Image.open(BytesIO(response.content))


def _resize(image: Image, pos1: list[int], pos2: list[int]) -> Image:
    """
    Resize an image with positions.
    :param image: The image
    :param pos1: Position 1
    :param pos2: Position 2
    :return: The image
    """
    w = abs(pos1[0] - pos2[0])
    h = abs(pos1[1] - pos2[1])

    logging.debug(f"Resizing an image : {w}, {h}")
    return image.resize((w, h))


def _delete_alpha(image: Image, color: tuple = (256, 256, 256)) -> Image:
    """
    Delete the alpha of the image
    :param image: The image
    :param color: The color behind
    :return: The image without the alpha
    """

    if len(image.split()) >= 4:
        logging.debug(f"Removing image alpha.")

        im = Image.new("RGB", image.size, color)

        im.paste(image, image)
        return im
    return image


def _pixelize(image: Image, divider: int = 5):
    """
    Pixelize the image by using resizing it.
    :param image: The image
    :param divider: The size divider
    :return: The same image that has been pixelized
    """
    w, h = image.size

    return image.resize((w // divider, h // divider))


def _get_every_pixels(image: Image) -> list:
    """
    Get every pixels.
    :param image: The image
    :return: List of every pixels
    """
    pixels_list = []
    logging.debug("Getting pixels list.")

    w, h = image.size

    for ph in range(h):
        pixel_list = [image.getpixel((pw, ph)) for pw in range(w)]

        pixels_list.append(pixel_list)

    return pixels_list


def _get_nearest_pixel(pixel: tuple[int, int, int], pixels_near: list[tuple[int, int, int]]) -> tuple:
    """
    Get the nearest color in a list of pixels.
    :param pixel: The pixel
    :param pixels_near: The list of pixels
    :return: The nearest pixel
    """
    if len(pixel) != 3:
        return 255, 255, 255

    colors = np.array(pixels_near)
    color = np.array(pixel)

    distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))

    nearest_pixel = colors[index_of_smallest]

    for p in nearest_pixel:
        return tuple([i for i in p])


def _get_nearest_pixels(pixels_list: list[list[tuple[int, int, int]]], pixels_near: list[tuple[int, int, int]]) -> list[list[tuple]]:
    """
    Get the nearest pixels using the _get_nearest_pixels function.
    :param pixels_list: Pixel list
    :param pixels_near: The list of the nearest pixels
    :return: The nearest pixels
    """
    pixels_nearest = []

    for pixels in pixels_list:
        pixel_nearest = []

        for pixel in pixels:
            pixel_nearest.append(_get_nearest_pixel(pixel, pixels_near))

        pixels_nearest.append(pixel_nearest)

    return pixels_nearest


if __name__ == "__main__":
    SETTINGS_FILE = Path(__file__).parents[1] / "data" / "settings.json"

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

        pixels_near = [tuple(i) for i in settings["pixels"]]

    image = _get_image_online(url)

    image = _delete_alpha(_pixelize(_resize(image, [-50, 50], [50, -50])))

    image = _get_nearest_pixels(_get_every_pixels(image), pixels_near)

    print(image)

