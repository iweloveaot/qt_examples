import os
import sys
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QRadioButton, QMainWindow, QListView, QListWidget, QSpinBox, \
    QFileDialog
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QCheckBox, QPlainTextEdit, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import QtWidgets


class Page1(QMainWindow):
    def __init__(self):
        super().__init__()
        Form, Base = uic.loadUiType("page1.ui")
        self.ui = Form()
        self.ui.setupUi(self)


users = {"Usr": '123'}
with open('data.csv') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    for row in reader:
        users[row[1]] = str(row[2])


class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        Form, Base = uic.loadUiType("login.ui")
        self.start = Form()
        self.page1 = Page1()
        self.start.setupUi(self)
        if os.path.isfile('memor.csv'):
            with open('memor.csv') as f:
                reader = csv.reader(f, delimiter=';')
                headers = next(reader)
                self.start.login.setText(headers[0])
                self.start.password.setText(headers[1])
        self.start.conf.clicked.connect(self.reg)
        self.start.ext.clicked.connect(self.ext)
        self.page1.ui.back.clicked.connect(self.back_1)

    def ext(self):
        sys.exit(app.exec())

    def back_1(self):
        self.page1.close()
    def reg(self):
        login = self.start.login.text()
        password = self.start.password.text()
        if login in users:
            if users[login] == password:
                if self.start.memor.isChecked():
                    with open('memor.csv', 'w', newline='') as csvfile:
                        wr = csv.writer(csvfile, delimiter=';',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        wr.writerow([login, password])
                else:
                    if os.path.isfile('memor.csv'):
                        os.remove('memor.csv')
                self.load_function()
                self.page1.show()

    # def save_function(self):
    #     sfile = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    #     if sfile != "":
    #         date = time.strftime("%d-%m-%Y")
    #         filename = '2 № 1 від {}.csv'.format(date)
    #         filepath = os.path.join(sfile, filename)
    #         with open(filepath, "w", newline='') as csvfile:
    #             writer = csv.writer(csvfile, dialect='excel', lineterminator='\n')
    #             columns_N = range(self.ui.table_Level_N.columnCount())
    #             columns_L = range(self.ui.table_Level_L.columnCount())
    #             for row in range(self.ui.table_Level_N.rowCount()):
    #                 writer.writerow(self.ui.table_Level_N.item(row, column).text() for column in columns_N)
    #
    #             for row in range(self.ui.table_Level_L.rowCount()):
    #                 writer.writerow(self.ui.table_Level_L.item(row, column).text() for column in columns_L)

    def load_function(self):
            with open("data.csv", 'r') as file:
                reader = csv.reader(file, delimiter=';')
                headers = next(reader)
                self.page1.ui.table.setHorizontalHeaderLabels(headers)
                for row, values in enumerate(reader):
                    for column, value in enumerate(values):
                        self.page1.ui.table.setItem(
                            row, column, QtWidgets.QTableWidgetItem(value))
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Test()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
