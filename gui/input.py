from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from gui.twilight import TwilightInput
from gui.weather import WeatherInput


class Input(QWidget):
    """
    Input window of GUI. Contains the WeatherInput and TwilightInput windows with corresponding labels.
    """

    def __init__(self):
        super().__init__()

        self.__init_input()
        self.__init_design()
        self.__init_connection()

    def __init_input(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.input_label = QLabel("Input")
        self.layout.addWidget(self.input_label, 0, 0)

        self.weather_label = QLabel("Weather")
        # label on window, not WeatherInput object to put labels on same row
        self.layout.addWidget(self.weather_label, 0, 1)

        self.twilight_label = QLabel("Twilight")
        self.layout.addWidget(self.twilight_label, 0, 4)  # 3-apart to allow centering

        self.weather = WeatherInput()
        self.twilight = TwilightInput()

        self.layout.addWidget(self.weather, 1, 0, 1, 3)  # width of 3 cells for centering
        self.layout.addWidget(self.twilight, 1, 3, 1, 3)

    def __init_design(self):
        self.input_label.setStyleSheet("QLabel {font-weight: 600}")  # bold output text
        self.layout.setContentsMargins(11, 11, 11, 0)  # no bottom margin to make button closer
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.twilight_label.setAlignment(Qt.AlignCenter)

    def __init_connection(self):
        self.weather.selector_button_group.buttonClicked.connect(lambda button: self.__connection_helper(button))
        self.weather.selector_button_group.checkedButton().click()

    def __connection_helper(self, button):
        self.weather.switch_window(button)

        enable = True if button.text() != "Scrape" else False
        # print(self.twilight.scrape_fields)
        city, state = self.twilight.scrape_fields["City"], self.twilight.scrape_fields["State"]
        city.setEnabled(enable)
        state.setEnabled(enable)
