import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QRadioButton, QHBoxLayout, QVBoxLayout, QStackedWidget, \
    QButtonGroup, QPushButton, QFileDialog, QPlainTextEdit, QApplication

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

        self.setLayout(self.layout)

    def __scrape(self):
        input_fields = [("City", "text"), ("State", "text"), ("Country", "text"), ("Days", "text"),
                        ("Imperial Units", "checkbox"), ("weatherbit.io Key", "text"),
                        ("Save Weather", "checkbox")]
        input_defaults = {"City": "Cambridge", "State": "MA", "Country": "US", "Days": "14",
                          "Imperial Units": True, "Save Weather": False}
        self.scrape_layout, self.scrape_fields = basic_form_creator(input_fields, input_defaults)
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


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = WeatherInput()
    w.show()

    sys.exit(app.exec_())
