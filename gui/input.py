from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from gui.twilight import TwilightInput
from gui.weather import WeatherInput


class Input(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_input()

    def __init_input(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Load"), 0, 0, 1, 2)

        self.layout.addWidget(WeatherInput(), 1, 0)
        self.layout.addWidget(TwilightInput(), 1, 1)
