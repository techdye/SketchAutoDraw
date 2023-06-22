from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLineEdit, QLabel


class Window(QMainWindow):
    def __init__(self, window_name):
        super().__init__()

        self.setWindowTitle(window_name)
        self.setFixedSize(QSize(400, 350))

        self.init_ui()

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
        self.draw_button.move(self.middle(200, self.color_button.size().width()), 300)


app = QApplication([])

window = Window("SketchHeads AutoDraw")
window.show()

app.exec()
