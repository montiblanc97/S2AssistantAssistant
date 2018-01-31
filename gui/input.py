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
        # Enable twilight common parameter fields only when weather is None (otherwise can be taken from weather)
        self.weather.selector_button_group.buttonClicked.connect(lambda button: self.__common_param_connect(button))
        self.weather.selector_button_group.checkedButton().click()

        # Two different connections, see comments inside.
        for name in self.twilight.button_groups.keys():
            twilight_group = self.twilight.button_groups[name]

            # Grey out browse button unless Import is selected.
            twilight_group.buttonClicked.connect(lambda button: self.__import_field_connect(button))

            # Disable weather "Country" field unless all twilight options are None (twilight only support US)
            twilight_group.buttonClicked.connect(lambda: self.__country_enabler())

            twilight_group.checkedButton().click()

        self.twilight.button_groups["Sun"].checkedButton().click()
        # need to do to update current text for "Sun" in combo box, guessing because individual radio button
        # is being connected above (due to issues with passing in a function)

    def __common_param_connect(self, button):
        self.weather.switch_window(button)  # using to simulate a click on weather panel buttons

        # disable common parameter fields when unneeded
        enable = True if button.text() == "None" else False  # other cases twilight data can be taken from weather
        city, state, date_start, date_end, timezone = self.twilight.scrape_fields["City"], \
                                                      self.twilight.scrape_fields["State"], \
                                                      self.twilight.scrape_fields["Date Start"], \
                                                      self.twilight.scrape_fields["Date End"], \
                                                      self.twilight.scrape_fields["Timezone"]

        city.setEnabled(enable)
        state.setEnabled(enable)
        date_start.setEnabled(enable)
        date_end.setEnabled(enable)
        timezone.setEnabled(enable)

    def __import_field_connect(self, button):
        # disable import fields when unneeded
        name = self.twilight.button_reverse_lookup[button]

        enable = True if button.text() == "Import" else False
        path = self.twilight.abbreviated_paths[name]
        browse = self.twilight.buttons[name]

        path.setEnabled(enable)
        browse.setEnabled(enable)

    def __country_enabler(self):
        enable = True

        for group in self.twilight.button_groups.values():
            if group.checkedButton().text() != "None":
                enable = False
                self.weather.scrape_fields["Country"].setText("US")  # reset it
                break

        self.weather.scrape_fields["Country"].setEnabled(enable)

