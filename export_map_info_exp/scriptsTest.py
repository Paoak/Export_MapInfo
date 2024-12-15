#***********************************************************************************************************************
# загрузка слоя фичи по имени:
#**************************************
# from qgis.core import QgsProject, QgsVectorLayer, QgsFeatureRequest, QgsGeometry, QgsMultiPolygon
# from osgeo import ogr
#
# # Путь к вашему GeoPackage
# subjects_gpkg_path = "C:/Users/shelipov.aa/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/export_map_info/russia_geojson_wgs84.gpkg"
#
# # Получаем список слоев из GeoPackage
# driver = ogr.GetDriverByName("GPKG")
# data_source = driver.Open(subjects_gpkg_path, 0)
#
# if not data_source:
#     print("Не удалось открыть GeoPackage.")
# else:
#     print("Список слоев в GeoPackage:")
#     for layer_index in range(data_source.GetLayerCount()):
#         layer = data_source.GetLayerByIndex(layer_index)
#         print(layer.GetName())
#
# # Название слоя и имя атрибута для фильтрации
# layer_name = "russia_geojson_wgs84"  # Используйте правильное имя слоя
# feature_name = "Омская область"  # Замените на значение, по которому вы ищите фичу
#
# # Создаем объект слоя
# layer = QgsVectorLayer(subjects_gpkg_path + f"|layername={layer_name}", layer_name, "ogr")
#
# # Проверка на валидность
# if not layer.isValid():
#     print("Ошибка загрузки слоя.")
# else:
#     print("Слой успешно загружен.")
#
#     # Создаем запрос для поиска фичи по атрибуту 'name'
#     request = QgsFeatureRequest().setFilterExpression(f"name = '{feature_name}'")
#
#     # Ищем фичи по запросу
#     features = layer.getFeatures(request)
#
#     # Если найдены фичи, добавляем их в проект
#     found = False
#     for feature in features:
#         # Создаем новый слой в памяти для найденного мультиполигона
#         new_layer = QgsVectorLayer("MultiPolygon?crs=EPSG:4326", "Найденные мультиполигоны", "memory")
#         new_layer_data = new_layer.dataProvider()
#
#         # Получаем геометрию фичи
#         geom = feature.geometry()
#
#         # Проверяем, является ли геометрия мультиполигона
#         if geom.isMultipart():
#             new_layer_data.addFeatures([feature])
#         else:
#             # Преобразуем в мультиполигон, если необходимо
#             multipolygon = QgsMultiPolygon(geom.asPolygon())  # Преобразуем в мультиполигон
#             new_feature = feature
#             new_feature.setGeometry(multipolygon)  # Установить новую геометрию
#             new_layer_data.addFeatures([new_feature])
#
#         # Добавляем новый слой в проект
#         QgsProject.instance().addMapLayer(new_layer)
#         found = True
#         print(f"Мультиполигон с именем '{feature_name}' успешно загружен.")
#         break  # Останавливаем цикл, если нашли первую подходящую фичу
#
#     if not found:
#         print(f"Мультиполигон с именем '{feature_name}' не найден.")
#***********************************************************************************************************************
# скрипты для поиска вхождений искать смотреть в файлах на рабочем столе
# #*********************************************************************************************************************
## Рабочая замена сабпроцесса на QProcess
# from PyQt5.QtCore import QProcess
#
# def ogr2ogrExport(input_path, name, bounds, format):
#     output_path = f"C:/Users/shelipov.aa/Desktop/py/exportTest/{name}.{format.lower()}"
#     crsWkt = 'ENGCRS["NonEarth",EDATUM["Unknown engineering datum"],CS[Cartesian,2],AXIS["(E)",east,ORDER[1],LENGTHUNIT["METER",1]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]'
#
#     process = QProcess()
#     process.setProcessChannelMode(QProcess.MergedChannels)  # Объединяем stdout и stderr
#     process.readyReadStandardOutput.connect(
#         lambda: print(process.readAllStandardOutput().data().decode('utf-8')))  # Вывод stdout
#     process.readyReadStandardError.connect(
#         lambda: print(process.readAllStandardError().data().decode('utf-8')))  # Вывод stderr
#
#     # должен быть ещё параметр output_path, но с ним почему-то не работает
#     args = ["-f", "MapInfo File",
#             "-a_srs", crsWkt,
#             '-lco', "ENCODING=CP1251",
#             "-lco", f"BOUNDS={bounds[0]},{bounds[1]},{bounds[2]},{bounds[3]}",
#             "-dsco", f"FORMAT={format}",
#             output_path,
#             input_path]
#
#     process.start("ogr2ogr", args)
#     process.waitForFinished()
#
#     if process.exitStatus() != QProcess.NormalExit osr process.exitCode() != 0:
#         print("Произошла ошибка при экспорте:", process.readAllStandardError().data().decode('utf-8'))
#     else:
#         print("Слой успешно экспортирован в формат .mif.")
#
# inputFile = 'C:/code/mapInfoBacksheevskoe/G521601.TAB'
# name = 'G521601'
# format = 'TAB'
# b = [70.3,53.4,76.4,58.6]
# ogr2ogrExport(inputFile,name,b,format)

