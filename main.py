from chempy import Substance, balance_stoichiometry
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
import sys


# класс, для химических подсчётов
class Task:
    def __init__(self, compound, quest, weight, tyof):
        self.tyof = tyof  # тип задачи
        self.compound = Substance.from_formula(compound[0])  # первый элемент
        self.quest = Substance.from_formula(quest)  # запрашиваемый элемент
        self.fbalance, self.sbalance = balance_stoichiometry(
            {elem for elem in compound}, {quest}
        )  # баланс
        self.felem, self.selem = (
            dict(self.fbalance)[compound[0]],
            dict(self.sbalance)[quest],
        )  # результат балансировки
        self.weight = weight  # данный вес
        self.fmole = round(weight / self.compound.mass, 1)  # моль первого соединения
        self.smole = round(weight / self.compound.mass, 1) / 22.4
        # print(self.compound.molar_mass(), self.smole, self.fmole, self.felem, self.quest.mass, balance_stoichiometry(
        #     {elem for elem in compound}, {quest}
        # ))
        self.proportion = round((self.fmole * self.felem / self.felem) * self.quest.mass)  # пропорция через моли
        self.secproportion = round(
            self.weight * self.quest.mass / int(self.compound.molar_mass()) / self.felem)  # пропорция через объём

    # отправка результата
    def result(self):
        if self.tyof == 'Моль':
            return str(self.proportion)
        elif self.tyof == 'Объём':
            return str(self.secproportion)


# главное окно
class App(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self.set()

    # связывание с UI
    def set(self):
        self.Form = uic.loadUi(r"UI/Form.ui")
        self.Form.button.clicked.connect(self.get_result)
        pct = QPixmap(r"UI/colba.png")
        self.Form.picture.setPixmap(pct)
        self.Form.show()

    # получение и вывод результата
    def get_result(self):
        try:
            grm = float(self.Form.edit_s.text())
            if self.Form.combo.currentText() != "г":
                grm *= 1000
            rez = Task(
                self.Form.edit_f.text().split(" + "), self.Form.edit_t.text(), grm, self.Form.combo_type.currentText()
            )
            self.Form.l_result.setText(f"{rez.result()} граммов")
        except:
            self.err = Error()


# класс ошибки
class Error(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.set()

    # связывание с UI
    def set(self):
        self.Eform = uic.loadUi(r"UI/Eform.ui")
        pct = QPixmap(r"UI/error.png")
        self.Eform.label.setPixmap(pct)
        self.Eform.show()


# движок, для начала работы приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App(app)
    app.exec_()

# моль
# FeBr2 + Br2
# FeBr3
# 90
# 118

# объём
# Fe + O2
# Fe3O2
# 5.1
# 7
