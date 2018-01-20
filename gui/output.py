import sys
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QGridLayout, QHBoxLayout, QLabel, QCheckBox, QApplication


class Output(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_output()

    def __init_output(self):
        self.layout = QGridLayout()
        self.__init_checkbox()
        self.__init_result()

        self.layout.addWidget(QLabel("Output"), 0, 0, 1, 2)
        self.layout.addWidget(self.checkbox_row, 1, 0)
        self.layout.addWidget(self.result_window, 2, 0)

        self.setLayout(self.layout)

    def __init_checkbox(self):
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(QLabel("Include"))
        self.checkboxes = {}

        for name in ["Sun", "Moon", "Nautical", "Civil", "Astronomical"]:
            checkbox = QCheckBox(name)
            self.checkboxes[name] = checkbox
            checkbox_layout.addWidget(checkbox)

        self.checkbox_row = QWidget()
        self.checkbox_row.setLayout(checkbox_layout)

    def __init_result(self):
        self.result_window = QPlainTextEdit()


# if __name__ == '__main__':  # testing
#     app = QApplication(sys.argv)
#
#     w = Output()
#     w.show()
#
#     sys.exit(app.exec_())