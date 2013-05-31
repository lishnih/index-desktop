#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-10

import sys
from PySide import QtCore, QtGui


from dialog_sources_ui import Ui_Dialog


class Sources(QtGui.QDialog):
    def __init__(self, parent, taskData, settings=None):
        super(Sources, self).__init__(parent)
#       self.parent = parent
#       self.taskData = taskData
        self.settings = settings

        # Загружаем элементы диалога
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Восстанавливаем состояние окна
        self.loadDialogSettings()

        # Добавляем виджеты
        for filename in taskData['sources']:
            self.ui.listWidget.addItem(filename)


# События


    def accept(self):
        self.saveDialogSettings()
        self.done(True)


    def reject(self):
        self.saveDialogSettings()
        self.done(False)


    def closeEvent(self, event):
        self.saveDialogSettings()


# Сервисные функции


    # Восстанавливаем состояние окна
    def loadDialogSettings(self):
        if self.settings:
            self.restoreGeometry(self.settings.value("geometry_sources"))
#           self.restoreState(self.settings.value("windowState_settings"))


    # Сохраняем состояние окна
    def saveDialogSettings(self):
        if self.settings:
            self.settings.setValue("geometry_sources", self.saveGeometry())
#           self.settings.setValue("windowState_settings", self.saveState())
