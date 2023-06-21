import json
from pathlib import Path
from time import sleep

import backend.image
import backend.draw

pos1 = (650, 300)
pos2 = (950, 850)

SETTINGS_FILE = Path(__file__).parents[0] / "data" / "settings.json"

with open(SETTINGS_FILE, "r") as f:
    settings = json.load(f)

    pixels_near = [tuple(i) for i in settings["pixels"]]
    positions_x: list = settings["positions_x"]
    position_y: int = settings["position_y"]

url: str = "https://www.giantbomb.com/a/uploads/scale_medium/3/34651/3407207-creepycreep.png"
image_pixels = backend.image.get_url_image_pixels(url, pixels_near, pos1, pos2, 12)

sleep(3)

backend.draw.draw(
        start_position=pos1,
        distance=12,
        values=image_pixels,
        positions_x=positions_x,
        position_y=position_y,
        colors=pixels_near
    )


print(image_pixels)
