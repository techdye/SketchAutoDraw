import PIL
import pytest
import requests

import backend.image


@pytest.fixture
def image_online():
    return backend.image._get_image_online("https://assets.stickpng.com/images/5848152fcef1014c0b5e4967.png")


def test__get_image_online(image_online):
    assert image_online


def test__get_image_online_missing_schema():
    with pytest.raises(requests.exceptions.MissingSchema):
        backend.image._get_image_online("adadadadada")


def test__get_image_online_bad_url():
    with pytest.raises(PIL.UnidentifiedImageError):
        assert backend.image._get_image_online("https://assets.stickpng.com/images/itsaveryverycooltest.png")


def test__resize_positive(image_online):
    image = backend.image._resize(image_online, [100, 100], [200, 200])

    w, h = image.size

    assert w == 100
    assert h == 100


def test__resize_negative(image_online):
    image = backend.image._resize(image_online, [-100, -100], [-200, -200])

    w, h = image.size

    assert w == 100
    assert h == 100


def test__resize_reversed(image_online):
    image = backend.image._resize(image_online, [200, 200], [100, 100])

    w, h = image.size

    assert w == 100
    assert h == 100


def test__resize_equality(image_online):
    with pytest.raises(ValueError):
        backend.image._resize(image_online, [200, 50], [200, 100])

    with pytest.raises(ValueError):
        backend.image._resize(image_online, [200, 100], [200, 100])
