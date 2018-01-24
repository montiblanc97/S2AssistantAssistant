import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout, QVBoxLayout

from gui.button import RunButton
from gui.input import Input
from gui.output import Output
from gui.twilight import TwilightInput
from gui.weather import WeatherInput


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_menu()

    def __init_menu(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("S2AssistantAssistant")

        self.layout.addWidget(Input())
        self.layout.addWidget(RunButton())
        self.layout.addWidget(Output(), 1)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = MainMenu()
    w.show()

    sys.exit(app.exec_())


# parameters = {"api_key": "", "city": "Cambridge", "state": "MA", "days": "14", "write_weather": True,
#               "write_unfixed_dict": True, "write_fixed_dict": True, "imperial_units": True, "write_html": True}
# with_weather = commander.create_rep(True, True, True, True, True, True, parameters)

# parameters = {"city": "Cambridge", "state": "MA", "days": "14", "write_weather": True, "write_unfixed_dict": True,
#               "write_fixed_dict": True, "imperial_units": True, "write_html": True, "year_start": "2018",
#               "month_start":"12", "day_start": "30", "year_end": "2020", "month_end": "1", "day_end": "1",
#               "timezone": "eastern"}
# with_weather = commander.create_rep(False, True, True, True, True, True, parameters)


"""
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