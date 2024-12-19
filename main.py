from PyQt5 import QtWidgets, QtCore
from window import Ui_MainWindow
import datetime
import sys
import csv
import os
from threading import Thread

from exporter import Exporter
from pathlib import Path

HOST = "localhost"
USER = "root"
PASSWORD = "Apples:12"
DATABASE = "cxdb"
TABLE =  "zonemeasure"

class Main:
    def __init__(self):
        self.exporter = Exporter()
        self.exporter.connect_to_mariadb(HOST, USER, PASSWORD, DATABASE)

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.setWindowTitle("ControlX Export Tool")

        self.ui.dateEdit.setDateTime(datetime.datetime.now())
        self.ui.dateEdit_2.setDateTime(datetime.datetime.now())
        self.ui.lineEdit_2.setText(os.path.dirname(os.path.abspath(__file__))+"\\")

        self.ui.pushButton_2.clicked.connect(lambda: self.createThread())
        
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def export_button_clicked(self):
        self.ui.pushButton_3.setDisabled(True)
        self.ui.pushButton_3.setText("Exporting...")
        self.exporter.export(self.ui, self.exporter.get_file_name(self.ui.lineEdit_2.text(), "export_"+self.ui.dateEdit.dateTime().toString("yyMMdd")), self.ui.lineEdit_2.text(), self.exporter.get_data(TABLE, self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")+ " 00:00:00",self.ui.dateEdit_2.dateTime().toString("yyyy-MM-dd")+" 23:59:59"))
        self.ui.pushButton_3.setDisabled(False)
        self.ui.pushButton_3.setText("Export")

    def createThread(self):
        thread = Thread(target=self.export_button_clicked, name="thread1")
        thread.start()

if __name__=="__main__":
    Main()
