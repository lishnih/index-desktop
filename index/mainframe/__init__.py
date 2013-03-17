#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22, 2013-02-04

import sys, os, re, time, logging
from PySide import QtCore, QtGui, __version__

from mainframe_ui import Ui_MainWindow
from thread1 import th                  # Поток (уже созданный)
from export import Proceed              # Модуль обработки
from view_db import view_db

from lib.dump_funcs import plain, html_val, html


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

        # Схема обработки, используется при многоцелевом использовании скрипта
        self.task_scheme = None

        # Назначаем потоку callback-функции
        th.set_callback(self.update_func, self.ending_func)

        # Обрабатываем параметры
        self.proceed_args(args)

        # Инициализируем пути
        self.init_default_path('companydata', '~~', True)
        self.init_default_path('appdata',     '~~~', True)


# Callback-функции для Таймера

    def convert_time(self, msecs):
        secs = int(msecs / 1000)
        hours = int(secs / 3600)
        secs = secs - hours * 3600
        mins = int(secs / 60)
        secs = secs - mins * 60
        time_str = "{:02}:{:02}:{:02}".format(hours, mins, secs)
        return time_str


    def update_func(self, msecs):
        time_str = self.convert_time(msecs)
        self.ui.statusbar.showMessage(u"{}   |   Processing {}".format(self.sb_message, time_str))


    def ending_func(self, msecs, message=''):
        time_str = self.convert_time(msecs)
        message = u"   |   {}".format(message) if message else ''
        self.ui.statusbar.showMessage(u"{}   |   Processed in {}{}".format(self.sb_message, time_str, message))


# События

    def OnTaskDir(self):
        if th.isRunning():
            print("running...")
            return

        # Предлагаем выбрать пользователю директорию
        dialog = QtGui.QFileDialog(None, "Select Dir")
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            # Выбираем директорию
            fileNames = dialog.selectedFiles()
            selected_dir = fileNames[0]

            self.ui.tree.clear()

            # Отображаем путь в Статусбаре
            self.set_status(selected_dir)

            # Запускаем обработку
            datadir = self.settings.value("appdata")
            th.start(Proceed, selected_dir, args, datadir, tree_widget=self.ui.tree)


    def OnTaskFile(self):
        if th.isRunning():
            print("running...")
            return

        # Предлагаем выбрать пользователю файл
        dialog = QtGui.QFileDialog(None, "Select File")
        if dialog.exec_():
            # Выбираем файл
            fileNames = dialog.selectedFiles()
            selected_file = fileNames[0]

            self.ui.tree.clear()

            # Отображаем путь в Статусбаре
            self.set_status(selected_file)

            # Запускаем обработку
            datadir = self.settings.value("appdata")
            th.start(Proceed, selected_file, args, datadir, tree_widget=self.ui.tree)


    def OnClose(self):
        if th.isRunning():
            print("running...")
            return

        self.ui.tree.clear()


    def OnDebugMenu(self):
        from export import tracing

        dialog = QtGui.QDialog(self)

        gridLayout = QtGui.QGridLayout(dialog)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        splitter = QtGui.QSplitter(dialog)
        gridLayout.addWidget(splitter)

        text = QtGui.QPlainTextEdit(dialog)
        splitter.addWidget(text)

        text.setPlainText('\n'.join(tracing))

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()


    def OnTreeItemPressed(self, item, prev):
        if not item:
            self.ui.text1.setHtml('')
            self.ui.text2.setHtml('')
            return

        tmpl = u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
<head></head>
<body>
  <h3>{}</h3>
  {}
</body>
</html>"""
        it = 1

        text1 = item.data(0, QtCore.Qt.UserRole)
        if text1 is not None:
            obj_dump = html(text1, it)
            text1 = tmpl.format(u"", obj_dump)
        self.ui.text1.setHtml(text1)

        if th.isRunning():
            return

        text2 = item.data(1, QtCore.Qt.UserRole)
        if text2 is not None:
            obj_name = html_val(text2)
            obj_dump = html(text2, it)
            text2 = tmpl.format(obj_name, obj_dump)
        self.ui.text2.setHtml(text2)


    def OnToolBoxChanged(self, current):
        if current == 1:
            self.ui.db_tree.clear()
            view_db(self.ui.db_tree)


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
        if th.isRunning():
            th.terminate()
            event.ignore()

        # Сохраняем состояние окна
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        event.accept()


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

        if args.files:
            # Отображаем путь в Статусбаре
            self.set_status(args.files)

            # Запускаем обработку
            datadir = self.settings.value("appdata")
            th.start(Proceed, args.files, args, datadir, tree_widget=self.ui.tree)


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
            logging.info(u"Creating directory: {}".format(path))
            os.makedirs(path)

        if os.path.isdir(path):
            return True
        else:
            QtGui.QMessageBox.critical(None, "Error",
                "Could not create directory:\n{}".format(path))
            return False
