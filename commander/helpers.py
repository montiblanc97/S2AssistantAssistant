from PyQt5.QtWidgets import QMessageBox


def missing_popup(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Missing Parameters")
    msg.setInformativeText(text)
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()

def bad_popup(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Bad Parameters")
    msg.setInformativeText(text)
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()
