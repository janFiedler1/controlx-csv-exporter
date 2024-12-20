from PyQt5 import QtWidgets, QtCore, QtGui
from window import Ui_MainWindow
import datetime
import sys
import csv
import os
from threading import Thread
import time

from exporter import Exporter
from error import ErrorMessage


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
        icon_path = os.getcwd()+'/controlx-logo.png'
        self.MainWindow.setWindowIcon(QtGui.QIcon(icon_path))
        

        self.ui.dateEdit.setDateTime(datetime.datetime.now())
        self.ui.dateEdit_2.setDateTime(datetime.datetime.now())
        self.ui.lineEdit_2.setText(os.path.dirname(os.path.abspath(__file__))+"\\")

        self.ui.pushButton_2.clicked.connect(lambda: self.export_button_clicked())
        self.ui.toolButton.clicked.connect(lambda: self.ui.lineEdit_2.setText(self.init_file_select()))
        self.ui.pushButton_3.clicked.connect(lambda: self.MainWindow.close())
        
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def init_file_select(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setWindowTitle("Select Folder")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            return selected_files[0]+"/"

    def export_thread(self):
        self.ui.pushButton_2.setDisabled(True)
        self.ui.pushButton_2.setText("Exporting...")
        if(self.ui.checkBox.isChecked()):
            start = self.ui.dateEdit.dateTime()
            end = self.ui.dateEdit_2.dateTime()
            n = 0
            while(start.addDays(n).daysTo(end) >= 0):
                #print(f"start: {start.addDays(n).toString("yyyy-MM-dd")+ " 00:00:00"}, end: {start.addDays(n).toString("yyyy-MM-dd")+ " 23:59:59"}")
                self.exporter.export(self.exporter.get_file_name(self.ui.lineEdit_2.text(), "export_"+start.addDays(n).toString("yyMMdd")), self.ui.lineEdit_2.text(), self.exporter.get_data(TABLE, start.addDays(n).toString("yyyy-MM-dd")+ " 00:00:00",start.addDays(n).toString("yyyy-MM-dd")+" 23:59:59"))
                n = n+1
        else:
            self.exporter.export(self.exporter.get_file_name(self.ui.lineEdit_2.text(), "export_"+self.ui.dateEdit.dateTime().toString("yyMMdd")), self.ui.lineEdit_2.text(), self.exporter.get_data(TABLE, self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")+ " 00:00:00",self.ui.dateEdit_2.dateTime().toString("yyyy-MM-dd")+" 23:59:59"))
        self.ui.pushButton_2.setDisabled(False)
        self.ui.pushButton_2.setText("Export")

    def export_button_clicked(self):
        if(os.path.exists(self.ui.lineEdit_2.text())):
            thread = Thread(target=self.export_thread, name="thread1")
            thread.start()
        else:
            ErrorMessage("Export path does not exist").show()
        

if __name__=="__main__":
    Main()
