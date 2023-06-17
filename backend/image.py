from PIL import Image
import requests
from io import BytesIO

url: str = "https://images.unsplash.com/photo-1575936123452-b67c3203c357?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D&w=1000&q=80"


def _get_image_online(url: str) -> Image:
    """
    Getting an image online.
    :param url: The url.
    :return: Image.
    """
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def _resize(image: Image, pos1: list[int], pos2: list[int]):
    w = abs(pos1[0] - pos2[0])
    h = abs(pos1[1] - pos2[1])

    return image.resize((w, h))


if __name__ == "__main__":
    image = _get_image_online(url)

    image = _resize(image, [500, 100], [200, 800])

    image.show()