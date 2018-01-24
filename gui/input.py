from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from gui.twilight import TwilightInput
from gui.weather import WeatherInput


class Input(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_input()
        self.__init_spacing()

    def __init_input(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        input_label = QLabel("Input")
        input_label.setStyleSheet("QLabel {font-weight: 600}")
        self.layout.addWidget(input_label, 0, 0)
        weather_label = QLabel("Weather")
        weather_label.setAlignment(Qt.AlignRight)
        self.layout.addWidget(weather_label, 0, 0)

        twilight_label = QLabel("Twilight")
        twilight_label.setAlignment(Qt.AlignRight)
        self.layout.addWidget(twilight_label, 0, 2)

        self.weather = WeatherInput()
        self.twilight = TwilightInput()

        self.layout.addWidget(self.weather, 1, 0, 1, 2)
        self.layout.addWidget(self.twilight, 1, 2, 1, 2)

    def __init_spacing(self):
        self.layout.setContentsMargins(11, 11, 11, 0)
