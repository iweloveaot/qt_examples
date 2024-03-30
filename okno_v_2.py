import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QCommandLinkButton
from PyQt5.QtGui import QTextCursor, QPixmap, QIcon
from PyQt5.QtCore import QSize

con = sqlite3.connect('horror_anima.db')  # Устанавливаем соединение с базой данных
cur = con.cursor()
studios = cur.execute('''SELECT name FROM studio''').fetchall()


class AddError(BaseException):
    pass


class NotNewError(BaseException):  # Создаём классы исключений
    pass


class Start(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('okno0.ui', self)  # Загружаем дизайн главного окна
        self.pushButton.clicked.connect(self.open_seen)
        self.pushButton_2.clicked.connect(self.open_katalog)

    def open_seen(self):  # Нажатием кнопки переходим в папку "Уже смотрел"
        self.seen = Seen()
        self.seen.show()

    def open_katalog(self):  # Нажатием кнопки переходим в каталог
        self.katalog = Katalog()
        self.katalog.show()


class Seen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('okno0_1.ui', self)
        watched = cur.execute('''SELECT title FROM Titles WHERE watched=?''', (1,)).fetchall()
        # Получаем из БД просмотренные произведения
        ghost = QPixmap('ghost.png')
        icon = QIcon(ghost)
        # Загружаем изображение для иконки CommandLinkButton
        for i in range(len(watched)):  # Размещаем кнопки-названия призведений в окне
            self.clb = QCommandLinkButton(watched[i][0], self)
            self.clb.setIcon(icon)
            self.clb.setIconSize(QSize(30, 30))
            self.clb.clicked.connect(self.info_s)
            self.verticalLayout_3.addWidget(self.clb)
            # Добавляем кнопки в layout, чтобы была возможность прокручивать их в ScrollArea
        self.pushButton.clicked.connect(self.closing)

    def closing(self):  # Закрываем окно по нажатию кнопки
        self.close()

    def info_s(self):  # Открытие окна с информацией о произведение
        self.name = self.sender().text()
        self.info = Info_S(self.name)
        self.info.show()


class Info_S(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('okno1_1.ui', self)
        self.name = name
        self.info()  # Вывод информации о произведении
        self.pushButton.clicked.connect(self.delete)

    def info(self):
        self.plainTextEdit.setReadOnly(False)
        key_words = {1: 'Название: ', 2: "Сюжет: ", 3: "Автор оригинала: ", 4: "Анимационная студия: ",
                     5: "Год выхода: ", 6: "Серий: "}
        res = cur.execute('''SELECT title, story, original_author FROM Titles WHERE title = ?''',
                          (self.name,)).fetchall()  # По названию произведения получаем из БД информацию о нём
        num = 1
        for elem in res:  # Выводим название, краткий сюжет и автора идеи
            for i in elem:
                self.plainTextEdit.appendPlainText(key_words[num] + str(i))
                num += 1
        studia = cur.execute('''SELECT name FROM studio WHERE id=(SELECT studio FROM Titles 
                    WHERE title = ?)''', (self.name,)).fetchall()
        self.plainTextEdit.appendPlainText(key_words[num] + studia[0][0])
        # Получаем и выводим название анимационной студии
        end = cur.execute('''SELECT years, series FROM Titles WHERE title = ?''', (self.name,)).fetchall()
        for elem in end:
            for i in elem:
                num += 1
                self.plainTextEdit.appendPlainText(key_words[num] + str(i))
        # Получаем и выводим год выхода и кол-во серий
        rat = cur.execute('''SELECT rating FROM Titles WHERE rating BETWEEN 1 AND 10 AND title = ?''',
                          (self.name,)).fetchall()
        if rat != []:
            self.plainTextEdit.appendPlainText("Ваша оценка: " + str(rat[0][0]))
        else:
            pass
        # При наличие в БД оценки произведения выводим её
        self.plainTextEdit.setReadOnly(True)

    def delete(self):
        cur.execute('''UPDATE Titles SET watched=0 WHERE title=?''', (self.name,))
        # Удаляем из БД информацию о том, что пользователь уже смотрел произведение
        con.commit()
        self.delmess = Mess()
        self.delmess.label.setText('Успешно унижтожено!\n(Только не забудь перезайти в Просмотренное)')
        self.delmess.show()
        self.close()


class Katalog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('okno0_2.ui', self)
        self.animas = cur.execute('''SELECT title FROM Titles ORDER BY title''').fetchall()
        # Получаем все произведения из БД
        num = len(self.animas)
        self.clbs = []
        knife = QPixmap('knife.png')
        icon = QIcon(knife)
        for n in range(num):
            self.btn = QCommandLinkButton(self)
            self.btn.setIcon(icon)
            self.btn.setIconSize(QSize(30, 30))
            self.btn.clicked.connect(self.info_k)
            self.verticalLayout.addWidget(self.btn)
            self.clbs.append(self.btn)
        self.load_data()
        self.pushButton.clicked.connect(self.add_new_anima)
        self.pushButton_2.clicked.connect(self.closing)

    def closing(self):
        self.close()

    def info_k(self):  # Переходим в окно с информацией о выбранном произведении
        self.name = self.sender().text()
        self.info = Info_K(self.name)
        self.info.show()

    def load_data(self):  # Устанавливаем навания кнопок
        ind = 0
        for elem in self.clbs:
            elem.setText(self.animas[ind][0])
            ind += 1

    def add_new_anima(self):  # Переходим в окно для добавления в каталог произведения по нажатию кнопки
        self.additor = Add_anima()
        self.additor.show()


class Info_K(QMainWindow):
    def __init__(self, sendr):
        super().__init__()
        uic.loadUi('okno2_1.ui', self)
        self.name = sendr
        self.inform()
        self.pushButton_2.clicked.connect(self.rate)
        self.pushButton.clicked.connect(self.to_watched)

    def inform(self):  # Выводим информацию о выбранном произведении
        self.plainTextEdit.setReadOnly(False)
        key_words = {1: 'Название: ', 2: "Сюжет: ", 3: "Автор оригинала: ", 4: "Анимационная студия: ",
                     5: "Год выхода: ", 6: "Серий: "}
        res = cur.execute('''SELECT title, story, original_author FROM Titles 
        WHERE title = ?''', (self.name, )).fetchall()
        num = 1
        for elem in res:
            for i in elem:
                self.plainTextEdit.appendPlainText(key_words[num] + str(i))
                num += 1
        studia = cur.execute('''SELECT name FROM studio WHERE id=(SELECT studio FROM Titles 
            WHERE title = ?)''', (self.name, )).fetchall()
        self.plainTextEdit.appendPlainText(key_words[num] + studia[0][0])
        end = cur.execute('''SELECT years, series FROM Titles WHERE title = ?''', (self.name, )).fetchall()
        for elem in end:
            for i in elem:
                num += 1
                self.plainTextEdit.appendPlainText(key_words[num] + str(i))
        rat = cur.execute('''SELECT rating FROM Titles 
        WHERE rating BETWEEN 1 AND 10 AND title = ?''', (self.name, )).fetchall()
        if rat != []:
            self.plainTextEdit.appendPlainText("Ваша оценка: " + str(rat[0][0]))
        else:
            pass
        self.plainTextEdit.setReadOnly(True)

    def rate(self):  # Функция выставления оценки по нажатию соответствующей кнопки
        cur.execute('''UPDATE Titles SET rating = ? WHERE title = ?''', (self.spinBox.text(), self.name,))
        con.commit()
        # Добавляем выставленную оценку в БД
        rat = cur.execute('''SELECT rating FROM Titles WHERE rating BETWEEN 1 AND 10 AND title = ?''',
                          (self.name,)).fetchall()
        # Выбираем произведения с оценкой, отличной от нуля
        flag = False
        curs = self.plainTextEdit.textCursor()
        end = curs.selectionEnd()
        curs.setPosition(end)
        curs.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        # Устанавливаем курсор на последнюю строку поля информации
        if 'Серий' in curs.selectedText() or curs.selectedText() is False:
            curs.clearSelection()
        else:
            curs.removeSelectedText()
            flag = True
        # Выясняем содержит ли последняя строка информацию об оценке или какую-то другую
        if rat != []:
            if not flag:
                self.plainTextEdit.appendPlainText("Ваша оценка: " + str(rat[0][0]))
            # Если последняя строка - не информация об оценке, добавляем её в новый абзац с новой строки
            else:
                curs.insertText("Ваша оценка: " + str(rat[0][0]))
            # Если это информация об оценке, мы заменяем её на актуальную
        else:
            pass

    def to_watched(self):  # Добавление в папку "Уже смотрел" по нажатию соответствующей кнопки
        watched = cur.execute('''SELECT title FROM Titles WHERE watched=?''', (1,)).fetchall()
        if (self.name,) in watched:  # Сообщение в отдельном окне, если произведение уже в папке
            self.to_watched_mess2 = Mess()
            self.to_watched_mess2.label.setText('Ты давно это добавил!')
            self.to_watched_mess2.show()
        else:  # Добавление в БД информации о "уже просмотренном" произведении и вывод соответствующего сообщения
            cur.execute('''UPDATE Titles SET watched=1 WHERE title=?''', (self.name,))
            con.commit()
            self.addmess = Mess()
            self.addmess.label.setText('Добавленно. А ты растёшь с моих глазах.')
            self.addmess.show()


class Add_anima(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('okno2_2.ui', self)
        self.pushButton.clicked.connect(self.add)

    def add(self):
        self.animas = cur.execute('''SELECT title FROM Titles ORDER BY title''').fetchall()
        try:
            if self.lineEdit.text() == '' or self.lineEdit_2.text() == '' or self.lineEdit_3.text() == '' or \
             self.lineEdit_4.text() == '' or self.lineEdit_5.text() == '' or self.plainTextEdit.toPlainText() == '':
                raise AddError
                # Сообщение об ошибке, если какое-то поле для ввода информации о новом произведении не заполненно
            elif (self.lineEdit_5.text(),) in self.animas:
                raise NotNewError
                # Сообщение об ошибке, если введённое название произведения уже есть в БД
        except AddError:
            self.err_mess = Mess()
            self.err_mess.label.setText('Недостаточно информации! Заполни все поля.')
            self.err_mess.show()
        except NotNewError:
            self.not_new_mess = Mess()
            self.not_new_mess.label.setText('А ты не оригинален. Такое название уже есть!')
            self.not_new_mess.show()
        else:
            st = []
            if (self.lineEdit_3.text(),) in studios:
                st = cur.execute('''SELECT id FROM studio WHERE name = ?''', (self.lineEdit_3.text(),)).fetchall()
            # Если введённое название студии есть в БД, получаем его индекс
            else:
                cur.execute('''INSERT INTO studio(name) VALUES(?)''', (self.lineEdit_3.text(),))
                st = cur.execute('''SELECT id FROM studio WHERE name = ?''', (self.lineEdit_3.text(),)).fetchall()
            # Если нет, до добавляем его в БД, после получаем его игдекс
            to_add = (self.lineEdit_5.text(), self.plainTextEdit.toPlainText(), self.lineEdit_2.text(), st[0][0],
                      int(self.lineEdit_4.text()), int(self.lineEdit.text()), 0, 0)
            cur.execute('''INSERT INTO Titles VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', to_add)
            con.commit()
            # Добавляем введённую информацию в БД
            self.add_mess = Mess()
            with open('phrases.txt', encoding='utf8') as file:
                text = file.read()
            self.add_mess.label.setText(text)
            self.add_mess.show()
            # Получаем текст сообщения об успешном добавлении из текстового файла
            self.close()
            # После успешного добавления, сразу закрываем окно добавления


class Mess(QDialog):  # Класс для вывода сообщений в окно QDialog с возможностью его закрыть
    def __init__(self):
        super().__init__()
        uic.loadUi('messages.ui', self)
        self.pushButton.clicked.connect(self.closing)

    def closing(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
