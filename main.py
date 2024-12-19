from PyQt5 import QtWidgets
from window import Ui_MainWindow
import datetime
import sys
import csv
import os

from exporter import Exporter
from pathlib import Path

HOST = "localhost"
USER = "root"
PASSWORD = "Apples:12"
DATABASE = "cxdb"
TABLE =  "zonemeasure"

if __name__=="__main__":
    exporter = Exporter()
    exporter.connect_to_mariadb(HOST, USER, PASSWORD, DATABASE)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle("ControlX Export Tool")

    ui.dateEdit.setDateTime(datetime.datetime.now())
    ui.dateEdit_2.setDateTime(datetime.datetime.now())
    ui.lineEdit_2.setText(os.path.dirname(os.path.abspath(__file__))+"\\")

    print(ui.dateEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss"))
    print(ui.dateEdit.dateTime().toString("yyyy-MM-dd")+" 00:00:00")

    ui.pushButton_2.clicked.connect(lambda: exporter.export(exporter.get_file_name(ui.lineEdit_2.text(), ui.dateEdit.dateTime().toString("yyMMdd")), ui.lineEdit_2.text()+"CSV Exports\\", exporter.get_data(TABLE, ui.dateEdit.dateTime().toString("yyyy-MM-dd")+ " 00:00:00",ui.dateEdit_2.dateTime().toString("yyyy-MM-dd")+" 23:59:59")))
    
    MainWindow.show()
    sys.exit(app.exec_())