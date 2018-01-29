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
        self.buttons = {}  # browse buttons for each type
        self.button_groups = {}  # dict to store {type name: corresponding button group}
        self.button_reverse_lookup = {}  # reverse lookup any radio button to its label
        self.abbreviated_paths = {}  # QLineEdit that shows just the file name because no space
        self.full_import_paths = {}  # MutableString stores full path for retrieval later (not seen on GUI)

        for name in self.types:
            row = self.__types_block(name)
            self.types_options.addWidget(row[0])
            self.buttons[name] = row[1]
            self.button_groups[name] = row[2]
            for radio in row[2].buttons():
                self.button_reverse_lookup[radio] = name
            self.abbreviated_paths[name] = row[3]
            self.full_import_paths[name] = row[4]

    def __types_block(self, name):
        """
        Makes block for twilight data selection:
            [radio buttons: {none, scrape, import}]
            [browse button (for import), path (for import)]
        Label not included (combo box contains)
        :param name: of type of data
        :return: widget of block, button group of radio buttons, line edit of path
        """
        layout = QVBoxLayout()

        top_row_layout = QHBoxLayout()

        button_group = QButtonGroup()  # radio buttons
        button_group.setExclusive(True)

        none_button = QRadioButton("None")
        scrape_button = QRadioButton("Scrape")
        import_button = QRadioButton("Import")

        button_group.addButton(none_button, 1)  # need 1-index because 0 means not found
        button_group.addButton(scrape_button, 2)
        button_group.addButton(import_button, 3)
        top_row_layout.addWidget(none_button)
        top_row_layout.addWidget(scrape_button)
        top_row_layout.addWidget(import_button)
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
        abbrev_path.textEdited.connect(lambda: self.set_path(abbrev_path, full_path, abbrev_path.text()))

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

        return out, button, button_group, abbrev_path, full_path

    def __scrape(self):
        input_fields = [("Date Start", "text"), ("Date End", "text"),
                        ("City", "text"), ("State", "text"), ("Timezone", "text")]
        input_defaults = {"Date Start": "2018MAR28", "Date End": "2018JUN28", "City": "Cambridge", "State": "MA",
                          "Country": "US", "Timezone": "Eastern"}
        self.scrape_layout, self.scrape_fields = basic_form_creator(input_fields, input_defaults)

        # adding "Imperial Units" and "Save Weather" options as checkboxes in same row.
        daylight_savings = QCheckBox("Apply Daylight Savings")
        daylight_savings.setChecked(True)  # default is checked
        save = QCheckBox("Save")
        self.scrape_fields["Apply Daylight Savings"] = daylight_savings
        self.scrape_fields["Save Twilight"] = save

        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(daylight_savings)
        self.checkbox_layout.addWidget(save)
        self.checkbox_layout.addStretch()

        checkbox = QWidget()
        checkbox.setLayout(self.checkbox_layout)
        self.scrape_layout.insertWidget(0, checkbox)

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

    def set_path(self, abbrev, full, path=None):
        """
        Requests a file path from user and updates abbrev and full accordingly
        :param abbrev: QLineEdit to store abbreviated path
        :param full: MutableString to store full path
        :param path: to change to or prompts user, if path is given does not abbreviate
        :return: nothing, mutates parameters
        """
        if path is None:
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
        self.checkbox_layout.setContentsMargins(0, 0, 0, 0)

        self.default_border = self.scrape_fields["City"].styleSheet()  # just get from any existing line edit
        self.error_border = "border: 1px solid red;"


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = WeatherInput()
    w.show()

    sys.exit(app.exec_())
