from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QMessageBox
from qgis.core import QgsProject, QgsApplication, QgsVectorFileWriterTask, QgsCoordinateTransform, \
    QgsCoordinateReferenceSystem, QgsVectorFileWriter
from .boundsManager import boundsLine
from .utils import addToProjAndOpenFolder, logMsg, closeWindowModule, getActiveLayer


# --------------<editor-fold desc="Основные сигналы сохранения">--------------------------------------------------------
# Сигнал. Обработка клика кнопки "Сохранить".
def saveFile(self):
    logMsg("Обработка события 'Cохранить'", 1)
    filename = self.dlg.filePath.text()  # Получаем из filePath имя файла.
    if len(filename) == 0:  # Если путь и имя явно не указаны - уведомляем пользователя.
        logMsg("Попытка сохранения без имени и пути файла", 1)
        QMessageBox.information(self.dlg,
                                'Внимание',
                                "Вы не указали путь и имя файла", )
    elif not self.dlg.xmin.text() or not self.dlg.ymin.text() or not self.dlg.xmax.text() or not self.dlg.ymax.text():
        QMessageBox.information(self.dlg,
                                'Внимание',
                                "Пределы не заполнены! \nПроверьте заполнение пределов и повторите попытку.", )
    else:
        logMsg("Попытка вызова основной функции сохранения", 1)
        # Добавляем расширение, согласно индексу формата из formatBox (1 = true = TAB, 0 = false= MIF).
        ext = '.tab' if self.dlg.formatBox.currentIndex() else '.mif'
        extReverse = '.mif' if ext == '.tab' else '.tab'
        print(f'ext = {ext}, extReverse = {extReverse}')
        #filename = filename + ext
        if ext not in filename:  # Если расширения нет в названии файла, будем подставлять его
            if extReverse in filename:
                # Если каким-то образом стоит другое расширение - заменим его на текущее из formatBox
                filenameIndex = filename.index(extReverse)
                filename = f"{filename[:filenameIndex]}.{ext}"
            else:  # Ну а если его нет (пользователь случайно стёр и т.п.) подставляем согласно текущему из formatBox
                filename = f"{filename}.{ext}"
        print(f'FILENAME = {filename}')
        selectedLayer = getActiveLayer(self)
        bounds = boundsLine(self, 'dlg')
        print(bounds)
        wkt = (
            'ENGCRS["NonEarth",'
            'EDATUM["Unknown engineering datum"],'
            'CS[Cartesian,2],'
            'AXIS["(E)",east,ORDER[1],LENGTHUNIT["METER",1]],'
            'AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]'
        )
        fileFormat = 'FORMAT=TAB' if self.dlg.formatBox.currentIndex() else 'FORMAT=MIF'
        if self.dlg.ogr2ogrCheck.isChecked():  # Если стоит чек - то выполняется ogr2ogr
            logMsg("Установлен чек. Вызов QProcess(ogr2ogr)", 1)
            ogr2ogrSaveFile(self, selectedLayer, filename, wkt, bounds, fileFormat)
        else:
            logMsg("Чек не установлен. Cохранение с помощью QgsVectorFileWriterTask ", 1)
            opt = QgsVectorFileWriter.SaveVectorOptions()  # Заполняем опции сохранения векторного слоя.
            opt.fileEncoding = 'CP1251'
            opt.layerOptions = [bounds, 'ENCODING=windows-1251']
            opt.driverName = 'MapInfo file'
            print(opt.layerOptions)
            if self.dlg.styleCheck.isChecked():
                opt.symbologyExport = QgsVectorFileWriter.FeatureSymbology
            converter = QgsVectorFileWriter.FieldValueConverter()
            opt.fieldValueConverter = converter
            # Преобразование в NonEarth(qgis ругается, что нет возможности)
            # crsSrc = selectedLayer.crs()
            # crs = QgsCoordinateReferenceSystem()
            # crs.createFromWkt(wkt)
            # trans = QgsCoordinateTransform(crsSrc, crs, QgsProject.instance())
            # opt.ct = trans
            # Формат и расширение файла согласно индексу из formatBox (1 = true = TAB, 0 = false= MIF).
            opt.datasourceOptions = [fileFormat]
            logMsg("Создание задачи и присваивание в неё QgsVectorFileWriterTask с выбранными опциями",
                   1)
            task = QgsVectorFileWriterTask(selectedLayer, filename, opt)  # Создаём фоновую задачу.
            logMsg("Подключение task к сигналам ", 1)
            task.writeComplete.connect(lambda: onComplete(self, filename))  # Подключаем к сигналам.
            task.errorOccurred.connect(onFail)
            logMsg("Попытка добавить task в taskManger", 1)
            QgsApplication.taskManager().addTask(task)
            print(f"АКТИВНЫЕ_ЗАДАЧИ={QgsApplication.taskManager().count()}")
            #addBoundsCSVFile(selectedLayer, bounds)
        self.dlg.filePath.clear()
        closeWindowModule(self, 'dlg')

