from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QHBoxLayout, QVBoxLayout, QStackedWidget, \
    QButtonGroup, QPushButton, QLineEdit, QFileDialog, QCheckBox, QGridLayout

from gui.helpers import basic_form_creator


class TwilightInput(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_twilight()

    def __init_twilight(self):
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Twilight"), 0, 0)

        self.__types_options()
        self.__scrape()

        self.layout.addWidget(self.types_options, 1, 0)
        self.layout.addWidget(self.scrape, 1, 1)

        self.setLayout(self.layout)

    def __types_options(self):
        self.types = ["Sun", "Moon", "Nautical", "Civil", "Astronomical"]
        self.types_layout = QVBoxLayout()
        self.button_groups = {}
        self.import_paths = {}
        self.checkboxes = {}

        for name in self.types:
            row = self.__types_row(name)
            self.types_layout.addWidget(row[0])
            self.button_groups[name] = row[1]
            self.import_paths[name] = row[2]
            self.checkboxes[name] = row[3]

        self.types_options = QWidget()
        self.types_options.setLayout(self.types_layout)

    def __types_row(self, name):
        """
        Makes row for twilight data selection:
            [Label for type, radio buttons: {none, scrape, import}, browse button (for import), path (for import),
            save checkbox]
        :param name: of type of data
        :return: widget of row, button group of radio buttons, line edit of path, checkbox
        """
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name))  # label

        button_group = QButtonGroup()  # radio buttons
        button_group.setExclusive(True)

        none_button = QRadioButton("None")
        scrape_button = QRadioButton("Scrape")
        import_button = QRadioButton("Import")

        button_group.addButton(none_button, 1)  # need 1-index because 0 means not found
        button_group.addButton(scrape_button, 2)
        button_group.addButton(import_button, 3)
        layout.addWidget(none_button)
        layout.addWidget(scrape_button)
        layout.addWidget(import_button)
        scrape_button.setChecked(True)

        button = QPushButton("Browse")  # browse button
        import_path = QLineEdit()  # line for path
        layout.addWidget(button)
        layout.addWidget(import_path)
        button.clicked.connect(lambda: import_path.setText(QFileDialog.getOpenFileName()[0]))

        checkbox = QCheckBox("Save")
        layout.addWidget(checkbox)

        out = QWidget()
        out.setLayout(layout)

        return out, button_group, import_path, checkbox

    def __scrape(self):
        input_fields = [("Apply Daylight Savings", "checkbox"), ("City", "text"), ("State", "text"),
                        ("Timezone", "text"), ("Date Start", "text"), ("Date End", "text")]
        input_defaults = {"City": "Cambridge", "State": "MA", "Country": "US", "Timezone": "Eastern",
                          "Apply Daylight Savings": True, "Date Start": "2018MAR28", "Date End": "2018JUN28"}
        scrape_layout, self.scrape_fields = basic_form_creator(input_fields, input_defaults)
        self.scrape = QWidget()

        self.scrape.setLayout(scrape_layout)

# if __name__ == '__main__':  # testing
#     app = QApplication(sys.argv)
#
#     w = WeatherInput()
#     w.show()
#
#     sys.exit(app.exec_())
