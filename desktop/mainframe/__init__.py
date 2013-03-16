#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22, 2013-02-04

import sys, os, re, time, logging
from PySide import QtCore, QtGui, __version__

from mainframe_ui import Ui_MainWindow
from dragwidget import DragWidget

from models    import DBSession, Base, Task
from models.db import initDb
from reg import reg_object, reg_object1
from task_item import init_task_item_from_db, update_row


# Настройки: [HKCU\Software\lishnih@gmail.com\<app_section>]
company_section = "lishnih@gmail.com"
app_section = re.sub(r'\W', '_', os.path.dirname(os.path.dirname(__file__)))


class MainFrame(QtGui.QMainWindow):
    def __init__(self, args=None):
        super(MainFrame, self).__init__()

        # Загружаем элементы окна
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Настройки / Восстанавливаем состояние окна
        self.settings = QtCore.QSettings(company_section, app_section)
        self.restoreGeometry(self.settings.value("geometry"))
        self.restoreState(self.settings.value("windowState"))

        # Сохраняем данные об окружении скрипта
        self.saveEnv()

        # Добавляем свой виджет
        verticalLayout = QtGui.QVBoxLayout(self.ui.widget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ui.gragWidget = DragWidget(self.ui.widget)
        self.ui.gragWidget.setObjectName("gragWidget")
        verticalLayout.addWidget(self.ui.gragWidget)

        # Обрабатываем параметры
        self.proceed_args(args)

        # Инициализируем пути
        self.init_default_path('companydata', '~~', True)
        self.init_default_path('appdata',     '~~~', True)
        self.init_default_path('indexscript', '../index')

        # Читаем из директории с базой данных данные о задачах
        self.appdata = self.settings.value("appdata")
        if self.appdata:
            self.loadScheme(self.appdata)


# События


    def OnAbout(self):
        msg  = u"Python: {}\n".format(sys.version)
        msg += u"PySide: {}\n".format(__version__)
        msg += u"Qt: {}\n\n".format(QtCore.__version__)
        msg += u"Core: {}\n".format(self.settings.value("lasttime/Core"))
        msg += u"AppData: {}\n\n".format(self.settings.value("appdata"))
        msg += u"Author: Stan <lishnih@gmail.com>\n"
        msg += u"License: MIT\n"
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


    def loadScheme(self, appdata):
        self.db_uri = 'sqlite:///{}/db.sqlite'.format(appdata)
        self.engine = initDb(self.db_uri, DBSession, Base)

        rows = DBSession.query(Task)
        for TASK in rows:
            init_task_item_from_db(self.ui.gragWidget, TASK)


    def saveScheme(self):
        for task in self.ui.gragWidget.tasks_list():
            update_row(task)

        DBSession.commit()


# Сервисные функции


    def set_status(self, message=''):
        if isinstance(message, (list, tuple)):
            message = u"{} и др. значения".format(message[0])
        self.sb_message = message
        self.ui.statusbar.showMessage(self.sb_message)


    def saveEnv(self):
        # Стат. данные первого запуска
        if not self.settings.contains("firsttime/time"):
            self.saveEnv_d("firsttime")

        # Стат. данные последнего запуска
        self.saveEnv_d("lasttime")

        # Кол-во запусков
        runs = self.settings.value("runs")
        if isinstance(runs, int):
            self.settings.setValue("runs", runs + 1)
        else:
            self.settings.setValue("runs", 1)


    def saveEnv_d(self, d=""):
        # Сохраняем данные рабочей среды
        self.settings.setValue(d+"/Python", sys.version)
        self.settings.setValue(d+"/PySide", __version__)
        self.settings.setValue(d+"/Qt", QtCore.__version__)

        # Время модификации данного файла
        try:
            mtime = time.localtime(os.path.getmtime(__file__))
            rev = time.strftime("%Y-%m-%d", mtime)
        except os.error:
            rev = "<undefined>"
        self.settings.setValue(d+"/Core", rev)

        # Стат. данные
        tt, ct = time.time(), time.ctime()
        self.settings.setValue(d+"/time", tt)
        self.settings.setValue(d+"/time_str", ct)


    def proceed_args(self, args):
        if args.datadir:
            print(u"Директория для данных: '{}'".format(self.settings.value("appdata")))
            sys.exit(0)

        if args.setdatadir:
            print(u"Назначение новой директории для данных!")
            try:    print(u"Было      | {}".format(self.settings.value("appdata")))
            except: print(u"Было      | {!r}".format(self.settings.value("appdata")))
            newdir = self.expand_path(args.setdatadir)
            self.settings.setValue("appdata", newdir)
            try:    print(u"Назначено | {}".format(self.settings.value("appdata")))
            except: print(u"Назначено | {!r}".format(self.settings.value("appdata")))
            sys.exit(0)

        if args.indexscript:
            print(u"Директория скрипта index: '{}'".format(self.settings.value("indexscript")))
            sys.exit(0)

        if args.setindexscript:
            print(u"Назначение директории скрипта index!")
            try:    print(u"Было      | {}".format(self.settings.value("indexscript")))
            except: print(u"Было      | {!r}".format(self.settings.value("indexscript")))
            newdir = self.expand_path(args.setindexscript)
            self.settings.setValue("indexscript", newdir)
            try:    print(u"Назначено | {}".format(self.settings.value("indexscript")))
            except: print(u"Назначено | {!r}".format(self.settings.value("indexscript")))
            sys.exit(0)


    def init_default_path(self, key, default, check=None):
        value = self.settings.value(key)

        if not value or not isinstance(value, basestring):
            value = self.expand_path(default)
            self.settings.setValue(key, value)

        if check and not self.check_path(value):
            self.settings.remove(key)


    def expand_path(self, path):
        if path == '~':
            value = os.path.expanduser("~")
            return value
        elif path == '~~':
            home = os.path.expanduser("~")
            value = os.path.join(home, company_section)
            return value
        elif path == '~~~':
            home = os.path.expanduser("~")
            value = os.path.join(home, company_section, app_section)
            return value
        else:
            return path


    def check_path(self, path):
        if not os.path.exists(path):
            logging.info("Creating directory: {}".format(path))
            os.makedirs(path)

        if os.path.isdir(path):
            return True
        else:
            QtGui.QMessageBox.critical(None, "Error",
                "Could not create directory:\n{}".format(path))
            return False
