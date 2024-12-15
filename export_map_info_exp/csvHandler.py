import csv
from pathlib import Path
import pandas as pd
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QMessageBox
from .boundsManager import boundsLine
from .utils import logMsg


# --------------<editor-fold desc="Функции для работы с .csv">----------------------------------------------------------
# Функция возвращает sortedBounds.csv файл с пределами
def csvFilePath():
    filename = 'export_map_info_exp/sortedBounds.csv'
    baseDir = Path(__file__).resolve().parent.parent
    filePath = baseDir.joinpath(filename)
    return filePath

# Возвращает userBounds.csv файл с историей ввода пределов
def userCsvFilePath():
    filename = 'export_map_info_exp/userBounds.csv'
    baseDir = Path(__file__).resolve().parent.parent
    filePath = baseDir.joinpath(filename)
    return filePath

# Функция заполняет историю использования пределов из userBounds.csv файла в QTableView
def loadDataFromCSV(self, filename):
    if not filename.exists():  # Если файла нет, создаем его
        with open(filename, mode='w', newline='', encoding='windows-1251') as csvFile:
            logMsg("userBounds.csv отсутствует - создаём новый", 1)
            writer = csv.writer(csvFile)
            writer.writerow(['Name', 'Bounds'])  # Записываем заголовки
    with open(filename, mode='r', newline='', encoding='windows-1251') as csvFile:
        csvreader = csv.reader(csvFile)
        next(csvreader)  # Пропустить заголовок, если он есть
        for row in csvreader:
            if len(row) >= 2:  # Проверка, что в строке достаточно элементов
                self.model.appendRow([QStandardItem(row[0]), QStandardItem(row[1]), QStandardItem("")])  # Пустая ячейка для кнопок

# Преобразование файла sortedBounds.csv, в котором хранятся данные о пределах, в словарь.
def getDictFromCSV():
    logMsg("Распаковка .csv файла в словарь", 1)
    # Получаем путь к файлу .csv
    filePath = csvFilePath()
    result = {}
    # Преобразование в словарь типа - name : [xmin, ymin, xmax, ymax].
    with open(filePath, encoding='windows-1251') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            key = row[1]
            result[key] = row[2:]
        result.pop('Name')
        del reader
    return result  # Возвращаем полученный словарь.

# Заполнение списка "Субъект РФ" пределами из словаря getDictFromCSV()
def fillBoundsBox(self, dictOfBounds):
    logMsg("Наполнение списка субъектов из словаря", 1)
    self.dlg.boundsBox.addItems([i for i in dictOfBounds.keys()])
# --------------</editor-fold>------------------------------------------------------------------------------------------
