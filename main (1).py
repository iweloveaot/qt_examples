import sys
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QRadioButton, QMainWindow, QListView, QListWidget, QSpinBox
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QCheckBox, QPlainTextEdit, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

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
        self.start.conf.clicked.connect(self.reg)
        self.start.ext.clicked.connect(self.ext)

    def ext(self):
        sys.exit(app.exec())
    def reg(self):
        login = self.start.login.text()
        password = self.start.password.text()
        if login in users:
            print(users[login], login, password)
            if users[login] == password:
                self.page1.show()




def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Test()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
