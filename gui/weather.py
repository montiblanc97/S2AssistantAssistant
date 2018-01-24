import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QHBoxLayout, QVBoxLayout, QStackedWidget, \
    QButtonGroup, QPushButton, QFileDialog, QPlainTextEdit, QApplication

from gui.helpers import basic_form_creator


class WeatherInput(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_weather()

    def __init_weather(self):
        self.layout = QVBoxLayout()

        self.__scrape()
        self.__import()
        self.__none()
        self.__revolver()
        self.__selector()

        self.layout.addWidget(self.selector)
        self.layout.addWidget(self.revolver)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

    def __scrape(self):
        input_fields = [("City", "text"), ("State", "text"), ("Country", "text"), ("Days", "text"),
                        ("Imperial Units", "checkbox"), ("weatherbit.io Key", "text"),
                        ("Save Weather", "checkbox")]
        input_defaults = {"City": "Cambridge", "State": "MA", "Country": "US", "Days": "14",
                          "Imperial Units": True, "Save Weather": False}
        scrape_layout, self.scrape_fields = basic_form_creator(input_fields, input_defaults)
        scrape_layout.setContentsMargins(0, 0, 11, 0)
        scrape_layout.setSpacing(5)

        self.scrape = QWidget(self)

        self.scrape.setLayout(scrape_layout)

    def __import(self):
        import_layout = QVBoxLayout()

        button = QPushButton("Browse")

        self.import_path = QPlainTextEdit()
        font_height = self.import_path.fontMetrics().height()
        num_rows = 5
        self.import_path.setFixedHeight(int(num_rows * font_height))

        import_layout.addWidget(button, 0, Qt.AlignTop | Qt.AlignLeft)
        import_layout.addWidget(self.import_path, 0, Qt.AlignTop | Qt.AlignLeft)

        button.clicked.connect(lambda: self.import_path.setPlainText(QFileDialog.getOpenFileName()[0]))

        import_layout.setSpacing(10)
        import_layout.addStretch(1)

        self.import_ = QWidget(self)
        self.import_.setLayout(import_layout)

    def __selector(self):
        selector_layout = QHBoxLayout()
        selector_layout.setContentsMargins(0, 0, 0, 11)
        self.selector_button_group = QButtonGroup()
        self.selector_button_group.setExclusive(True)

        self.none_button = QRadioButton("None")
        self.scrape_button = QRadioButton("Scrape")
        self.import_button = QRadioButton("Import")

        self.selector_button_group.addButton(self.none_button, 1)
        self.selector_button_group.addButton(self.scrape_button, 2)  # need 1-index because 0 means not found
        self.selector_button_group.addButton(self.import_button, 3)
        selector_layout.addWidget(self.none_button)
        selector_layout.addWidget(self.scrape_button)
        selector_layout.addWidget(self.import_button)
        selector_layout.addStretch()
        self.scrape_button.setChecked(True)

        self.selector_button_group.buttonClicked.connect(lambda button: self.switch_window(button))

        self.selector = QWidget(self)
        self.selector.setLayout(selector_layout)

    def __none(self):
        self.none_ = QWidget()

    def __revolver(self):
        self.revolver = QStackedWidget()
        self.revolver.addWidget(self.none_)
        self.revolver.addWidget(self.scrape)
        self.revolver.addWidget(self.import_)
        self.revolver.setCurrentIndex(1)

    def switch_window(self, button):
        self.revolver.setCurrentIndex(self.selector_button_group.id(button) - 1)  # make up for 1-index


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = WeatherInput()
    w.show()

    sys.exit(app.exec_())
