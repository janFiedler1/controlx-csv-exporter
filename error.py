from error_ui import Ui_Error
from PyQt5 import QtWidgets, QtCore
import sys

class ErrorMessage:
    def __init__(self, message):
        self.error_popup = QtWidgets.QDialog()
        self.error_ui = Ui_Error()
        self.error_ui.setupUi(self.error_popup)
        self.error_ui.error_message.setText(message)
        self.error_popup.setFixedHeight(130)
        self.error_popup.setFixedWidth(300)
        self.error_popup.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.error_popup.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.error_popup.setWindowTitle("Path Select Error")
        self.error_ui.ok_button.clicked.connect(lambda: self.error_popup.close())

    def show(self):
        self.error_popup.show()