# Активация по чек-боксу сохранения с помощью ogr2ogr(QProcess)
def ogr2ogrSaveFile(self, layer, filename, wkt, bounds, fileFormat):
    project = QgsProject.instance()
    layer = project.mapLayersByName(layer.name())[0]
    path = layer.dataProvider().dataSourceUri()
    if "|" in path:  # Для случаев с файлами, в конце пути которых указаны параметры(геометрия и т.п.)
        path = path.split('|')[0]
    process = QProcess()
    process.setProcessChannelMode(QProcess.MergedChannels)  # Объединяем stdout и stderr
    process.finished.connect(lambda exitCode, exitStatus: onProcessFinished(self, exitCode, exitStatus, filename,
                                                                            process))
    process.errorOccurred.connect(ogr2ogrOnFail)
    args = ["-f", "MapInfo File",
            #"-a_srs", wkt,
            '-lco', "ENCODING=CP1251",
            "-lco", f"{bounds}",
            #"-dsco", f"{fileFormat}",
            filename,
            path]
    process.start("ogr2ogr", args)
    closeWindowModule(self, 'dlg')
    process.finished.connect(lambda: afterProcessFinished(layer, bounds))
# --------------</editor-fold>------------------------------------------------------------------------------------------


# --------------<editor-fold desc="Сигналы для QProcess">-----------------------------------------------------------
# Сигнал завершения QProcess
def onProcessFinished(self, exitCode, exitStatus, filename, process):
    if exitStatus == QProcess.NormalExit and exitCode == 0:
        addToProjAndOpenFolder(self, filename)
        print("Слой успешно экспортирован")
        logMsg("Сигнал 'Выполнено'. Задача по экспорту успешно выполнена", 1)
    else:
        logMsg(f"Произошла ошибка при экспорте:{process.readAllStandardError().data().decode('utf-8')}",
               1)
        print("Произошла ошибка при экспорте:", process.readAllStandardError().data().decode('utf-8'))

# Сигнал ошибки QProcess(возможно бесполезен, так как в onProcessFinished выводятся ошибки)
def ogr2ogrOnFail():
    logMsg("Сигнал 'Ошибка'. Ошибка записи в файл", 1)

# Метод, вызываемый после завершения процесса
def afterProcessFinished(layer, bounds):
    # Ваш код, который должен выполняться после завершения QProcess
    logMsg("Процесс ogr2ogr завершился!", 1)  # Например, логгируем завершение
    #addBoundsCSVFile(layer, bounds)
# --------------</editor-fold>------------------------------------------------------------------------------------------


# --------------<editor-fold desc="Сигналы для QgsVectorFileWriterTask">------------------------------------------------
# Сигнал ошибки для QgsVectorFileWriterTask.
def onFail():
    logMsg("Сигнал 'Ошибка'. QgsVectorFileWriterTask - ошибка записи в файл", 1)

# Сигнал для завершения QgsVectorFileWriterTask. Параметры передаются через lambda, если без - будет ошибка.
def onComplete(self, filename):
    logMsg("Сигнал 'Выполнено'. QgsVectorFileWriterTask успешно выполнена", 1)
    print(filename)
    addToProjAndOpenFolder(self, filename)
# --------------</editor-fold>------------------------------------------------------------------------------------------
