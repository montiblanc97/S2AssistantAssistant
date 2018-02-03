import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QLabel


class RunButton(QWidget):
    """
    Button to run the program.
    """
    def __init__(self):
        super().__init__()

        self.__init_button()
        self.__init_design()

    def __init_button(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel(), 1)
        self.hooah = QPushButton("   HOOAH   ")
        self.layout.addWidget(self.hooah)
        self.layout.addWidget(QLabel(), 1)


        self.setLayout(self.layout)

    def __init_design(self):
        self.layout.setContentsMargins(11, 11, 11, 0)
        # margin on top and none on button because output window margin's are jacked up


if __name__ == '__main__':  # testing
    app = QApplication(sys.argv)

    w = RunButton()
    w.show()

    sys.exit(app.exec_())
