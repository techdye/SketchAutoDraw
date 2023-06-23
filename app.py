import json
import logging
from pathlib import Path
from time import sleep

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLineEdit, QLabel
from pynput.mouse import Listener

import backend.image
import backend.draw

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='app.log',
                    level=logging.DEBUG)


def _round_lists(array):
    new_array = []

    for i in array:
        new_array.append(round(i))

    if isinstance(array, list):
        return new_array
    return tuple(new_array)


class Window(QMainWindow):
    def __init__(self, window_name):
        super().__init__()

        self.url = ""
        self.pos1 = ()
        self.pos2 = ()
        self.distance = 0
        self.posx = []
        self.posy = 0

        self.pos_set = 0

        self.listener = Listener()

        self.setWindowTitle(window_name)
        self.setFixedSize(QSize(400, 350))

        self.init_ui()
        self.init_actions()

    def middle(self, pos, width):
        return pos - width // 2

    def init_ui(self):
        self.url_label = QLabel("URL à choisir", self)
        self.url_label.adjustSize()
        self.url_label.move(self.middle(200, self.url_label.size().width()), 20)

        self.url_edit = QLineEdit("", self)
        self.url_edit.setFixedWidth(360)
        self.url_edit.setFixedHeight(30)
        self.url_edit.move(self.middle(200, self.url_edit.size().width()), 50)

        self.pos_label = QLabel("Position de l'image", self)
        self.pos_label.adjustSize()
        self.pos_label.move(145, 95)

        self.pos1_button = QPushButton("Début", self)
        self.pos1_button.setFixedWidth(70)
        self.pos1_button.setFixedHeight(30)
        self.pos1_button.move(self.middle(150, self.pos1_button.size().width()), 120)

        self.pos2_button = QPushButton("Fin", self)
        self.pos2_button.setFixedWidth(70)
        self.pos2_button.setFixedHeight(30)
        self.pos2_button.move(self.middle(250, self.pos2_button.size().width()), 120)

        self.distance_label = QLabel("Distance entre chaque pixel", self)
        self.distance_label.adjustSize()
        self.distance_label.move(115, 155)

        self.distance_edit = QLineEdit("", self)
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 100)
        self.distance_edit.setValidator(onlyInt)
        self.distance_edit.move(self.middle(200, self.distance_edit.size().width()), 180)
        self.distance_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pos_label = QLabel("Mettre la position des dix couleurs de la palette", self)
        self.pos_label.adjustSize()
        self.pos_label.move(50, 220)

        self.color_button = QPushButton("Mettre les positions", self)
        self.color_button.setFixedWidth(150)
        self.color_button.setFixedHeight(30)
        self.color_button.move(self.middle(200, self.color_button.size().width()), 245)

        self.draw_button = QPushButton("Dessiner l'image", self)
        self.draw_button.setFixedWidth(250)
        self.draw_button.setFixedHeight(30)
        self.draw_button.move(self.middle(200, self.draw_button.size().width()), 300)

    def init_actions(self):
        self.pos1_button.clicked.connect(self.position_1)
        self.pos2_button.clicked.connect(self.position_2)

        self.color_button.clicked.connect(self.colors)

        self.draw_button.clicked.connect(self.draw)

    def set_position_one(self, x, y, button, pressed):
        if pressed:
            self.pos1 = x, y
            self.listener.stop()
            self.listener = Listener()
            logging.debug(f"Position one is x: {x}, y: {y}.")

    def set_position_two(self, x, y, button, pressed):
        if pressed:
            self.pos2 = x, y
            self.listener.stop()
            self.listener = Listener()
            logging.debug(f"Position two is x: {x}, y: {y}.")

    def position_1(self):
        logging.debug("Getting position one.")
        self.showMinimized()
        self.listener = Listener(on_click=self.set_position_one)
        self.listener.start()
        self.listener.join()

    def position_2(self):
        logging.debug("Getting position two.")
        self.showMinimized()
        self.listener = Listener(on_click=self.set_position_two)
        self.listener.start()
        self.listener.join()

    def set_colors(self, x, y, button, pressed):
        if pressed:
            logging.debug(f"{len(self.posx)} color (x: {x}, y: {y}) position set.")
            self.posx.append(x)
            self.pos_set += 1

        if len(self.posx) >= 10:
            self.posy = y

            logging.debug(f"Positions for colors are set.")

            self.listener.stop()
            self.listener = Listener()
            self.pos_set = 0

    def colors(self):
        self.posx = []
        logging.debug(f"Getting positions for the colors.")

        self.showMinimized()
        self.listener = Listener(on_click=self.set_colors)
        self.listener.start()
        self.listener.join()

    def draw(self):
        self.url = self.url_edit.text()
        try:
            self.distance = int(self.distance_edit.text())
        except ValueError:
            self.distance = ""
            self.distance_edit.setText(self.distance)

        self.pos1 = _round_lists(self.pos1)
        self.pos2 = _round_lists(self.pos2)
        self.posx = _round_lists(self.posx)

        if not (self.url and self.pos1 and self.pos2 and self.distance and self.posx and self.posy):
            logging.warning("Needs more value.")
            return

        self.showMinimized()

        SETTINGS_FILE = Path(__file__).parents[0] / "data" / "settings.json"

        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)

            pixels_near = [tuple(i) for i in settings["pixels"]]

        image_pixels = backend.image.get_url_image_pixels(self.url, pixels_near, self.pos1, self.pos2, self.distance)

        if not image_pixels:
            return

        sleep(2.5)

        backend.draw.draw(
            start_position=self.pos1,
            distance=self.distance,
            values=image_pixels,
            positions_x=self.posx,
            position_y=self.posy,
            colors=pixels_near
        )


app = QApplication([])

window = Window("SketchHeads AutoDraw")
window.show()

app.exec()
