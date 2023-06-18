from PIL import Image
import PIL
import pytest
import requests

import backend.image


@pytest.fixture
def image_online():
    return backend.image._get_image_online("https://assets.stickpng.com/images/5848152fcef1014c0b5e4967.png")


@pytest.fixture
def image():
    return Image.open("photo.jpeg")


def test__get_image_online(image_online):
    assert image_online


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
