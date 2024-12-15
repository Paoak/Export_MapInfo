import inspect
import math
import os
import subprocess
import traceback
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAction
from qgis.core import QgsMessageLog, Qgis, QgsVectorLayer, QgsProject, QgsMapLayerType


# --------------<editor-fold desc="Сигналы и вспомогательные функции">--------------------------------------------------
# Функция добавляет надпись "Экспорт в MapInfo" в контекстное меню векторного слоя в легенде qgis.
def addCustomAction(self):
    """Add a custom action to the existing 'Экспорт' menu for vector layers."""
    action = QAction(u'Экспорт в MapInfo', self.iface.mainWindow())
    action.triggered.connect(self.run)  # Подключаем действие к методу запуска
    self.iface.addCustomActionForLayerType(action, '', QgsMapLayerType.VectorLayer, True)
    self.actions.append(action)

# Логирование сообщений с выводом в окно событий модуля.
def logMsg(text, indexOfAttention):
    frame = inspect.currentframe()  # получаем объект текущего фрейма
    lineno = frame.f_back.f_lineno  # извлекаем номер строки
    caller_name = frame.f_back.f_code.co_name  # получаем название функции
    message = f'log line {lineno} - {caller_name}(): {text.lower()}'  # создаем сообщение с номером строки
    if indexOfAttention:
        QgsMessageLog.logMessage(message,
                                 'Debug export module',
                                 level=Qgis.Info)
    else:
        QgsMessageLog.logMessage(message,
                                 'Debug export module',
                                 level=Qgis.Critical)

# Возвращаем путь к файлу .gpkg с картой
def geojsonFilePath():
    filename = 'export_map_info_exp/russia_geojson_wgs84.gpkg'
    baseDir = Path(__file__).resolve().parent.parent
    filePath = baseDir.joinpath(filename)
    return filePath

# Возврат пределов выбранного слоя
def layerExtent(layer):
    lExtent = layer.extent()  # Получаем extent слоя. Затем округляем координаты и возвращаем.
    xmin = math.floor(lExtent.xMinimum() * 10) / 10
    ymin = math.floor(lExtent.yMinimum() * 10) / 10
    xmax = math.ceil(lExtent.xMaximum() * 10) / 10
    ymax = math.ceil(lExtent.yMaximum() * 10) / 10
    listOfExtent = [xmin, ymin, xmax, ymax]
    return listOfExtent

# Возвращаем активный слой проекта(выбранный).
def getActiveLayer(self):
    layer = self.iface.activeLayer()
    return layer

# Сигнал смены расширения в formatBox для подстановки расширения в путь файла (если он указан)
def formatChange(self):
    path = self.dlg.filePath.text()  # Получение текста из строки
    ext = '.tab' if self.dlg.formatBox.currentIndex() else '.mif'  # Расширение согласно положению formatBox
    replaceableExt = '.mif' if ext == '.tab' else '.tab'  #  Расширение, которое ищем для замены
    if path:
        if replaceableExt in path and ext not in path:  # Ориентируемся по расширению
            layerIndex = path.index(replaceableExt)
            newPath = f"{path[:layerIndex]}{ext}"  # Новая строка: оставляем часть до слоя и добавляем слой с расширением
            self.dlg.filePath.setText(newPath)  # Обновляем QLineEdit
            print('formatChange: if replaceableExt in path and ext not in path')
        elif ext not in path and replaceableExt not in path:  # Если путь без расширения, тогда явно добавляем расширение к пути файла
            newPath = f"{path}{ext}"
            self.dlg.filePath.setText(newPath)
            print('formatChange: elif ext not in path and replaceableExt not in path')

# Сигнал изменения текста filePath для изменения положения formatBox
def formatPathEdit(self):
    text = self.dlg.filePath.text()  # Если в ручную изменить расширение в строке filePath - то изменится formatBox
    if text:
        if '.mif' in text and self.dlg.formatBox.currentIndex():
            self.dlg.formatBox.setCurrentIndex(0)
        elif '.tab' in text and not self.dlg.formatBox.currentIndex():
            self.dlg.formatBox.setCurrentIndex(1)
        elif '.mif' not in text and '.tab' not in text:
            # Если в строке вообще нет расширения, тогда ставим его в зависимости от положения formatBox
            ext = '.tab' if self.dlg.formatBox.currentIndex() else '.mif'
            self.dlg.filePath.setText(text+ext)

