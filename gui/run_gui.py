import sys

from PyQt5.QtWidgets import QApplication

from gui.main_menu import MainMenu

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainMenu()

    sys.exit(app.exec_())
