import os
import time
from PyQt5.QtWidgets import QMessageBox
from qgis.core import QgsGeometry, QgsSpatialIndex, QgsVectorLayer
from .utils import logMsg, messageError, geojsonFilePath


# --------------<editor-fold desc="Функции для работы со строками BOUNDS">----------------------------------------------
# Сигнал активации "Подобрать пределы". (На слое > 5000 фич работа около 3 секунд, поэтому для ускорения, уменьшаем выборку)
def autoBounds(self, layer, dictOfBounds, mode):
    if mode == 'click':
        self.dlg.boundsCheck.setChecked(True)
        onClickCheckButtonBox(self)
    start_time = time.time()  # Таймер для измерения времени выполнения функции
    geojsonFile = geojsonFilePath()  # Путь к файлу GeoJSON
    if not os.path.exists(geojsonFile):  # Проверяем, существует ли файл
        logMsg(f"Файл не найден: {geojsonFile}", 0)  # Логируем сообщение о ненахождении файла
        messageError(self)  # Показываем сообщение об ошибке пользователю
        return  # Завершаем выполнение функции, если файл не найден
    # Загружаем слой GeoJSON из файла
    geojsonLayer = QgsVectorLayer(str(geojsonFile), "russia_geojson_wgs84", "ogr")
    # Если фич в слое > 500, то берём только 100 фич. Это для оптимизации обработки по времени.
    featureCount = layer.featureCount()  # Определяем количество фич в текущем слое
    # print(f'featureCount = {featureCount}')  # Для отладки
    if featureCount > 500:  # Решаем, сколько фич использовать на основе их количества
        features_to_process = layer.getFeatures()
        feature_subset = [next(features_to_process) for _ in range(100)]  # Берем только первые 100 фич
        # print(f'feature_subset = {len(feature_subset)}')
    else:
        feature_subset = list(layer.getFeatures())  # Используем все фичи
    # Объединяем геометрии выбранных фич
    layerUnion = QgsGeometry.unaryUnion([f.geometry() for f in feature_subset])
    # layerUnion = QgsGeometry.unaryUnion([f.geometry() for f in layer.getFeatures()])
    boundingBox = layerUnion.boundingBox()  # Получаем границу (bounding box) объединенной геометрии
    # Создаём пространственный индекс для оптимизации поиска пересечений
    geojsonSpatialIndex = QgsSpatialIndex(geojsonLayer.getFeatures())
    # Находим идентификаторы фичей, пересекающихся с границей (bounding box)
    intersectingFeatureIds = geojsonSpatialIndex.intersects(boundingBox)
    areaPerFeature = {}  # Словарь для хранения площадей пересечений с фичами
    for featureId in intersectingFeatureIds:  # Проходим по всем идентификаторам пересекающихся фичей
        feature2 = geojsonLayer.getFeature(featureId)  # Получаем фичу по идентификатору
        # Находим пересечение между объединенной геометрией и фичей
        intersection_geom = layerUnion.intersection(feature2.geometry())
        if not intersection_geom.isEmpty():  # Проверяем, что пересечение не пустое
            # Сохраняем площадь пересечения в словаре, суммируя для одной фичи
            areaPerFeature[feature2['name']] = areaPerFeature.get(feature2['name'], 0) + intersection_geom.area()
    if areaPerFeature:  # Если имеются пересеченные фичи
        maxFeatureName = max(areaPerFeature, key=areaPerFeature.get)  # Находим имя фичи с максимальной площадью
        self.dlg.boundsBox.setCurrentText(maxFeatureName)  # Устанавливаем найденное имя в текстовое поле
        # Установленное имя, по сигналу подставит пределы из .csv файла
        # Если в boundsBox стоит тот же субъект - перезаписываем пределы (для повторного нажатия на авто подстановку)
        if self.dlg.boundsBox.currentText() == maxFeatureName :
            selectInBoundsBox(self, dictOfBounds)
    else:  # Если пересечений нет
        # Информируем пользователя, что пересечений не найдено
        QMessageBox.information(self.dlg, 'Внимание', "Текущий слой не имеет пересечений с субъектами РФ.\n"
                                                      "Воспользуйтесь пользовательской настройкой пределов.", )
        setDefaultBounds(self, 'noBounds')  # Устанавливаем значения по умолчанию для границ
    print(f'Время выполнения: {time.time() - start_time:.2f} секунд(ы).')  # Выводим время выполнения скрипта

# Редактирование строки BOUNDS по нажатию на чекбокс.
def onClickCheckButtonBox(self):
    logMsg("Редактирование строки BOUNDS по нажатию на чекбокс", 1)
    if self.dlg.boundsCheck.isChecked():
        linesEdit(self, 1)
        self.dlg.boundsBox.setDisabled(False)
    else:
        linesEdit(self, 0)
        self.dlg.boundsBox.setDisabled(True)

