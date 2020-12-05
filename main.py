import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QDialog
from PyQt5 import uic
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.eventT()
        self.action.triggered.connect(self.go)

    def go(self):
        exp = MyDialog()
        exp.show()
        exp.exec_()
        self.eventT()

    def eventT(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute('SELECT * FROM list').fetchall()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'название сорта',
                                              'степень обжарки', 'молотый', 'описание вкуса',
                                              'цена', 'объем упаковки'])
        self.table.setRowCount(0)
        for i, row in enumerate(res):
            self.table.setRowCount(
                self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    elem = 'да' if elem else 'нет'
                self.table.setItem(
                    i, j, QTableWidgetItem(str(elem)))


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        self.res = cur.execute('SELECT * FROM list').fetchall()
        self.id = len(self.res) + 1
        self.comboBox.addItems(['Новый'])
        self.comboBox.addItems([str(i + 1) for i in range(len(self.res))])
        self.comboBox.currentTextChanged.connect(self.index)
        self.btn.clicked.connect(self.save)

    def index(self, text):
        if text == 'Новый':
            self.id = len(self.res) + 1
            self.line1.clear()
            self.line2.clear()
            self.line3.clear()
            self.line4.clear()
            self.line5.clear()
            self.line6.clear()
            return
        self.id = int(text)
        self.set_text(self.id)

    def set_text(self, ind):
        self.line1.setText(self.res[ind - 1][1])
        self.line2.setText(self.res[ind - 1][2])
        self.line3.setText(str(self.res[ind - 1][3]))
        self.line4.setText(self.res[ind - 1][4])
        self.line5.setText(str(self.res[ind - 1][5]))
        self.line6.setText(str(self.res[ind - 1][6]))

    def save(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        elem = 1 if self.line3.text() == 'да' else 0
        if self.comboBox.currentText() == 'Новый':
            cur.execute(f"""INSERT INTO list(ID, name, degree, ground, description, price, volume)
                        VALUES ({self.id}, "{self.line1.text()}", "{self.line2.text()}", {elem}, "{self.line4.text()}", 
                        {self.line5.text()}, {self.line6.text()});""")
            con.commit()
            self.hide()
            return
        cur.execute(f"""UPDATE list
                        SET name = "{self.line1.text()}", degree = "{self.line2.text()}", ground = {elem},
                        description = "{self.line4.text()}", price = {self.line5.text()}, volume = {self.line6.text()}""")
        con.commit()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
