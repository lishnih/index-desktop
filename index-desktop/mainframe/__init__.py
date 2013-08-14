#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import sys, os, re
from PySide import QtCore, QtGui, __version__

from mainframe_ui import Ui_MainWindow
from dragwidget import DragWidget

from lib.info import __description__, __version__
from lib.backwardcompat import *
from lib.settings import Settings
from task_item import draw_task


# Настройки: [HKCU\Software\lishnih@gmail.com\<app_section>]
company_section = "lishnih@gmail.com"
app_section = re.sub(r'\W', '_', os.path.dirname(os.path.dirname(__file__)))


class MainFrame(QtGui.QMainWindow):
    def __init__(self, args=None):
        super(MainFrame, self).__init__()

        # Загружаем элементы окна
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Восстанавливаем состояние окна
        self.settings = QtCore.QSettings(company_section, app_section)
        self.restoreGeometry(self.settings.value("geometry"))
        self.restoreState(self.settings.value("windowState"))

        # Настройки
        self.s = Settings()
        self.s.saveEnv()

        # Добавляем свой виджет
        verticalLayout = QtGui.QVBoxLayout(self.ui.widget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ui.gragWidget = DragWidget(self.ui.widget, self.settings, self.s)
        self.ui.gragWidget.setObjectName("gragWidget")
        verticalLayout.addWidget(self.ui.gragWidget)

        # Читаем из директории с базой данных данные о задачах
        self.loadScheme()


# События


    def OnAbout(self):
        msg  = u"{0}\n".format(__description__)
        msg += u"Version: {0}\n\n".format(__version__)

        msg += u"Author: Stan <lishnih@gmail.com>\n"
        msg += u"License: MIT\n\n"

        msg += u"Python: {0}\n".format(sys.version)
        msg += u"PySide: {0}\n".format(__version__)
        msg += u"Qt: {0}\n".format(QtCore.__version__)
        QtGui.QMessageBox.about(None, "About", msg)


    def OnAbout_Qt(self):
        QtGui.QApplication.aboutQt()


    def closeEvent(self, event):
        # Сохраняем состояние окна
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        # Сохраняем данные о задачах
        self.saveScheme()
        event.accept()


# Основной функционал


    def loadScheme(self):
        tasks = self.s.get('tasks', [])
        for task in tasks:
            draw_task(self.ui.gragWidget, task)


    def saveScheme(self):
        tasks = []
        for task in self.ui.gragWidget.tasks_list():
            task_dict = {}
            for key, value in task.items():
                if isinstance(value, (simple_types, collections_types, dict)):
                    task_dict[key] = value
            tasks.append(task_dict)
        self.s.set('tasks', tasks)


# Сервисные функции


    def set_status(self, message=''):
        if isinstance(message, (list, tuple)):
            message = u"{0} и др. значения".format(message[0])
        self.sb_message = message
        self.ui.statusbar.showMessage(self.sb_message)
