# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ExportToMapInfo
                                 A QGIS plugin
 плагин экспортирует векторный слой в формат .tab
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-06-13
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Shelipov A.A.
        email                : horusadeptus@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtWidgets import QDialogButtonBox
from .boundsManager import selectInBoundsBox, onClickCheckButtonBox, linesEdit, setDefaultBounds, autoBounds
from .csvHandler import getDictFromCSV, fillBoundsBox
from .custom_bounds_dialog import CustomBoundsDialog, openCustomBoundsDialog, saveUserBounds
from .qTableWidgetManager import userTableInit
from .saveProcessHandler import saveFile
from .utils import getActiveLayer, logMsg, ogr2ogrCheckChange, selectOutputFile, formatChange, formatPathEdit, \
    layerExtent, addCustomAction
from .export_map_info_dialog import ExportToMapInfoDialog
import os.path
from .resources import *

# Попробовать изменить логику изменения строк. Не добавлять фальшивые, а сразу переинициализировать таблицу, для корре
# тного отображения и возможности авто-подстановки пределов. Иначе, по нажатию, на только что созданные пределы -
# вылетает ошибка..
class ExportToMapInfo:
    """QGIS Plugin Implementation."""

    # --------------<editor-fold desc="Код, в основном, сгенерированный PluginBuilder'ом">------------------------------
    def __init__(self, iface):
        self.iface = iface  # Save reference to the QGIS interface
        self.plugin_dir = os.path.dirname(__file__)  # initialize plugin directory
        locale = QSettings().value('locale/userLocale')[0:2]  # initialize locale
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ExportToMapInfo_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
        self.actions = []  # Declare instance attributes
        self.menu = self.tr(u'&Экспорт векторного слоя в формат MapInfo')
        self.first_start = None  # Check if plugin was started the first time in current QGIS session
        self.error = False

    def tr(self, message):
        return QCoreApplication.translate('ExportToMapInfo', message)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        addCustomAction(self)
        self.first_start = True
        self.error = False

    def unload(self):
        for action in self.actions:
            self.iface.removeCustomActionForLayerType(action)  # Удаляем действия
        if hasattr(self, 'dlg') and self.dlg:  # Проводим проверку наличия dlg и его состояния
            self.dlg.reject()  # Закрываем диалог, если он открыт
            #self.dlg.deleteLater()  # Отмечаем диалог для удаления
        if hasattr(self, 'cbd') and self.cbd:
            self.cbd.reject()

    # Основной метод точки входа в плагин.
    def run(self):
        """Run method that performs all the real work"""
        if self.first_start:
            logMsg("Модуль запускается", 1)
            # После входа в модуль переводим флаг first_start в False.
            self.first_start = False  # Флаг переводится в True в функции инициализации GUI.
            self.dlg = ExportToMapInfoDialog()
            self.cbd = CustomBoundsDialog()
            layer = getActiveLayer(self)  # Получаем активный слой.
            self.dlg.selectLayerLine.setText(layer.name())
            logMsg("Попытка запуска функции инициализации", 1)
            # self.runInit()  # Инициализация подключения сигналов и заполнения полей/селекторов.
            dictOfBounds = getDictFromCSV()  # Получение словаря из csv
            logMsg("Инициализация, подключение к сигналам, заполнение списков/полей", 1)
            fillBoundsBox(self, dictOfBounds)  # Заполнение списка названиями субъектов РФ
            self.dlg.boundsBox.currentTextChanged.connect(
                lambda: selectInBoundsBox(self, dictOfBounds))  # Сигнал выбора пределов.
            self.dlg.ogr2ogrCheck.stateChanged.connect(lambda: ogr2ogrCheckChange(self))  # Сигнал чека ogr2ogr.
            self.dlg.browseFileButton.clicked.connect(lambda: selectOutputFile(self))  # Выбор пути сохранения файла
            self.dlg.formatBox.currentIndexChanged.connect(lambda: formatChange(self))
            self.dlg.boundsCheck.clicked.connect(lambda: onClickCheckButtonBox(self))  # Редактирование BOUNDS
            self.dlg.clearButton.clicked.connect(lambda: linesEdit(self, 2))  # Очистка/дефолтные BOUNDS
            self.dlg.saveButton.clicked.connect(lambda: saveFile(self))  # Обработка сигнала 'Сохранить'
            self.cbd.saveButton.clicked.connect(lambda: saveUserBounds(self))  # Обработка сохранения пределов.
            self.dlg.defaultBoundsButton.clicked.connect(
                lambda: setDefaultBounds(self, 'click'))  # Сигнал копки стандартные пределы
            self.dlg.autoBoundsButton.clicked.connect(
                lambda: autoBounds(self, layer, dictOfBounds, 'click'))  # Сигнал кнопки авторасчёт пределов
            # Сигнал изменения строки "Путь сохранения". Должен изменяться formarBox(.mif/.tab)
            self.dlg.filePath.editingFinished.connect(lambda: formatPathEdit(self))
            self.dlg.saveUserBounds.clicked.connect(lambda: openCustomBoundsDialog(self))
            # Ограничение на ввод в строки bounds (знак минус, числа, точка).
            regex = QRegularExpression(r"^-?(\d{1,9}(\.\d{1,9})?)?$")
            validator = QRegularExpressionValidator(regex)
            self.dlg.xmin.setValidator(validator)  # Ограничение на ввод только чисел в строки bounds.
            self.dlg.ymin.setValidator(validator)
            self.dlg.xmax.setValidator(validator)
            self.dlg.ymax.setValidator(validator)
            self.dlg.button_box.button(QDialogButtonBox.Cancel).setText('Выход')
            self.dlg.formatBox.addItems(['MapInfo MIF', 'MapInfo TAB'])  # Добавляем в список расширения.
            lUnits = 'Градусы' if layer.crs().mapUnits() else 'Метры'  # Единицы измерения
            lCrsDescription = layer.crs().description()  # CRS
            lCrsId = layer.crs().authid()
            lExt = layerExtent(layer)  # Пределы выбранного слоя
            self.dlg.extentLabel.setText(f'({lExt[0]}, {lExt[1]}) ({lExt[2]}, {lExt[3]})')
            if lCrsId:
                self.dlg.crs.setText(str(f"{lCrsDescription} - {lCrsId} "))
            else:
                self.dlg.crs.setText(str(f"{lCrsDescription}"))
            self.dlg.units.setText(str(lUnits))
            self.dlg.boundsCheck.setChecked(False)  # Инициализация чеков и строк bounds.
            self.dlg.styleCheck.setChecked(False)
            #self.dlg.filePath.setReadOnly(True)  # Сокрытие возможности редактировать поле пути файла.
            userTableInit(self)  # Инициализация таблицы 'tableWidget'
            if lUnits == 'Градусы':  # Если ед.изм. = градусы, тогда автоматически подставляем пределы
                autoBounds(self, getActiveLayer(self), dictOfBounds, 'Init')  # Авто-подстановка пределов для текущего слоя
            elif lUnits == 'Метры':  # Если ед.изм. = метры, тогда подставляем дефолтные пределы
                setDefaultBounds(self, 'Init')
            logMsg("Попытка отображения диалогового окна пользователю", 1)
            self.dlg.show()  # show the dialog.
            logMsg("Диалоговое окно успешно отображено", 1)
            result = self.dlg.exec_()  # self.dlg.exec_() возвращает 1 при нажатии на ок (if result = True)
            if not result:  # Нажатие на cancel возвращает 0
                logMsg("Выход из модуля", 1)
                self.first_start = True  # После явного закрытия окна, так же переводим флаг.
        else:    # При повторном открытии модуля, если модуль уже запущен, сообщаем об этом пользователю.
            logMsg("Попытка запуска ещё одного экземпляра модуля", 1)
            QMessageBox.information(self.dlg,
                                    'Внимание',
                                    "Модуль уже запущен")
    # --------------</editor-fold>--------------------------------------------------------------------------------------