# Подставляем дефолтные значения.
def setDefaultBounds(self, mode):
    logMsg("Установка DefaultBounds", 1)
    self.dlg.xmin.setText('-10000000')
    self.dlg.ymin.setText('-10000000')
    self.dlg.xmax.setText('10000000')
    self.dlg.ymax.setText('10000000')
    self.dlg.boundsBox.setCurrentIndex(-1)  # Отображение пустой строки выбора субъектов
    if mode == 'click':
        self.dlg.boundsCheck.setChecked(True)
        onClickCheckButtonBox(self)

# Метод возвращает bounds из полей ui.
def boundsLine(self, mode):
    logMsg("Сбор строки BOUNDS", 1)
    if mode == 'dlg':
        xminText = self.dlg.xmin.text().replace(' ', '')
        yminText = self.dlg.ymin.text().replace(' ', '')
        xmaxText = self.dlg.xmax.text().replace(' ', '')
        ymaxText = self.dlg.ymax.text().replace(' ', '')
        xminText = replaceDot(xminText)
        yminText = replaceDot(yminText)
        xmaxText = replaceDot(xmaxText)
        ymaxText = replaceDot(ymaxText)
        bounds = ('BOUNDS=' + xminText + ',' + yminText + ',' + xmaxText + ',' + ymaxText)
        print(f'boundsLine, mode = f{mode}\nbounds = {bounds}')
        return bounds
    elif mode =='cbd':
        xminText = self.cbd.xmin.text().replace(' ', '')
        yminText = self.cbd.ymin.text().replace(' ', '')
        xmaxText = self.cbd.xmax.text().replace(' ', '')
        ymaxText = self.cbd.ymax.text().replace(' ', '')
        xminText = replaceDot(xminText)
        yminText = replaceDot(yminText)
        xmaxText = replaceDot(xmaxText)
        ymaxText = replaceDot(ymaxText)
        bounds = (xminText + ',' + yminText + ',' + xmaxText + ',' + ymaxText)
        print(f'boundsLine, mode = f{mode}\nbounds = {bounds}')
        return bounds

# Урезание лишних нулей и точки.
def replaceDot(text):
    if text.endswith('.'):  # Убираем точку в конце строки
        return text[:-1]
    elif text.endswith('.0'):  # Убираем нули после точки в конце строки
        return text[:-2]
    elif '.' not in text:  # Если нет точки и в начале идут нули
        # Убираем все ведущие нули
        return text.lstrip('0') or '0'  # '0' на случай, если строка была только из нулей
    elif '.' in text:  # Если точка есть и после неё идут только нули, убираем их
        if text.endswith('0'):  # Удаляем нули и точку, если после точки только нули
            return text.rstrip('0').rstrip('.') if text.rstrip('0').endswith('.') else text.rstrip('0')
    return text

# Управление состоянием полей bounds
#   (включение/выключение редактирования, очистка).
def linesEdit(self, index):
    if index == 1:
        logMsg("Управление состоянием полей BOUNDS: поля доступны", 1)
        self.dlg.xmin.setDisabled(False)
        self.dlg.ymin.setDisabled(False)
        self.dlg.xmax.setDisabled(False)
        self.dlg.ymax.setDisabled(False)
    elif index == 0:
        logMsg("Управление состоянием полей BOUNDS: поля недоступны", 1)
        self.dlg.xmin.setDisabled(True)
        self.dlg.ymin.setDisabled(True)
        self.dlg.xmax.setDisabled(True)
        self.dlg.ymax.setDisabled(True)
    else:
        logMsg("Управление состоянием полей BOUNDS: поля очищены", 1)
        self.dlg.xmin.clear()
        self.dlg.ymin.clear()
        self.dlg.xmax.clear()
        self.dlg.ymax.clear()
        self.dlg.boundsBox.setCurrentIndex(-1)  # Прячем название субъекта
        self.dlg.boundsCheck.setChecked(True)
        onClickCheckButtonBox(self)

# После выбора субъекта РФ из списка, подставляем соответствующие пределы из словаря.
def selectInBoundsBox(self, dictOfBounds):
    logMsg("Выбор пределов в диалоговом окне", 1)
    textOfKey = self.dlg.boundsBox.currentText()
    if textOfKey:
        b = dictOfBounds.get(textOfKey)
        self.dlg.xmin.setText(b[0])
        self.dlg.ymin.setText(b[1])
        self.dlg.xmax.setText(b[2])
        self.dlg.ymax.setText(b[3])
# --------------</editor-fold>------------------------------------------------------------------------------------------