# #**********************************************************************************************************************
### Рабочая конвертация ogr2ogr
# import subprocess
# #------------------------- ogr2ogr экспорт вектора -------------------------#
# def ogr2ogrExport(input, name, format):
#     #input_path = r"C:/code/mapInfoBacksheevskoe/G521601.TAB"
#     input_path = input
#     output_path = r"C:/Users/shelipov.aa/Desktop/py/exportTest/"+name+'.'+format.lower()
#     crsWkt = 'ENGCRS["NonEarth",EDATUM["Unknown engineering datum"],CS[Cartesian,2],AXIS["(E)",east,ORDER[1],LENGTHUNIT["METER",1]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]'
#     args = ["ogr2ogr",
#             "-f", "MapInfo File",
#             "-a_srs", crsWkt,
#             '-lco', "ENCODING=CP1251",
#             "-lco", "BOUNDS=-10000000,-10000000,10000000,10000000", # -lco задаёт пределы новому, создаваемому слою
#             "-dsco", "FORMAT="+format,
#             output_path,
#             input_path]
#     process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     # Дождитесь завершения процесса и получите вывод
#     stdout, stderr = process.communicate()
#     # Проверьте вывод на наличие ошибок
#     if stderr:
#         print("Произошла ошибка при экспорте:", stderr)
#     else:
#         print("Слой успешно экспортирован в формат .mif.")
# #------------------------- управление -------------------------#
# # Получить объект проекта QGIS
# project = QgsProject.instance()
# # Получить слой по его имени
# layer_name = "G521601"
# layer = project.mapLayersByName(layer_name)[0]
# # Используйте путь к слою
# path = layer.dataProvider().dataSourceUri()
# if "|" in path:
#     path = path.split('|')[0]
# print(path)
# f1='MIF'
# f2='TAB'
# ogr2ogrExport(path, layer_name, f2)
# #**********************************************************************************************************************
# from qgis.core import QgsRectangle
#
# # Предположим, что у вас уже есть слой layer и его ограничивающий прямоугольник
# layer_extent = layer.extent()
#
# # Предположим, что у вас есть словарь с координатами прямоугольников
# coordinates_dict = {
#     "rect1": (xmin1, ymin1, xmax1, ymax1),
#     "rect2": (xmin2, ymin2, xmax2, ymax2),
#     # Другие прямоугольники
# }
#
# for rect_name, rect_coords in coordinates_dict.items():
#     # Проверяем пересечение с ограничивающим прямоугольником слоя
#     if (rect_coords[0] < layer_extent.xMaximum() and
#         rect_coords[2] > layer_extent.xMinimum() and
#         rect_coords[1] < layer_extent.yMaximum() and
#         rect_coords[3] > layer_extent.yMinimum()):
#         # Найден прямоугольник, пересекающийся с слоем
#         # Здесь вы можете совершить любые нужные действия
#         print(f"Прямоугольник {rect_name} с координатами {rect_coords} пересекается со слоем")
# #**********************************************************************************************************************
# спрятать прогресс-бар, во время выполнения появляется, отображаются проценты, после выполнения надпись - успешно
# на секунды три, потом снова прятать прогресс-бар/
# ####
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
# from PyQt5.QtCore import QTimer
# # прикрутить в основной модуль через сигнал изменения текста, сетается текст, срабатывет сигнал, надпись прячется
# class MyMainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.label = QLabel('Привет, мир!', self)
#         self.label.adjustSize()
#
#         # Устанавливаем таймер для скрытия текста через 3 секунды
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.hide_text)
#         self.timer.start(3000)  # 3000 миллисекунд = 3 секунды
#
#     def hide_text(self):
#         self.label.hide()
#         self.timer.stop()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec_())
# В этом примере мы создаем главное окно с помощью PyQt, добавляем метку (label) с текстом "Привет, мир!"
# и устанавливаем таймер для вызова функции hide_text через 3 секунды.
# Функция hide_text скрывает метку после истечения времени.
# Это конечно лишь простой пример, который можно дальше настраивать в зависимости от ваших потребностей.
# В плагине PyGIS вы можете использовать подход примерно такой же, чтобы управлять отображением текста на вашей карте.
# #**********************************************************************************************************************
# В случае если фалй map info содержит несколько слоёв:
### from osgeo import ogr
#
# # Укажите путь к вашему файлу MapInfo
# file_path = 'путь_к_вашему_файлу.mapinfo'
#
# # Открываем файл
# driver = ogr.GetDriverByName('MapInfo File')
# dataset = driver.Open(file_path, 0)  # 0 означает чтение
#
# if dataset is None:
#     print('Не удалось открыть файл.')
# else:
#     # Получаем количество слоев в файле
#     num_layers = dataset.GetLayerCount()
#
#     if num_layers < 2:
#         print('Файл содержит меньше чем 2 слоя.')
#     else:
#         # Получаем первый слой
#         layer1 = dataset.GetLayerByIndex(0)
#         # Получаем второй слой
#         layer2 = dataset.GetLayerByIndex(1)
#
#         # Теперь у вас есть доступ к двум слоям и можете работать с ними дальше
# #**********************************************************************************************************************
# Вырезано из метода runInit()
### self.clearProgressBar()
# self.dlg.crsLabel.clear()  # СК.
# self.dlg.units.clear()  # Единицы измерения.
# self.dlg.selectLayerBox.clear()  # Очистка selectLayerBox и formatBox от предыдущих запусков.
# self.dlg.formatBox.clear()
# self.dlg.boundsBox.clear()
# #**********************************************************************************************************************
# Нахождение попаданий в пределы
### Чтение данных о границах субъекта из .csv файла
# subject_bounds = pd.read_csv('C:/Users/shelipov.aa/Desktop/defaultBounds1.csv', encoding='cp1251')  # read_file
# l = iface.activeLayer()
# ex = l.extent()
#
# xmin = ex.xMinimum()
# ymin = ex.yMinimum()
# xmax = ex.xMaximum()
# ymax = ex.yMaximum()
#
# print('xmin', xmin, '\n'
#                     'ymin', ymin, '\n'
#                                   'xmax', xmax, '\n'
#                                                 'ymax', ymax)
#
# cA = 0
# cD = 0
# # Перебор строк в данных о границах субъекта
# for index, row in subject_bounds.iterrows():
#     subject_name = row['Name']
#     subject_xmin = row['xmin']
#     subject_ymin = row['ymin']
#     subject_xmax = row['xmax']
#     subject_ymax = row['ymax']
#
#     # Сравнение границ карты с границами субъекта
#     if (xmin >= subject_xmin and ymin >= subject_ymin and
#             xmax <= subject_xmax and ymax <= subject_ymax):
#         cA = cA + 1
#         print("Карта укладывается в границы субъекта:", subject_name)
#     else:
#         cD = cD + 1
#         # print("Карта  НЕ укладывается в границы субъекта:", subject_name)
#
# print('Количество субъектов в которые попадает слой = ', cA, '\n'
#                                                              'Количество субъектов в которые слой не попал =  ', cD)
# #**********************************************************************************************************************
# Скрипт поиска пути к файлу по названию слоя
### from qgis.core import QgsProject
# from pathlib import Path
#
# # Задаем название искомого векторного слоя
# layer_name = iface.activeLayer().name()
# print(layer_name)
#
# # Получаем объект проекта QGIS
# project = QgsProject.instance()
#
# # Получаем все векторные слои в проекте
# map_layers = project.mapLayers()
#
# # Ищем нужный слой по его названию
# target_layer = None
# for layer_id, layer in map_layers.items():
#     if layer.name() == layer_name:
#         target_layer = layer
#         break
#
# # Если нашелся искомый слой, получаем его путь
# if target_layer:
#     layer_source = target_layer.source()
#     layer_path = Path(layer_source)
#     print("Путь к расположению векторного слоя:", layer_path)
# else:
#     print("Слой с таким названием не найден в проекте")
# #**********************************************************************************************************************
# Построение прямоугольников и csv файла
### Импортирование необходимых модулей
# from qgis.core import QgsVectorLayer, QgsProject
# from qgis.PyQt.QtCore import QVariant
# import csv
#
# # Путь к файлу CSV
# csv_file_path = 'C:/Users/shelipov.aa/Desktop/defaultBounds1.csv'
#
# # Создание пустого векторного слоя для прямоугольников
# layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "rectangles", "memory")
# provider = layer.dataProvider()
# provider.addAttributes([QgsField('Name', QVariant.String)])  # Добавление поля для хранения названия
#
# # Открытие файла CSV и чтение координат для создания прямоугольников
# # Открытие файла CSV и чтение координат для создания прямоугольников
# with open(csv_file_path, 'r', encoding='cp1251') as csvfile:  # Убедитесь, что правильная кодировка используется
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         xmin = float(row['xmin'])
#         ymin = float(row['ymin'])
#         xmax = float(row['xmax'])
#         ymax = float(row['ymax'])
#         name = row['Name']
#
#         # Создание прямоугольника на основе координат
#         rectangle = [QgsPointXY(xmin, ymin), QgsPointXY(xmin, ymax), QgsPointXY(xmax, ymax), QgsPointXY(xmax, ymin)]
#         feature = QgsFeature()
#         feature.setGeometry(QgsGeometry.fromPolygonXY([rectangle]))
#         feature.setAttributes([name])  # Установка названия
#         provider.addFeatures([feature])
#
# # Добавление созданного слоя в проект QGIS
# QgsProject.instance().addMapLayer(layer)
# #**********************************************************************************************************************
# Плохая идея делать так
### import geopandas as gpd
# import pandas as pd
#
# # Загрузка геоданных субъектов и карты
# subject_boundaries = gpd.read_file('C:/Users/shelipov.aa/Desktop/defaultBounds1.csv', encoding='cp1251')
# map_data = gpd.read_file('C:/Users/shelipov.aa/Documents/msk.shp', encoding='cp1251')
#
# # Определение пересечений между объектами и границами субъектов
# intersection = gpd.sjoin(map_data, subject_boundaries, how="left", op='intersects')
#
# # Объединение с результатом пересечений для добавления названия субъекта
# intersection_with_names = intersection.merge(subject_boundaries[['Name']], how='left', left_on='index_right', right_index=True)
#
# print(intersection_with_names)
#**********************************************************************************************************************
# Рабочее!
### нахождение ВХОЖДЕНИЯ СЛОЯ В ПРЕДЕЛЫ из csv файла
# import pandas as pd
# from osgeo import ogr
# from qgis.core import QgsProject
# from pathlib import Path
#
# from qgis.utils import iface
#
# # Чтение данных о границах субъекта из .csv файла
# subject_bounds = pd.read_csv('C:/Users/shelipov.aa/Desktop/defaultBounds1.csv', encoding='cp1251')  # read_file
#
# def findActiveLayerPath(layer_name):
#     # Задаем название искомого векторного слоя
#     # layer_name = iface.activeLayer().name()
#     print(layer_name)
#     # Получаем объект проекта QGIS
#     project = QgsProject.instance()
#     # Получаем все векторные слои в проекте
#     map_layers = project.mapLayers()
#     # Ищем нужный слой по его названию
#     target_layer = None
#     for layer_id, layer in map_layers.items():
#         if layer.name() == layer_name:
#             target_layer = layer
#             break
#     # Если нашелся искомый слой, получаем его путь
#     if target_layer:
#         layer_source = target_layer.source()
#         layer_path = Path(layer_source)
#         print('layer_source = ', layer_source)
#         print('layer_path = ', layer_path)
#         print("Путь к расположению векторного слоя:", layer_path)
#     else:
#         print("Слой с таким названием не найден в проекте")
#     return layer_path
#
# l = findActiveLayerPath('komi')  # сюда нужно передавать имя слоя проекта из comboBox
# c = 1
# dataSource = ogr.Open(l, 0)
# layer = dataSource.GetLayer()
#
# xmin = 0; ymin = 0; xmax = 0; ymax = 0
#
# # Перебираем все объекты и вычисляем ограничивающий прямоугольник
# for feature in layer:
#     geom = feature.GetGeometryRef()
#     xmin, xmax, ymin, ymax = geom.GetEnvelope()
#     print(feature, )
#     # Выводим результат
#     print("xmin:", xmin)
#     print("ymin:", ymin)
#     print("xmax:", xmax)
#     print("ymax:", ymax)
#
# # фактические значения границ карты
# map_bounds = (xmin, ymin, xmax, ymax)
# cA = 0; cD = 0
# # Перебор строк в данных о границах субъекта
# for index, row in subject_bounds.iterrows():
#     subject_name = row['Name']
#     subject_xmin = row['xmin']
#     subject_ymin = row['ymin']
#     subject_xmax = row['xmax']
#     subject_ymax = row['ymax']
#
#     # Сравнение границ карты с границами субъекта
#     if (xmin >= subject_xmin and ymin >= subject_ymin and
#             xmax <= subject_xmax and ymax <= subject_ymax):
#         cA = cA + 1
#         print("Карта укладывается в границы субъекта:", subject_name)
#     else:
#         cD = cD + 1
#         # print("Карта  НЕ укладывается в границы субъекта:", subject_name)
#
# print('Количество субъектов в которые попадает слой = ', cA, '\n'
#                                                              'Количество субъектов в которые слой не попал =  ', cD)
#**********************************************************************************************************************
### ДЛЯ ТЕСТА И ПРОВЕРОК КООРДИНАТ
# from osgeo import ogr
# import math
# import csv
#
# l = 'C:/Users/shelipov.aa/Desktop/py/exportTest/geoj/russia_geojson_wgs84.gpkg'
# c = 1
# dataSource = ogr.Open(l, 0)
# layer = dataSource.GetLayer()
# xmin = 0
# ymin = 0
# xmax = 0
# ymax = 0
#
# with open(output_file, 'w', newline='', encoding='cp1251') as csvfile:
#     fieldnames = ['Feature ID', 'Name', 'xmin', 'ymin', 'xmax', 'ymax']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     # Перебираем все объекты и вычисляем ограничивающий прямоугольник
#     for feature in layer:
#         geom = feature.GetGeometryRef()
#         xmin, xmax, ymin, ymax = geom.GetEnvelope()
#
#         print("Feature ID:", feature.GetFID(), feature['name'])
#         print("xmin:", xmin)
#         print("ymin:", ymin)
#         print("xmax:", xmax)
#         print("ymax:", ymax)
#         print('')
#         print('xmin - 0.5 =', xmin - 0.5)
#         print('ymin - 0.5 =', ymin - 0.5)
#         print('xmax + 0.5 =', xmax + 0.5)
#         print('ymax + 0.5 =', ymax + 0.5)
#         print('')
#         xmin = math.floor(xmin - 0.5)
#         ymin = math.floor(ymin - 0.5)
#         xmax = round(xmax + 0.5)        # xmax = math.ceil(xmax + 0.5)
#         ymax = round(ymax + 0.5)        # ymax = math.ceil(ymax + 0.5)
#
#         print('math.floor(xmin - 0.5) =', xmin)
#         print('math.floor(ymin - 0.5) =', ymin)
#         print('round(xmax + 0.5) =', xmax)
#         print('round(ymax + 0.5) =', ymax)
#         print('')
#         print("Результирующие записи", feature.GetFID(), feature['name'])
#         print("xmin:", xmin)
#         print("ymin:", ymin)
#         print("xmax:", xmax)
#         print("ymax:", ymax)
#         print('')
#         if feature.GetFID() == 3:
#             break
#**********************************************************************************************************************
### from qgis.core import QgsVectorLayer, QgsGeometry
#
# # Загрузка векторного слоя с границами субъекта
# subject_bounds_layer = QgsVectorLayer('defaultBounds1.csv', 'subject_bounds', 'ogr')
#
# # Загрузка векторного слоя с вашей картой или другими объектами
# map_layer = QgsVectorLayer('randomLayer.shp', 'map_data', 'ogr')
#
# # Получение экстента картографического слоя
# map_extent = map_layer.extent()
#
# # Получение экстента слоя с границами субъекта
# subject_extent = subject_bounds_layer.extent()
#
# # Создание геометрии QgsGeometry из экстентов
# map_geometry = QgsGeometry.fromRect(map_extent)
# subject_geometry = QgsGeometry.fromRect(subject_extent)
#
# # Проверка, попадает ли экстент картографического слоя в экстент границ субъекта
# if map_geometry.intersects(subject_geometry):
#     print("Карта укладывается в границы субъекта")
# else:
#     print("Карта не укладывается в границы субъекта")
#**********************************************************************************************************************
# Если границы субъектов хранятся в формате .csv и представляют из себя 4 точки (xmin, ymin, xmax, ymax),
# то вы можете использовать библиотеку pandas для чтения данных из .csv файла и затем сравнить границы карты с
# границами субъекта, используя эти координаты.
# Вот пример того, как вы можете сделать это с использованием Python и pandas:
### import pandas as pd
# from osgeo import ogr
#
# # Чтение данных о границах субъекта из .csv файла
# subject_bounds = pd.read_csv('C:/Users/shelipov.aa/Desktop/defaultBounds1.csv', encoding='cp1251')
#
# l = 'C:/Users/shelipov.aa/Documents/msk.shp'
# c=1
# dataSource = ogr.Open(l, 0)
# layer = dataSource.GetLayer()
#
# # Перебираем все объекты и вычисляем ограничивающий прямоугольник
# for feature in layer:
#     geom = feature.GetGeometryRef()
#     xmin, xmax, ymin, ymax = geom.GetEnvelope()
#
#     # Выводим результат
#     print("xmin:", xmin)
#     print("ymin:", ymin)
#     print("xmax:", xmax)
#     print("ymax:", ymax)
#
# # Получение границ карты
# map_bounds = (xmin, ymin, xmax, ymax)  # замените на фактические значения границ вашей карты
#
# # Перебор строк в данных о границах субъекта
# for index, row in subject_bounds.iterrows():
#     subject_xmin = row['xmin']
#     subject_ymin = row['ymin']
#     subject_xmax = row['xmax']
#     subject_ymax = row['ymax']
#
#     # Сравнение границ карты с границами субъекта
#     if (xmin >= subject_xmin and ymin >= subject_ymin and
#             xmax <= subject_xmax and ymax <= subject_ymax):
#         print("Карта укладывается в границы субъекта")
#         break
# else:
#     print("Карта не укладывается в границы субъекта")
#**********************************************************************************************************************
### ПРОВЕРИТЬ
# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import Polygon
#
# # Чтение .csv файла с данными о прямоугольных областях
# data = pd.read_csv('C:/Users/shelipov.aa/Desktop/defaultBounds1.csv', encoding='cp1251')  # Подставьте путь к вашему .csv файлу
# 
# # Создание геометрических объектов Polygon на основе данных о четырех точках
# geometry = [Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)]) for x1, y1, x2, y2 in zip(data.xmin, data.ymin, data.xmax, data.ymax)]
#
# # # Определение координатной системы
# # crs = {'init': 'epsg:4326'}  # Предполагается, что используется географическая система координат WGS 84
#
# # Создание GeoDataFrame
# geo_data = gpd.GeoDataFrame(data, geometry=geometry)
#
# # Создание прямоугольной области для заданных координат
# bounds = (37.6, 55.7, 37.8, 55.9)  # Пример границ Москвы (xmin, ymin, xmax, ymax)
# search_area = Polygon([(bounds[0], bounds[1]), (bounds[2], bounds[1]), (bounds[2], bounds[3]), (bounds[0], bounds[3])])
#
# # Поиск прямоугольной области, которая содержит заданную область
# relevant_areas = geo_data[geo_data.geometry.contains(search_area)]
#
# if 'Name' in relevant_areas.columns:
#     # Поиск соответствующих областей
#     relevant_areas = geo_data[geo_data.geometry.contains(search_area)]
#
#     # Вывод названия и геометрии соответствующих областей
#     print(relevant_areas[['Name', 'geometry']])
# else:
#     print("Столбец 'Name' отсутствует в GeoDataFrame.")
#************************************
### ПРОВЕРИТЬ
# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import Polygon
#
# # Чтение .csv файла с данными, включающими координаты
# data = pd.read_csv('C:/Users/shelipov.aa/Desktop/defaultBounds1.csv', encoding='cp1251')  # Подставьте путь к вашему .csv файлу
#
# # Создание многоугольника на основе точек
# polygon = Polygon([(data['xmin'][0], data['ymin'][0]), (data['xmax'][0], data['ymin'][0]), (data['xmax'][0], data['ymax'][0]), (data['xmin'][0], data['ymax'][0])])
#
# # Создание GeoSeries с многоугольником
# geo_series = gpd.GeoSeries([polygon])
#
# # Создание GeoDataFrame
# geo_data = gpd.GeoDataFrame(geometry=geo_series)
#
# # Вывод первого элемента GeoDataFrame
# print(geo_data.head())
#**********************************************************************************************************************
#Для определения территориального субъекта, к которому относится объект на карте,
# обычно используются географические информационные системы (ГИС) или библиотеки для геопространственного анализа
# в языках программирования, такие как GeoPandas для Python, Turf.js для JavaScript, GeoTools для Java и другие.
# Обычно этот процесс включает определение принадлежности токи (или другой геометрии) к полигону, представляющему
# границы территориального субъекта. Этот процесс известен как "точка в полигоне" или "пространственный анализ".
#Вот пример того, как это можно сделать на Python с использованием библиотеки GeoPandas:
### from osgeo import ogr
# import geopandas as gpd
# from shapely.geometry import Point
#
# # Создание геометрического объекта для точки
# point = Point(37.6173, 55.7558)  # Например, координаты Москвы
#
# # Чтение геоданных субъектов
# gdf = gpd.read_file(
#     'C:/Users/shelipov.aa/Desktop/py/exportTest/geoj/russia_geojson_wgs84.gpkg')  # Подставьте путь к файлу с геоданными
#
# # Поиск территориального субъекта, к которому относится точка
# relevant_subject = gdf[gdf.geometry.contains(point)]
#
# # Вывод результата
# print(relevant_subject)
# print(relevant_subject['name'])
#**********************************************************************************************************************
# ПРОВЕРИТЬ. Открытие папки и добавление слоя в проект
### import os
# import subprocess
#
# # Предполагается, что у вас есть переменная output_path, содержащая путь к вашему экспортированному слою
#
# # Открываем папку в файловом менеджере
# output_folder = os.path.dirname(output_path)
# subprocess.Popen(f'explorer "{output_folder}"' if os.name == 'nt' else f'xdg-open "{output_folder}"', shell=True)

