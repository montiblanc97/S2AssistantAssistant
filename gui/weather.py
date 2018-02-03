import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QRadioButton, QHBoxLayout, QVBoxLayout, QStackedWidget, \
    QButtonGroup, QPushButton, QFileDialog, QPlainTextEdit, QApplication, QCheckBox, QLabel

from gui.helpers import basic_form_creator


class WeatherInput(QWidget):
    """
    Weather parameter input for GUI. Contains selector on whether to scrape, import, or ignore with corresponding
    windows for each based on current selection e.g. parameter input fields if scraping.
    """

    def __init__(self):
        super().__init__()

        self.__init_weather()
        self.__init_design()

    def __init_weather(self):
        self.layout = QVBoxLayout()

        self.__scrape()
        self.__import()
        self.__none()
        self.__revolver()
        self.__selector()

        self.layout.addWidget(self.selector)
        self.layout.addWidget(self.revolver)

        self.layout.addWidget(QLabel("Powered by the <a href=\"https://www.weatherbit.io/\">Weatherbit API</a>"))

        self.setLayout(self.layout)

    def __scrape(self):
        input_fields = [("City", "text"), ("State", "text"), ("Country", "text"), ("Days", "text"),
                        ("weatherbit.io Key", "text")]
        input_defaults = {"City": "Cambridge", "State": "MA", "Country": "US", "Days": "14"}
        self.scrape_layout, self.scrape_fields = basic_form_creator(input_fields, input_defaults)

        # adding "Imperial Units" and "Save Weather" options as checkboxes in same row.
        imperial = QCheckBox("Imperial Units")
        imperial.setChecked(True)  # default is checked
        save = QCheckBox("Save")
        self.scrape_fields["Imperial Units"] = imperial
        self.scrape_fields["Save Weather"] = save

        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(imperial)
        self.checkbox_layout.addWidget(save)
        self.checkbox_layout.addStretch()

        checkbox = QWidget()
        checkbox.setLayout(self.checkbox_layout)
        self.scrape_layout.addWidget(checkbox)

        self.scrape = QWidget(self)
        self.scrape.setLayout(self.scrape_layout)

    def __import(self):
        self.import_layout = QVBoxLayout()

        button = QPushButton("Browse")

        self.import_path = QPlainTextEdit()
        font_height = self.import_path.fontMetrics().height()
        num_rows = 5  # size of browse window, plenty of space to display full path
        self.import_path.setFixedHeight(int(num_rows * font_height))

        self.import_layout.addWidget(button, 0, Qt.AlignTop | Qt.AlignLeft)  # align top-left corner
        self.import_layout.addWidget(self.import_path, 0, Qt.AlignTop | Qt.AlignLeft)

        button.clicked.connect(lambda: self.import_path.setPlainText(QFileDialog.getOpenFileName()[0]))

        self.import_ = QWidget(self)
        self.import_.setLayout(self.import_layout)

    def __selector(self):
        self.selector_layout = QHBoxLayout()
        self.selector_button_group = QButtonGroup()
        self.selector_button_group.setExclusive(True)

        self.none_button = QRadioButton("None")
        self.scrape_button = QRadioButton("Scrape")
        self.import_button = QRadioButton("Import")

        self.selector_button_group.addButton(self.none_button, 1)
        self.selector_button_group.addButton(self.scrape_button, 2)  # need 1-index because 0 means not found
        self.selector_button_group.addButton(self.import_button, 3)
        self.selector_layout.addWidget(self.none_button)
        self.selector_layout.addWidget(self.scrape_button)
        self.selector_layout.addWidget(self.import_button)
        self.selector_layout.addStretch()
        self.scrape_button.setChecked(True)

        self.selector = QWidget(self)
        self.selector.setLayout(self.selector_layout)

    def __none(self):
        self.none_ = QWidget()

    def __revolver(self):
        self.revolver = QStackedWidget()
        self.revolver.addWidget(self.none_)
        self.revolver.addWidget(self.scrape)
        self.revolver.addWidget(self.import_)
        self.revolver.setCurrentIndex(1)  # default setting is scrape

    def switch_window(self, button):
        """
        Switch input fields based on current selection.
        :param button: radio button of current selection
        :return: nothing, mutates object
        """
        self.revolver.setCurrentIndex(self.selector_button_group.id(button) - 1)  # make up for 1-index

    def __init_design(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.scrape_layout.setContentsMargins(0, 3, 11, 0)  # effort to line up to TwilightInput
        self.scrape_layout.setSpacing(5)
        self.import_layout.setSpacing(10)
        self.import_layout.addStretch(1)
        self.selector_layout.setContentsMargins(0, 0, 0, 11)
        self.checkbox_layout.setContentsMargins(0, 0, 0, 0)
        self.scrape_layout.addStretch(25)  # stretch large enough to move checkboxes close to other fields

        self.default_border = self.scrape_fields["City"].styleSheet()  # just get from any existing line edit
        self.error_border = "border: 1px solid red;"

if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = WeatherInput()
    w.show()

    sys.exit(app.exec_())