# Выбор пути сохранения файла и отображение в строке.
def selectOutputFile(self):
    logMsg("Выбор имени и пути файла", 1)
    layer = self.iface.activeLayer()  # Получаем активный слой
    if layer is not None:  # Проверяем, что слой активен
        file_path = layer.dataProvider().dataSourceUri()  # Получаем путь к директории активного слоя
        directory = os.path.dirname(file_path)
    else:  # Если активный слой не найден, используем текущую директорию
        directory = ""
    # Открываем диалог сохранения файла
    filename, _filter = QFileDialog.getSaveFileName(
        self.dlg,
        "Выберите расположение и имя файла",
        directory  # Используем директорию активного слоя
    )
    ext = 'tab' if self.dlg.formatBox.currentIndex() else 'mif'
    # Проверяем, если пользователь выбрал файл или нажал 'Отмена'
    if filename:  # Если имя файла не пустое
        self.dlg.filePath.setText(f'{filename}.{ext}')

# Сигнал активации чека ogr2ogr. Закрывает чек план-схема и экспорт стиля символов.
def ogr2ogrCheckChange(self):
    if self.dlg.ogr2ogrCheck.isChecked():  # Проверяем, установлен ли чек-бокс
        self.dlg.styleCheck.setChecked(False)
        self.dlg.styleCheck.setEnabled(False)
        #self.dlg.formatBox.setDisabled(True)
        #self.dlg.formatBox.setCurrentIndex(0)
    else:
        self.dlg.styleCheck.setEnabled(True)
        self.dlg.formatBox.setDisabled(False)

# Функция меняет строки в файле MIF.
def convertMif(filename, ext):
    logMsg("Функция перезаписи файла", 1)
    setCrs = 'CoordSys NonEarth Units "m"'
    defaultBounds = 'Bounds (-10000000, -10000000) (10000000, 10000000)'
    filename = filename[:-4] + ext
    # Считываем 4 строку файла .mif, если там указаны bounds, то явно урезаем строку и копируем,
    #   что бы вставить с финальной строкой, а если нет -> подставляем стандартные значения.
    logMsg("Функция перезаписи файла. Открытие файла для чтения", 1)
    with open(filename, 'r') as f:
        lines = f.readlines()
        currLine = lines[3]
        if 'Bounds' in currLine:
            temp = currLine.find('Bounds')
            currLine = currLine[temp:]
            setLine = setCrs + ' ' + currLine
            f.close()
        else:
            setLine = setCrs + ' ' + defaultBounds + '\n'
            f.close()
    logMsg("Функция перезаписи файла. Открытие файла для записи.", 1)
    with open(filename, 'w') as g:
        lines[3] = setLine
        g.writelines(lines)
        g.close()

# Сообщение пользователю об ошибке и выбрасывание её в консоль.
def messageError(self):
    self.error = True
    QMessageBox.information(self.dlg,
                            'Внимание',
                            "Произошла ошибка")
    logMsg(traceback.format_exc(), 0)
    self.dlg.reject()
    self.dlg.close()

# Добавление экспортированного слоя в проект и открытие расположения файла
def addToProjAndOpenFolder(self, filename):
    # Добавляем экспортированный слой в проект, если активирован чекбокс
    if self.dlg.addToProjectCheck.isChecked():
        logMsg("Добавление экспортированного слоя в проект с приставкой new_", 1)
        newFileName = Path(filename).stem
        layer = QgsVectorLayer(filename,
                               "new_" + newFileName,
                               "ogr")
        QgsProject.instance().addMapLayer(layer)
    # Открываем пользователю расположение файла, если выбран чекбокс
    if self.dlg.openFolderCheck.isChecked():
        logMsg("Отображение пользователю расположения экспортированного файла", 1)
        path = Path(filename)
        directory_path = path.parent
        # Формирование команды в зависимости от операционной системы
        command = f'explorer "{directory_path}"' if os.name == 'nt' else f'xdg-open "{directory_path}"'
        process = subprocess.Popen(command, shell=True)  # Открытие директории с помощью subprocess
        process.communicate()  # Ожидание завершения процесса
        process.terminate()  # Явное завершение подпроцесса

# Закрытие окна модуля после нажатия на 'Сохранить'
def closeWindowModule(self, mode):
    if mode == 'dlg':
        self.first_start = True
        self.dlg.reject()
        self.dlg.close()
    elif mode == 'cbd':
        self.cbd.reject()
        self.cbd.close()
# --------------</editor-fold>------------------------------------------------------------------------------------------
