import os
import pandas as pd
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator, QStandardItem
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from .utils import closeWindowModule
from .boundsManager import boundsLine
from .csvHandler import userCsvFilePath, loadDataFromCSV
from .qTableWidgetManager import updateView

# Путь к .ui файлу класса
FORM_CLASS, _ = uic.loadUiType(os.path.join(
  os.path.dirname(__file__), 'customBounds.ui'))

# Класс диалогового окна с сохранением пользовательских пределов.
class CustomBoundsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CustomBoundsDialog, self).__init__(parent)
        self.setupUi(self)

# --------------<editor-fold desc="Настройка и сигналы класса CustomBoundsDialog">--------------------------------------
# Настройка диалогового окна
def openCustomBoundsDialog(self):
    # Ограничение на ввод в строки bounds (один знак минус, числа, одна точка).
    regex = QRegularExpression(r"^-?(\d{1,9}(\.\d{1,9})?)?$")
    validatorForBounds = QRegularExpressionValidator(regex)
    self.cbd.xmin.setValidator(validatorForBounds)  # Ограничение на ввод только чисел в строки bounds.
    self.cbd.ymin.setValidator(validatorForBounds)
    self.cbd.xmax.setValidator(validatorForBounds)
    self.cbd.ymax.setValidator(validatorForBounds)
    # Регулярное выражение для букв, цифр и кириллицы длиной от 1 до 30 символов
    regex_name = QRegularExpression("^[a-zA-Z0-9а-яА-ЯёЁ]{1,30}$")
    validatorForName = QRegularExpressionValidator(regex_name)  # Валидатор ввода для строки с названием пользовательской настройки.
    self.cbd.name.setValidator(validatorForName)
    self.cbd.xmin.setText(self.dlg.xmin.text())
    self.cbd.ymin.setText(self.dlg.ymin.text())
    self.cbd.xmax.setText(self.dlg.xmax.text())
    self.cbd.ymax.setText(self.dlg.ymax.text())
    self.cbd.exec_()

# Сигнал для кнопки 'Сохранить'. Показываем диалоговое окно, с предложением сохранить пользовательские пределы.
def saveUserBounds(self):
    optionName = self.cbd.name.text()  # Получаем имя файла из текстового поля
    if len(optionName) == 0:  # Если не заполнено имя - сообщаем пользователю
        QMessageBox.information(self.dlg, 'Внимание', "Вы не указали название")
        return
    if (not self.cbd.xmin.text() or not self.cbd.ymin.text() or
            not self.cbd.xmax.text() or not self.cbd.ymax.text()):  # Если есть пустые строки - сообщаем пользователю
        QMessageBox.information(self.dlg, 'Внимание', "Пределы не заполнены!")
        return
    bounds = boundsLine(self, 'cbd')  # Получаем границы
    name = self.cbd.name.text()
    csvPath = userCsvFilePath()  # Путь к файлу CSV
    if csvPath.exists():  # Сохранение пользовательской настройки в .csv файл
        df = pd.read_csv(csvPath, encoding='windows-1251')
    else:
        df = pd.DataFrame(columns=['name', 'bounds'])
    newRow = pd.DataFrame({'name': [name], 'bounds': [bounds]})  # Добавляем новую запись
    df = pd.concat([newRow, df], ignore_index=True)
    df.to_csv(csvPath, index=False, encoding='windows-1251')
    # Очищаем текущие данные в модели и обновляем таблицу
    self.model.removeRows(0, self.model.rowCount())  # Очищаем текущие данные
    loadDataFromCSV(self, csvPath)  # Загружаем данные из CSV файла
    updateView(self)  # Обновляем таблицу с кнопками
    closeWindowModule(self, 'cbd')
# --------------</editor-fold>------------------------------------------------------------------------------------------