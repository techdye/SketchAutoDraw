import json
from pathlib import Path

from PIL import Image
import PIL
import pytest
import requests

import backend.image


@pytest.fixture
def image():
    return Image.open("image.jpeg")


@pytest.fixture
def colors():
    return Image.open("colors.png")


@pytest.fixture
def colors_near():
    SETTINGS_FILE = Path(__file__).parents[1] / "data" / "settings.json"

    with open(SETTINGS_FILE, "r") as f:
        return [tuple(i) for i in json.load(f)["pixels"]]


def test__get_image_online():
    assert backend.image._get_image_online("https://assets.stickpng.com/images/5848152fcef1014c0b5e4967.png")


def test__get_image_online_missing_schema():
    with pytest.raises(requests.exceptions.MissingSchema):
        backend.image._get_image_online("adadadadada")


def test__get_image_online_bad_url():
    with pytest.raises(PIL.UnidentifiedImageError):
        assert backend.image._get_image_online("https://assets.stickpng.com/images/itsaveryverycooltest.png")


def test__resize_positive(image):
    image = backend.image._resize(image, [100, 100], [200, 200])

    w, h = image.size

    assert w == 100
    assert h == 100


def test__resize_negative(image):
    image = backend.image._resize(image, [-100, -100], [-200, -200])

    w, h = image.size

    assert w == 100
    assert h == 100


def test__resize_reversed(image):
    image = backend.image._resize(image, [200, 200], [100, 100])

    w, h = image.size

    assert w == 100
    assert h == 100


def test__resize_equality(image):
    with pytest.raises(ValueError):
        backend.image._resize(image, [200, 50], [200, 100])

    with pytest.raises(ValueError):
        backend.image._resize(image, [200, 100], [200, 100])


def test__delete_alpha_gray(image):
    image = image.copy()
    image.putalpha(0)

    image = backend.image._delete_alpha(image, (128, 128, 128))

    r, g, b = image.getpixel((1, 1))

    if r == 128 and g == 128 and b == 128:
        assert True
    else:
        assert False


def test__delete_alpha_white(image):
    image = image.copy()
    image.putalpha(0)

    image = backend.image._delete_alpha(image, (255, 255, 255))

    r, g, b = image.getpixel((1, 1))

    if r == 255 and g == 255 and b == 255:
        assert True
    else:
        assert False


def test__delete_alpha_black(image):
    image = image.copy()
    image.putalpha(0)

    image = backend.image._delete_alpha(image, (0, 0, 0))

    r, g, b = image.getpixel((1, 1))

    if r == 0 and g == 0 and b == 0:
        assert True
    else:
        assert False


def test__pixelize(image):
    before_w, before_h = image.size

    image = backend.image._pixelize(image)

    w, h = image.size

    assert before_w // 5 == w and before_h // 5 == h


def test__pixelize__ten(image):
    before_w, before_h = image.size

    image = backend.image._pixelize(image, 10)

    w, h = image.size

    assert before_w // 10 == w and before_h // 10 == h


def test__get_every_pixels(colors):
    pixelsList = [[(0, 0, 0), (255, 43, 0)], [(135, 87, 50), (255, 98, 22)], [(255, 243, 0), (73, 255, 0)],
                  [(0, 255, 255), (0, 177, 255)], [(98, 73, 237), (230, 67, 255)], [(255, 255, 255), (236, 236, 236)]]

    assert pixelsList == backend.image._get_every_pixels(backend.image._delete_alpha(colors))


def test__get_nearest_pixel_black(colors_near):
    assert backend.image._get_nearest_pixel((0, 0, 0), colors_near) == (57, 57, 59)


def test__get_nearest_pixel_red(colors_near):
    assert backend.image._get_nearest_pixel((255, 0, 0), colors_near) == (255, 92, 87)


def test__get_nearest_pixel_brown(colors_near):
    assert backend.image._get_nearest_pixel((135, 87, 50), colors_near) == (160, 112, 74)


def test__get_nearest_pixel_orange(colors_near):
    assert backend.image._get_nearest_pixel((255, 98, 22), colors_near) == (255, 123, 60)


def test__get_nearest_pixel_yellow(colors_near):
    assert backend.image._get_nearest_pixel((255, 255, 0), colors_near) == (244, 236, 67)


def test__get_nearest_pixel_green(colors_near):
    assert backend.image._get_nearest_pixel((0, 255, 0), colors_near) == (89, 182, 52)


def test__get_nearest_pixel_cyan(colors_near):
    assert backend.image._get_nearest_pixel((0, 255, 255), colors_near) == (41, 211, 210)


def test__get_nearest_pixel_blue(colors_near):
    assert backend.image._get_nearest_pixel((0, 177, 255), colors_near) == (32, 161, 218)


def test__get_nearest_pixel_purple(colors_near):
    assert backend.image._get_nearest_pixel((39, 0, 255), colors_near) == (98, 73, 237)


def test__get_nearest_pixel_pink(colors_near):
    assert backend.image._get_nearest_pixel((230, 67, 255), colors_near) == (238, 126, 254)


def test__get_nearest_pixel_white(colors_near):
    assert backend.image._get_nearest_pixel((210, 210, 210), colors_near) == (255, 255, 255)


def test__get_nearest_pixels(colors_near):
    pixelsList = [[(0, 0, 0), (255, 43, 0)], [(135, 87, 50), (255, 98, 22)], [(255, 243, 0), (73, 255, 0)],
                  [(0, 255, 255), (0, 177, 255)], [(98, 73, 237), (230, 67, 255)], [(255, 255, 255), (236, 236, 236)]]

    newPixelsList = [[(57, 57, 59), (255, 92, 87)], [(160, 112, 74), (255, 123, 60)], [(244, 236, 67), (89, 182, 52)],
                     [(41, 211, 210), (32, 161, 218)], [(98, 73, 237), (238, 126, 254)],
                     [(255, 255, 255), (255, 255, 255)]]

    assert backend.image._get_nearest_pixels(pixelsList, colors_near) == newPixelsList
