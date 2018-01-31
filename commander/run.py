import sys

from PyQt5.QtWidgets import QApplication

from gui.main_menu import MainMenu
from commander.gather import gather_all
from commander.process import process_gathered


def initialize():
    app = QApplication(sys.argv)

    w = MainMenu()
    w.run_widget.button.clicked.connect(lambda: run(w))
    w.show()

    sys.exit(app.exec_())


def run(main_menu):
    gathered_flag, gathered_data = gather_all(main_menu)
    if gathered_flag is not False:
        processed = process_gathered(gathered_data)


if __name__ == '__main__':
    initialize()
