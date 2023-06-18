from PIL import Image
import requests
from io import BytesIO
from pathlib import Path
import json
import logging

url: str = "https://static.wikia.nocookie.net/among-us-wiki/images/4/43/Orange.png/revision/latest/thumbnail/width/360/height/360?cb=20211122214800"
SETTINGS_FILE = Path(__file__).parents[1] / "data" / "settings.json"


def _get_image_online(url: str) -> Image:
    """
    Getting an image online.
    :param url: The url.
    :return: Image.
    """
    response = requests.get(url)

    logging.debug(f"Getting an image online : {url}")
    return Image.open(BytesIO(response.content))


def _resize(image: Image, pos1: list[int], pos2: list[int]) -> Image:
    w = abs(pos1[0] - pos2[0])
    h = abs(pos1[1] - pos2[1])

    logging.debug(f"Resizing an image : {w}, {h}")
    return image.resize((w, h))


def _delete_alpha(image: Image, color: tuple = (256, 256, 256)) -> Image:
    if len(image.split()) >= 4:
        logging.debug(f"Removing image alpha.")

        im = Image.new("RGB", image.size, color)

        im.paste(image, image)
        return im
    return image


def _pixelize(image, divider: int = 5):
    w, h = image.size

    return image.resize((w // divider, h // divider))


def _get_every_pixels(image):
    pixels_list = []
    logging.debug("Getting pixels list.")

    w, h = image.size

    for ph in range(h):
        pixel_list = [image.getpixel((pw, ph)) for pw in range(w)]

        print(pixel_list)
        pixels_list.append(pixel_list)

    return pixels_list


if __name__ == "__main__":
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

        pixels_near = [tuple(i) for i in settings["pixels"]]

    print(pixels_near)

    image = _get_image_online(url)

    image = _delete_alpha(_pixelize(_resize(image, [-50, 50], [50, -50])))

    print(_get_every_pixels(image))

    image.show()
