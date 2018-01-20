import sys
from main_menu import MainMenu
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainMenu()

    sys.exit(app.exec_())