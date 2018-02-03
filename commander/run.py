import sys

from PyQt5.QtWidgets import QApplication

from gui.main_menu import MainMenu
from commander.gather import gather_all
from commander.process import process_gathered
from backend.complete_rep import create_rep


def initialize():
    app = QApplication(sys.argv)

    w = MainMenu()
    w.run_widget.hooah.clicked.connect(lambda: run(w))
    w.show()

    sys.exit(app.exec_())


def run(main_menu):
    gathered_flag, gathered_data = gather_all(main_menu)
    if gathered_flag is not False:
        processed = process_gathered(gathered_data)
        if processed is not False:
            rep = create_rep(*processed)  # use processed as arguments individually
            flags = infer_flags(processed[:-1], main_menu)  # ignore parameters, the last item
            csv = rep.get_csv(*flags)
            main_menu.output.result_window.setPlainText(csv)


def infer_flags(processed_data, main_menu):
    """
    Infer which pieces of information to display
    :param processed_data: output from process_gathered
    :param main_menu: GUI to retrieve whether or not guidance is requested
    :return: parameters for MultiDayWeather.get_csv, which pieces of data to display
    """
    out = []

    for data_type in processed_data:
        out.append(not(data_type is None or data_type is False))

    out.append(main_menu.output.checkbox.isChecked())

    return out

if __name__ == '__main__':
    initialize()
