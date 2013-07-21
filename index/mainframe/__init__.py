#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import sys, os, re
from PySide import QtCore, QtGui, __version__

from mainframe_ui import Ui_MainWindow
from thread1 import th                  # Поток (уже созданный)
from export import ProceedInit          # Модуль обработки
from view_db import view_db

from lib.info import __description__, __version__
from lib.backwardcompat import *
from lib.settings import Settings
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

        # Восстанавливаем состояние окна
        self.settings = QtCore.QSettings(company_section, app_section)
        self.restoreGeometry(self.settings.value("geometry"))
        self.restoreState(self.settings.value("windowState"))

        # Настройки
        self.s = Settings()
        self.s.saveEnv()

        # Назначаем потоку callback-функции
        th.set_callback(self.update_func, self.ending_func)

        # Инициализируем datadir
        self.s.init_path('datadir', '~~~')

        # Обрабатываем параметры
        self.proceed_args(args)


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
        self.ui.statusbar.showMessage(u"{0}   |   Processing {1}".format(self.sb_message, time_str))


    def ending_func(self, msecs, message=''):
        time_str = self.convert_time(msecs)
        message = u"   |   {0}".format(message) if message else ''
        self.ui.statusbar.showMessage(u"{0}   |   Processed in {1}{2}".format(self.sb_message, time_str, message))


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
            th.start(ProceedInit, selected_dir, self.s, {}, tree_widget=self.ui.tree)


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
            th.start(ProceedInit, selected_file, self.s, {}, tree_widget=self.ui.tree)


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
  <h3>{0}</h3>
  {1}
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
            message = u"{0} и др. значения".format(message[0])
        self.sb_message = message
        self.ui.statusbar.showMessage(self.sb_message)


    def proceed_args(self, args):
        if args.files:
            # Отображаем путь в Статусбаре
            self.set_status(args.files)

            # Запускаем обработку
            args = dict(args._get_kwargs())
            th.start(ProceedInit, args['files'], self.s, args, tree_widget=self.ui.tree)
