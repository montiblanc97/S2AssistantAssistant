import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from gui.button import RunButton
from gui.input import Input
from gui.output import Output


class MainMenu(QWidget):
    """
    Main window for the GUI. Contains the Input, RunButton, and Output.
    """

    def __init__(self):
        super().__init__()

        self.__init_menu()
        self.__init_design()
        self.__init_connection()

    def __init_menu(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("S2AssistantAssistant")

        self.input = Input()
        self.run_widget = RunButton()
        self.output = Output()

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.run_widget)
        self.layout.addWidget(self.output, 1)

    def __init_connection(self):
        self.input.weather.selector_button_group.buttonClicked.connect(lambda button: self.__guidance_connect(button))
        self.input.weather.selector_button_group.checkedButton().click()

    def __init_design(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def __guidance_connect(self, button):
        self.input.weather.switch_window(button)  # using to simulate a click on weather panel buttons

        # disable guidance if weather is not given (nothing to base off of)
        enable = True if button.text() == "None" else False

        if enable is True:
            self.output.checkbox.setChecked(False)
            self.output.checkbox.setEnabled(False)
        else:
            self.output.checkbox.setEnabled(True)

if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = MainMenu()
    w.show()

    sys.exit(app.exec_())

"""
# Example calls to backend that GUI needs to support
parameters = {"api_key": "", "city": "Cambridge", "state": "MA", "days": "14", "write_weather": True,
              "write_unfixed_dict": True, "write_fixed_dict": True, "imperial_units": True, "write_html": True}
with_weather = commander.create_rep(True, True, True, True, True, True, parameters)

parameters = {"city": "Cambridge", "state": "MA", "days": "14", "write_weather": True, "write_unfixed_dict": True,
              "write_fixed_dict": True, "imperial_units": True, "write_html": True, "year_start": "2018",
              "month_start":"12", "day_start": "30", "year_end": "2020", "month_end": "1", "day_end": "1",
              "timezone": "eastern"}
with_weather = commander.create_rep(False, True, True, True, True, True, parameters)
"""

"""
# Idea behind GUI
Load data:
    (all radio buttons)
    -weather {scrape: city, state, country, api_key, days, imperial_units, save_weather_data} {load: browse} {None}
    -twilight_data 
        -{sun, moon, nautical, civil, astronomical} each with radio buttons {scrape, load, none}, save checkbox
        -{scrape: fix_dst, if weather is not selected: city, state, timezone, year_start, etc. }

Output data:
    - (checkboxes) include: {weather, sun, moon, nautical, civil, astronomical}
    - (textbox) output
"""
