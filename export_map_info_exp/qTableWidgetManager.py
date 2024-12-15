import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QHeaderView, QWidget, QHBoxLayout, QPushButton
from .csvHandler import userCsvFilePath, loadDataFromCSV
from .utils import logMsg


# --------------<editor-fold desc="Сигналы и функции для QTableView(таблицы с пределами">-----------------------------
# Функция инициализации QTableView
def userTableInit(self):
    logMsg("Инициализация таблицы 'userBoundsView'", 1)
    self.model = QStandardItemModel()  # Создаем модель для QTableView
    self.dlg.userBoundsView.setModel(self.model)  # Устанавливаем модель в QTableView
    self.model.setHorizontalHeaderLabels(['Наименование', 'Пределы', 'Взаимодействие'])  # Добавляем заголовки
    header = self.dlg.userBoundsView.horizontalHeader()  # Настройка вида таблицы
    header.setFixedHeight(20)  # Высота заголовков
    self.dlg.userBoundsView.setColumnWidth(0, 150)  # Настройка размеров колонок
    self.dlg.userBoundsView.setColumnWidth(1, 300)
    self.dlg.userBoundsView.setColumnWidth(2, 100)
    header.setSectionResizeMode(0, QHeaderView.Fixed)
    header.setSectionResizeMode(1, QHeaderView.Fixed)  # Первые две колонки - фиксированные
    header.setSectionResizeMode(2, QHeaderView.Stretch)  # Колонка с кнопками растягивается
    csvFilePath = userCsvFilePath()
    loadDataFromCSV(self, csvFilePath)  # Загружаем данные из CSV файла
    updateView(self)  # Заполняем таблицу

# Добавление кнопок в 3 колонку, настройка размеров строк, шрифта кнопок, подключение сигналов.
def updateView(self):
    row_count = self.model.rowCount()
    if row_count > 0:  # Проверка на наличие строк в модели
        logMsg("Создание кнопок 'Подставить' и 'Удалить' в таблице", 1)
        for row in range(row_count):
            self.dlg.userBoundsView.setRowHeight(row, 20)  # Устанавливаем высоту каждой строки
            buttonWidget = QWidget()  # Создаем контейнер для кнопок
            layout = QHBoxLayout(buttonWidget)
            addButton = QPushButton('Подставить')
            removeButton = QPushButton('Удалить')
            addButton.setMinimumSize(50, 10)  # Установите минимальный размер по своему усмотрению
            removeButton.setMinimumSize(50, 10)
            font = addButton.font()  # Установка шрифта для кнопок
            font.setPointSize(8)
            addButton.setFont(font)
            removeButton.setFont(font)
            layout.setSpacing(0)  # Установка отступа между кнопками
            # Подключаем сигналы
            addButton.clicked.connect(lambda checked, r=row: onAddButtonClicked(self, r))
            removeButton.clicked.connect(lambda checked, r=row: onRemoveButtonClicked(self, r))
            layout.addWidget(addButton)
            layout.addWidget(removeButton)
            layout.setContentsMargins(0, 0, 0, 0)
            # Устанавливаем виджет в ячейку(3 столбец)
            self.dlg.userBoundsView.setIndexWidget(self.model.index(row, 2), buttonWidget)
            for column in range(2):  # Первые два столбца
                item = self.model.item(row, column)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Убираем флаг редактирования

# Обработка нажатия на кнопку 'Подставить'
def onAddButtonClicked(self, row):
    if self.model.rowCount() > row >= 0:  # Проверяем, что указанная строка действительна
        # Получаем текст из всех ячеек текущей строки
        text = [self.model.item(row, column).text() for column in range(self.model.columnCount())]
        if len(text) > 1:  # Проверяем, что массив содержит по крайней мере 2 элемента
            setBoundsFromRowText(self, text[1])  # Передаем второй элемент для дальнейшей обработки

# Сигнал кнопки удалить в ячейках QTableView
def onRemoveButtonClicked(self, row):
    self.model.removeRow(row)  # Удаляем строку из модели
    csvPath = userCsvFilePath()  # Обновляем CSV файл
    df = pd.read_csv(csvPath, encoding='windows-1251')
    # Удаляем строку из DataFrame
    df = df.drop(index=row).reset_index(drop=True)
    df.to_csv(csvPath, index=False, encoding='windows-1251')
    updateView(self)  # Обновляем QTableView

# Устанавливаем пределы в соответствующие элементы интерфейса из строки текста
def setBoundsFromRowText(self, boundsText):
    # Разбиваем строку по запятой и убираем лишние пробелы
    numbersAsStrings = [num.strip() for num in boundsText.split(',')]
    if len(numbersAsStrings) == 4:  # Проверяем, что получено ровно 4 значения
        self.dlg.xmin.setText(numbersAsStrings[0])  # Устанавливаем 1 значение
        self.dlg.ymin.setText(numbersAsStrings[1])  # Устанавливаем 2 значение
        self.dlg.xmax.setText(numbersAsStrings[2])  # Устанавливаем 3 значение
        self.dlg.ymax.setText(numbersAsStrings[3])  # Устанавливаем 4 значение
        self.dlg.boundsBox.setCurrentIndex(-1)  # Сбрасываем индекс в comboBox
        print("Значения успешно вставлены:", numbersAsStrings)  # Для отладки
    else:
        print("Некорректное количество пределов, ожидалось 4 значения.")  # Для отладки
# --------------</editor-fold>------------------------------------------------------------------------------------------
