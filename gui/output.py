import sys

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout, QLabel, QCheckBox, QApplication, \
    QVBoxLayout


class Output(QWidget):
    """
    Output window for GUI, containing checkboxes to designate which types of data to include and a result window
    to display the output .csv.
    """

    def __init__(self):
        super().__init__()
        self.__init_output()

    def __init_output(self):
        self.layout = QVBoxLayout()
        self.__init_checkbox()
        self.__init_result()

        self.row_layout = QHBoxLayout()
        self.title_label = QLabel("Output")

        self.row_layout.addWidget(self.title_label)
        self.row_layout.addWidget(self.checkbox_row)
        self.row_layout.addStretch()
        self.row = QWidget()
        self.row.setLayout(self.row_layout)

        self.layout.addWidget(self.row)
        self.layout.addWidget(self.result_window)

        self.__init_design()
        self.setLayout(self.layout)

    def __init_checkbox(self):
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(QLabel("       Include: "))  # white-space for design

        self.checkbox = QCheckBox("Guidance")
        self.checkbox.setChecked(True)
        self.checkbox_layout.addWidget(self.checkbox)

        self.checkbox_layout.addWidget(QLabel("Copy to Notepad, save file as .csv, open in Google Sheets"))

        self.checkbox_row = QWidget()
        self.checkbox_row.setLayout(self.checkbox_layout)

    def __init_result(self):
        self.result_window = QPlainTextEdit()

    def __init_design(self):
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setStyleSheet("QLabel {font-weight: 600}")
        self.checkbox_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(11, 11, 11, 11)
        self.layout.setSpacing(0)
        self.row_layout.setContentsMargins(0, 0, 0, 11)


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = Output()
    w.show()

    sys.exit(app.exec_())
