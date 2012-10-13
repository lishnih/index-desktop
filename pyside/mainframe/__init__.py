#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import sys, os, time
from PySide import QtCore, QtGui, __version__

from mainframe_ui import Ui_MainWindow
from thread1 import th                  # Поток (уже созданный)
from export import Proceed              # Модуль обработки
from view_db import view_db

from lib.dump_funcs import html, plain, html_r


# Настройки
company_section = "PySide"
app_section = "Db"


class MainFrame(QtGui.QMainWindow):
    def __init__(self, argv=None):
        super(MainFrame, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Восстанавливаем состояние окна
        settings = QtCore.QSettings(company_section, app_section)
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))

        # Схема обработки, используется при многоцелевом использовании скрипта
        self.task_scheme = None

        # Назначаем потоку callback-функции
        th.set_callback(self.update_func, self.ending_func)

        # Если передан параметр - обрабатываем
        if len(argv) > 1:
            filename = argv[1]
            if   os.path.isdir(filename):
                th.start(task.TaskDir, filename, self.ui.tree)
            elif os.path.isfile(filename):
                th.start(task.TaskFile, filename, self.ui.tree)
            else:
                print u"Необходимо задать имя файла или директории!"
                sys.exit(-1)


# Callback-функции для Таймера

    def convert_time(self, msecs):
        secs = int(msecs / 1000)
        hours = int(secs / 3600)
        secs = secs - hours * 3600
        mins = int(secs / 60)
        secs = secs - mins * 60
        time_str = "{:02}:{:02}:{:02}".format(hours, mins, secs)
        return time_str


    def set_status(self, message=''):
        self.sb_message = message
        self.ui.statusbar.showMessage(self.sb_message)


    def update_func(self, msecs):
        time_str = self.convert_time(msecs)
        self.ui.statusbar.showMessage(u"{}   |   Processing {}".format(self.sb_message, time_str))


    def ending_func(self, msecs, message=''):
        time_str = self.convert_time(msecs)
        message = u"   |   {}".format(message) if message else ''
        self.ui.statusbar.showMessage(u"{}   |   Processed in {}{}".format(self.sb_message, time_str, message))


# Слоты

    def OnTaskDir(self):
        if th.isRunning():
            print "running..."
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
            th.start(Proceed, selected_dir, tree_widget=self.ui.tree)


    def OnTaskFile(self):
        if th.isRunning():
            print "running..."
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
            th.start(Proceed, selected_file, tree_widget=self.ui.tree)


    def OnClose(self):
        if th.isRunning():
            print "running..."
            return

        self.ui.tree.clear()


    def OnDebugMenu(self):
        import presets

        dialog = QtGui.QDialog(self)

        gridLayout = QtGui.QGridLayout(dialog)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        splitter = QtGui.QSplitter(dialog)
        gridLayout.addWidget(splitter)

        text = QtGui.QPlainTextEdit(dialog)
        splitter.addWidget(text)

        text.setPlainText('\n'.join(presets.tracing))

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()


    def OnAbout(self):
        print u"Python: {}".format(sys.version)
        print u"PySide version: {}; Qt version: {}".format(__version__, QtCore.__version__)
        print u"Core: rev20120930"


    def OnAbout_Qt(self):
        QtGui.QApplication.aboutQt()


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

        text1 = item.data(0, QtCore.Qt.UserRole)
        if text1 is not None:
            obj_dump = html(text1)
            text1 = tmpl.format(u"", obj_dump)
        self.ui.text1.setHtml(text1)

        text2 = item.data(1, QtCore.Qt.UserRole)
        if text2 is not None:
            obj_name = html(text2)
            obj_dump = html_r(text2)
            text2 = tmpl.format(obj_name, obj_dump)
        self.ui.text2.setHtml(text2)


    def OnToolBoxChanged(self, current):
        if current == 1:
            self.ui.db_tree.clear()
            view_db(self.ui.db_tree)


    def closeEvent(self, event):
#       if self.userReallyWantsToQuit():
#           event.accept()
#       else:
#           event.ignore()

        if th.isRunning():
            th.terminate()

        settings = QtCore.QSettings(company_section, app_section)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

        while th.isRunning():
            print "Still running..."
            time.sleep(1)