# Предполагается, что у вас есть переменная output_path, содержащая путь к вашему экспортированному слою
# и layer_name, содержащая желаемое имя для добавляемого слоя.
#
# # Импортируем необходимые классы
# from qgis.core import QgsVectorLayer, QgsProject
#
# # Добавляем экспортированный слой в проект
# layer = QgsVectorLayer(output_path, layer_name, "ogr")
# QgsProject.instance().addMapLayer(layer)
#**********************************************************************************************************************
# Данный код создаёт дополнительный диалог, по нажатию на кнопку.
### class NewDialog(QDialog):
#     def __init__(self, parent=None):
#         super(NewDialog, self).__init__(parent)
#         self.setFixedSize(300, 200)
#         self.setWindowTitle('Processing')  # Установка заголовка окна
#         layout = QVBoxLayout()  # Создание вертикального макета
#
#         label = QLabel('This is a new dialog!')  # Создание метки
#         layout.addWidget(label)  # Добавление метки на макет
#         self.name_input = QLineEdit()  # Создание поля для ввода
#         layout.addWidget(self.name_input)
#         button = QPushButton('Закрыть')  # Создание кнопки
#         button.clicked.connect(self.close)  # Подключение метода закрытия окна к событию клика
#         layout.addWidget(button)  # Добавление кнопки на макет
#         button = QPushButton('Выполнить')  # Создание кнопки
#         button.clicked.connect(self.close)  # Подключение метода закрытия окна к событию клика
#         layout.addWidget(button)  # Добавление кнопки на макет
#
#         self.setLayout(layout)  # Установка макета для диалогового окна
#
#     def submit_form(self):
#         name = self.name_input.text()
#         print('Submitted name:', name)
#         # Здесь вы можете выполнить дополнительные действия с полученными данными
#
#
# # Это функцию нужно создать в родительском классе, для вызова окна
# def procDialog(self):
#     newDlg = NewDialog()
#     newDlg.exec_()
#     pass
#**********************************************************************************************************************
# ПРОВЕРИТЬ (работает)
# import subprocess
#
# input_path = r"C:/Users/shelipov.aa/Downloads/pyqgis_masterclass/seismic_zones.shp"
# output_path = r"C:/Users/shelipov.aa/Desktop/py/exportTest/mapinfo1.mif"
# crsWkt = 'ENGCRS["NonEarth",EDATUM["Unknown engineering datum"],CS[Cartesian,2],AXIS["(E)",east,ORDER[1],LENGTHUNIT["METER",1]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]'
# xmin = 70
# ymin = 53
# xmax = 76
# ymax = 59
# args = ["ogr2ogr",
#         "-f", "MapInfo File",
#         "-a_srs", crsWkt,
#         '-lco', "ENCODING=CP1251",
#         "-lco", "BOUNDS=-10000000,-10000000,10000000,10000000", # -lco задаёт пределы новому, создаваемому слою
#         output_path,
#         input_path]
# process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # Дождитесь завершения процесса и получите вывод
# stdout, stderr = process.communicate()
# # Проверьте вывод на наличие ошибок
# if stderr:
#     print("Произошла ошибка при экспорте:", stderr)
# else:
#     print("Слой успешно экспортирован в формат .mif.")
#*******************************************
### import subprocess
# from PyQt5.QtWidgets import QApplication, QProgressDialog
# from PyQt5.QtCore import Qt
#
# app = QApplication([])
#
# input_path = "C:/Users/shelipov.aa/Downloads/pyqgis_masterclass/seismic_zones.shp"
# output_path = "C:/Users/shelipov.aa/Desktop/py/exportTest/mapinfo.tab"
#
# # Определяем функцию, которая будет вызываться для обновления прогресса
# def update_progress(current, total):
#     if progress_dialog is not None:
#         progress = int(current / total * 100)
#         progress_dialog.setValue(progress)
#
#
# crsWkt = 'ENGCRS["NonEarth",EDATUM["Unknown engineering datum"],CS[Cartesian,2],AXIS["(E)",east,ORDER[1],LENGTHUNIT["METER",1]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]'
# xmin = -180
# ymin = -62
# xmax = 180
# ymax = 72
#
# args = ["ogr2ogr",
#         "-f", "MapInfo File",
#         "-a_srs", crsWkt,
#         '-lco', "ENCODING=CP1251",
#         "-lco", "BOUNDS=-10000000,-10000000,10000000,10000000",
#         "-clipsrc", str(xmin), str(ymin), str(xmax), str(ymax),
#         output_path,
#         input_path]
#
# # Создаем диалог прогресса
# progress_dialog = QProgressDialog()
# progress_dialog.setWindowModality(Qt.WindowModal)
# progress_dialog.setWindowTitle('Выполняется экспорт...')
# progress_dialog.setLabelText('Идет процесс экспорта...')
# progress_dialog.setRange(0, 100)
#
# # Запускаем процесс в фоне
# process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# while True:
#     output = process.stdout.read(1)
#     if output == '' and process.poll() is not None:
#         break
#     if output:
#         # Обновляем прогресс
#         update_progress(current_progress, total_progress)
#
# # Дожидаемся завершения процесса
# stdout, stderr = process.communicate()
#
# # Проверяем вывод на наличие ошибок
# if stderr:
#     print("Произошла ошибка при экспорте:", stderr)
# else:
#     print("Слой успешно экспортирован в формат .tab.")
#
# app.exec_()
#**********************************************************************************************************************
### Сортировка и запись csv
# from pathlib import Path
# import pandas as pd
#
# filename = 'boundsWithFix.csv'
# baseDir = Path(__file__).resolve().parent.parent
# print(baseDir)
# filePath = baseDir.joinpath(filename)
# print(filePath)
#
# # assign dataset
# #csvData = pd.read_csv(r'C:\Users\shelipov.aa\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\export_map_info\bounds_coords.csv', encoding='windows-1251')
# csvData = pd.read_csv(r'D:\boundsWithFix.csv', encoding='windows-1251')
# print(csvData)
# # sort data frame
# csvData.sort_values(["Name"], inplace=True)
#
# #csvData.to_csv('sorted_bounds.csv')
# print(csvData)
# # index=False, позволяет не дублировать столбец id
# #csvData.to_csv(r'C:\Users\shelipov.aa\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\export_map_info\sortedBounds.csv', encoding='windows-1251', index=False)
# csvData.to_csv(r'D:\sortedBounds.csv', encoding='windows-1251', index=False)
#**********************************************************************************************************************
### Ненужный кусок кода
# filename = 'export_map_info/sortedBounds.csv'
# baseDir = Path(__file__).resolve().parent.parent
# filePath = baseDir.joinpath(filename)
# try:
#     with open(filePath, encoding='windows-1251') as r_file:
#         file_reader = csv.DictReader(r_file, delimiter=",")
#         for row in file_reader:
#             self.logMsg('Попал в цикл заполнения пределов, на позиции 0', 1)
#             self.dlg.boundsBox.addItem(row["name"])
# except (QgsException, Exception) as e:
#     print(e)
#     self.messageError()
#     QMessageBox.information(self.dlg,
#                             'Внимание',
#                             "Файл с координатами не обнаружен")
#**********************************************************************************************************************
# Получение словаря из csv файла
### import csv
# reader = csv.reader(open('sortedBounds.csv', encoding='windows-1251'))
#
# result = {}
# for row in reader:
#     key = row[2]
#     if key in result:
#         # implement your duplicate row handling here
#         pass
#     result[key] = row[3:]
# print(result)
# result.pop('name')
# print(result.keys())
#**********************************************************************************************************************
# Для умышленной ошибки
### crsSrc = selectedLayer.crs()
# wkt = ('ENGCRS["NonEarth",EDATUM["Unknown engineering datum"],CS[Cartesian,2],AXIS["(E)",east,ORDER[1],'
#        'LENGTHUNIT["METER",1]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]')
# crs = QgsCoordinateReferenceSystem(wkt)
# opt.ct = QgsCoordinateTransform(crsSrc, crs)
#**********************************************************************************************************************
# Бэкап функции сохранения
# Функция с основной логикой заполнения опций и сохранения.
###   def mainSaveFunc(self, layers, filename):
#         self.dlg.progressBar.setDisabled(False)
#         self.dlg.saveButton.setDisabled(True)
#         self.dlg.breakButton.setDisabled(False)
#         self.lockComboBox()
#         self.dlg.label_3.setText('Идёт сохранение...')
#         # Добавляем расширение, согласно индексу формата из formatBox (1 = true = TAB, 0 = false= MIF).
#         ext = '.tab' if self.dlg.formatBox.currentIndex() else '.mif'
#         filename = filename + ext
#         selectedLayerIndex = self.dlg.selectLayerBox.currentIndex()  # Получаем индекс слоя.
#         selectedLayer = layers[selectedLayerIndex]  # Получаем слой из списка по индексу.
#         self.logMsg("Получаем и формируем опции сохранения для дальнейшей передачи в writer", 1)
#         opt = QgsVectorFileWriter.SaveVectorOptions()  # Заполняем опции сохранения векторного слоя.
#         opt.fileEncoding = u'windows-1251'
#         opt.layerOptions = [self.boundsLine()]
#         opt.driverName = 'MapInfo file'
#         converter = QgsVectorFileWriter.FieldValueConverter()  # ПРОВЕРИТЬ ПО ЭКСПОРТНЫМ ФАЙЛАМ
#         opt.fieldValueConverter = converter
#         if self.dlg.styleCheck.isChecked(): opt.symbologyExport = QgsVectorFileWriter.FeatureSymbology
#         # Формат и расширение файла согласно индексу из formatBox (1 = true = TAB, 0 = false= MIF).
#         opt.datasourceOptions = ['FORMAT=TAB'] if self.dlg.formatBox.currentIndex() else ['FORMAT=MIF']
#         self.logMsg("Создание задачи и присваивание в неё QgsVectorFileWriterTask с выбранными опциями",
#                     1)
#         task = QgsVectorFileWriterTask(selectedLayer, filename, opt)  # Создаём фоновую задачу.
#         self.logMsg("Подключение task к сигналам ", 1)
#         task.writeComplete.connect(lambda: self.onComplete(filename, ext))  # Подключаем к сигналам.
#         task.errorOccurred.connect(self.onFail)
#         task.progressChanged.connect(lambda: self.progressTask(task))
#         self.logMsg("Попытка добавить task в taskManger", 1)
#         try:
#             QgsApplication.taskManager().addTask(task)
#         except (QgsException, Exception) as e:
#             print(e)
#             self.messageError()
#         else:
#             self.logMsg("Успешно. Task была добавлена в taskManger", 1)
#         self.linesEdit(2)
#         self.dlg.filePath.clear()
#**********************************************************************************************************************
# ПРОВЕРИТЬ
### crsid = int(crs.authid().split(':')[1])
#
#     extent = self.map.extent()
#
#     if crsid != 4326:  # reproject to EPSG:4326
#         src = QgsCoordinateReferenceSystem(crsid)
#         dest = QgsCoordinateReferenceSystem(4326)
#         xform = QgsCoordinateTransform(src, dest)
#         minxy = xform.transform(QgsPoint(extent.xMinimum(),
#                                          extent.yMinimum()))
#         maxxy = xform.transform(QgsPoint(extent.xMaximum(),
#                                          extent.yMaximum()))
#         minx, miny = minxy
#         maxx, maxy = maxxy
#     else:  # 4326
#         minx = extent.xMinimum()
#         miny = extent.yMinimum()
#         maxx = extent.xMaximum()
#         maxy = extent.yMaximum()
#**********************************************************************************************************************
# рабочий код для замены подмены строки и смены crs на план-схему NonEarth
### selectedLayer = iface.activeLayer()
# transCont = QgsProject.instance().transformContext()
# crsSrc = selectedLayer.crs()
# wkt = ('ENGCRS["NonEarth",EDATUM["Unknown engineering datum"],CS[Cartesian,2],AXIS["(E)",east,ORDER[1],LENGTHUNIT["METER",1]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]')
# crs = QgsCoordinateReferenceSystem()
# print('1) CRS = ',crs)
# crs.createFromWkt(wkt)
# print('2) crsSrc = ', crsSrc)
# print('3) crs = ', crs)
# trans = QgsCoordinateTransform(crsSrc, c, QgsProject.instance())
# print(trans)
#**********************************************************************************************************************
# А вот эта часть уже ругается с ошибкой, что в данном контексте нельзя трансформировать
### if self.dlg.planSchemeCheck.isChecked():
#     crsSrc = selectedLayer.crs()
#     wkt = (
#         'ENGCRS["NonEarth",EDATUM["Unknown engineering datum"],CS[Cartesian,2],AXIS["(E)",east,ORDER[1],LENGTHUNIT["METER",1]],AXIS["(N)",north,ORDER[2],LENGTHUNIT["METER",1]]]')
#     crs = QgsCoordinateReferenceSystem()
#     crs.createFromWkt(wkt)
#     trans = QgsCoordinateTransform(crsSrc,
#                                    crs,
#                                    QgsProject.instance()).transform(QgsRectangle(float(self.dlg.xmin.text()),
#                                                                                  float(self.dlg.xmin.text()),
#                                                                                  float(self.dlg.xmin.text()),
#                                                                                  float(self.dlg.xmin.text())))
#     opt.ct = trans
#**********************************************************************************************************************
### Старая логика доступности селекторов
# def clickInSelectLayerBox(self, layers):
#     self.logMsg("Подставляем CRS и единицы измерения, регулируем доступ к опциям", 1)
#     cIndex = self.dlg.selectLayerBox.currentIndex()
#     lUnits = 'градусы' if layers[cIndex].crs().mapUnits() else 'метры'
#     lCrs = layers[cIndex].crs().description()
#     self.dlg.crsLabel.setText(str(lCrs))
#     self.dlg.units.setText(str(lUnits))
#     if lUnits == 'градусы' and self.dlg.formatBox.currentIndex():  # Если градусы и .mif
#         self.dlg.planSchemeCheck.setChecked(False)
#         self.dlg.planSchemeCheck.setDisabled(True)
#         self.dlg.boundsBox.setDisabled(False)
#         self.dlg.nonEarthCheck.setDisabled(False)
#         # Старая логика доступности:
#         # self.dlg.boundsCheck.setChecked(False)
#         # self.dlg.boundsCheck.setDisabled(True)
#         # self.dlg.boundsCheck.setDisabled(False)
#         # self.dlg.clearDefButton.setDisabled(True)
#         # self.dlg.boundsBox.setDisabled(True)
#         # self.linesEdit(2)
#         # self.linesEdit(0)
#     elif lUnits == 'метры' and self.dlg.formatBox.currentIndex():  # Если градусы и .mif
#         self.dlg.boundsCheck.setDisabled(False)
#         self.dlg.planSchemeCheck.setChecked(False)
#         self.dlg.planSchemeCheck.setDisabled(True)
#         self.dlg.clearDefButton.setDisabled(False)
#         self.dlg.boundsBox.setDisabled(False)
#         self.dlg.nonEarthCheck.setDisabled(False)
#         # Старая логика доступности:
#         # self.setDefaultBounds()
#         # self.dlg.clearDefButton.setDisabled(True)
#         # self.dlg.boundsCheck.setChecked(False)
#         # self.linesEdit(3)
#         # self.linesEdit(0)
#     else:
#         self.dlg.boundsCheck.setDisabled(False)
#         self.dlg.planSchemeCheck.setDisabled(False)
#         self.dlg.clearDefButton.setDisabled(False)
#         self.dlg.boundsBox.setDisabled(False)
#         self.dlg.nonEarthCheck.setDisabled(False)
#         # self.setDefaultBounds()
#     if self.dlg.boundsCheck.isChecked():  # Если ручной ввод пределов, то селектор недоступен
#         self.dlg.boundsBox.setDisabled(True)
#     if lCrs == 'Nonearth':
#         self.dlg.nonEarthCheck.setDisabled(True)
#         self.dlg.nonEarthCheck.setChecked(False)
#**********************************************************************************************************************
