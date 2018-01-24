import sys

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout, QLabel, QCheckBox, QApplication, \
    QVBoxLayout


class Output(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_output()

    def __init_output(self):
        self.layout = QVBoxLayout()
        self.__init_checkbox()
        self.__init_result()

        self.row_layout = QHBoxLayout()
        title_label = QLabel("Output")
        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setStyleSheet("QLabel {font-weight: 600}")
        self.row_layout.addWidget(title_label)
        self.row_layout.addWidget(self.checkbox_row)
        self.row_layout.addStretch()
        self.row = QWidget()
        self.row.setLayout(self.row_layout)

        self.layout.addWidget(self.row)
        self.layout.addWidget(self.result_window)

        self.__init_spacing()
        self.setLayout(self.layout)

    def __init_checkbox(self):
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.addWidget(QLabel("       Include: "))
        self.checkboxes = {}

        for name in ["Sun", "Moon", "Nautical", "Civil", "Astronomical"]:
            checkbox = QCheckBox(name)
            self.checkboxes[name] = checkbox
            checkbox_layout.addWidget(checkbox)

        self.checkbox_row = QWidget()
        self.checkbox_row.setLayout(checkbox_layout)

    def __init_result(self):
        self.result_window = QPlainTextEdit()

    def __init_spacing(self):
        self.layout.setContentsMargins(11, 0, 11, 11)
        self.layout.setSpacing(0)
        self.row_layout.setContentsMargins(0, 0, 0, 11)


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = Output()
    w.show()

    sys.exit(app.exec_())
