import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QLabel


class RunButton(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_button()
        self.__init_spacing()

    def __init_button(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel(), 1)
        self.button = QPushButton("   HOOAH   ")
        self.layout.addWidget(self.button)
        self.layout.addWidget(QLabel(), 1)

        self.setLayout(self.layout)

    def __init_spacing(self):
        self.layout.setContentsMargins(11, 11, 11, 0)
        # good where it is
        pass


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = RunButton()
    w.show()

    sys.exit(app.exec_())
