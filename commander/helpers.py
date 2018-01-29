from PyQt5.QtWidgets import QMessageBox


def missing_popup(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Missing Parameters")
    msg.setInformativeText(text)
    msg.setWindowTitle("MessageBox demo")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()
