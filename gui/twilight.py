import sys

from PyQt5.QtWidgets import QWidget, QRadioButton, QHBoxLayout, QVBoxLayout, QStackedWidget, \
    QButtonGroup, QPushButton, QLineEdit, QFileDialog, QCheckBox, QApplication, QComboBox

from gui.helpers import basic_form_creator, MutableString
from gui.weather import WeatherInput


class TwilightInput(QWidget):
    """
    Twilight parameter input for GUI. Contains twilight data types in a ComboBox and corresponding selector
    on whether to scrape, import, or ignore as well as necessary parameter input for scraping (unused if not).
    """
    def __init__(self):
        super().__init__()

        self.__init_twilight()
        self.__init_design()

    def __init_twilight(self):
        self.layout = QVBoxLayout()

        self.__types_options()
        self.__scrape()

        self.layout.addWidget(self.combo_box, 0)
        self.layout.addWidget(self.types_options, 0)
        self.layout.addWidget(self.scrape, 0)

        self.setLayout(self.layout)

    def __types_options(self):
        self.types = ["Sun", "Moon", "Nautical", "Civil", "Astronomical"]
        self.__types_combo_box()  # creates the combo box
        self.__types_revolver()  # creates the rotating window
        self.combo_box.setCurrentIndex(0)  # need to reset because revolver creation ends on last combo box entry
        self.combo_box.currentIndexChanged.connect(lambda index: self.combo_switch_window(index))
        # can only link after everything is initialized

    def __types_combo_box(self):
        self.combo_box = QComboBox()
        for name in self.types:
            self.combo_box.addItem(name)

    def __types_revolver(self):
        self.types_options = QStackedWidget()
        self.button_groups = {}  # dict to store {type name: corresponding button group}
        self.abbreviated_paths = {}  # QLineEdit that shows just the file name because no space
        self.full_import_paths = {}  # MutableString stores full path for retrieval later (not seen on GUI)
        self.checkboxes = {}

        for name in self.types:
            row = self.__types_block(name)
            self.types_options.addWidget(row[0])
            self.button_groups[name] = row[1]
            self.abbreviated_paths[name] = row[2]
            self.full_import_paths[name] = row[3]
            self.checkboxes[name] = row[3]

    def __types_block(self, name):
        """
        Makes block for twilight data selection:
            [radio buttons: {none, scrape, import}]
            [browse button (for import), path (for import), save checkbox]
        Label not included (combo box contains)
        :param name: of type of data
        :return: widget of block, button group of radio buttons, line edit of path, checkbox
        """
        layout = QVBoxLayout()

        top_row_layout = QHBoxLayout()

        button_group = QButtonGroup()  # radio buttons
        button_group.setExclusive(True)

        none_button = QRadioButton("None")
        scrape_button = QRadioButton("Scrape")
        import_button = QRadioButton("Import")
        checkbox = QCheckBox("Save")

        button_group.addButton(none_button, 1)  # need 1-index because 0 means not found
        button_group.addButton(scrape_button, 2)
        button_group.addButton(import_button, 3)
        top_row_layout.addWidget(none_button)
        top_row_layout.addWidget(scrape_button)
        top_row_layout.addWidget(import_button)
        top_row_layout.addWidget(checkbox)
        top_row_layout.addStretch()

        button_group.buttonClicked.connect(lambda current: self.update_combo_label_clicked(current))

        self.combo_box.setCurrentIndex(self.types.index(name))
        if name in {"Sun", "Moon", "Nautical"}:  # default setting for Paul Revere Battalion slides
            scrape_button.setChecked(True)
            scrape_button.click()
        else:
            none_button.setChecked(True)
            none_button.click()

        top_row = QWidget()
        top_row.setLayout(top_row_layout)

        bottom_row_layout = QHBoxLayout()

        button = QPushButton("Browse")  # browse button
        abbrev_path = QLineEdit()  # line for import path
        full_path = MutableString("")
        bottom_row_layout.addWidget(button)
        bottom_row_layout.addWidget(abbrev_path)
        button.clicked.connect(lambda: self.set_path(abbrev_path, full_path))

        bottom_row = QWidget()
        bottom_row.setLayout(bottom_row_layout)

        layout.addWidget(top_row)
        layout.addWidget(bottom_row)

        out = QWidget()
        out.setLayout(layout)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        top_row_layout.setContentsMargins(0, 0, 5, 0)
        bottom_row_layout.setContentsMargins(0, 0, 0, 0)
        bottom_row_layout.setSpacing(5)

        return out, button_group, abbrev_path, full_path, checkbox

    def __scrape(self):
        input_fields = [("Apply Daylight Savings", "checkbox"), ("City", "text"), ("State", "text"),
                        ("Timezone", "text"), ("Date Start", "text"), ("Date End", "text")]
        input_defaults = {"City": "Cambridge", "State": "MA", "Country": "US", "Timezone": "Eastern",
                          "Apply Daylight Savings": True, "Date Start": "2018MAR28", "Date End": "2018JUN28"}
        self.scrape_layout, self.scrape_fields = basic_form_creator(input_fields, input_defaults)
        self.scrape = QWidget()

        self.scrape.setLayout(self.scrape_layout)

    def combo_switch_window(self, index):
        self.types_options.setCurrentIndex(index)

    def update_combo_label_clicked(self, changed):
        """
        Updates label in combo box to match current state of that label (scrape, import, or none)
        :param changed: the label that will be changed
        :return: nothing, mutates object
        """
        current_text = self.combo_box.currentText()
        split = current_text.split(" ")
        new_text = split[0] + " - " + changed.text()
        self.combo_box.setItemText(self.combo_box.currentIndex(), new_text)

    def set_path(self, abbrev, full):
        """
        Requests a file path from user and updates abbrev and full accordingly
        :param abbrev: QLineEdit to store abbreviated path
        :param full: MutableString to store full path
        :return: nothing, mutates parameters
        """
        path = QFileDialog.getOpenFileName()[0]
        abbrev.setText(path.split("/")[-1])
        full.set_string(path)

    def __init_design(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addStretch(1)
        self.combo_box.setContentsMargins(0, 0, 0, 0)
        self.types_options.setContentsMargins(0, 5, 0, 0)
        self.scrape_layout.setContentsMargins(0, 0, 0, 0)
        self.scrape_layout.setSpacing(5)


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = WeatherInput()
    w.show()

    sys.exit(app.exec_())
