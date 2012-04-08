#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import sys, os, time, logging
from PySide import QtCore, QtGui, __version__

from mainframe_ui import Ui_MainWindow
from thread1 import th                  # Поток (уже созданный)
from export import Proceed              # Модуль обработки


# Настройки
company_section = "PySide"
app_section = "Db"

task_scheme = "default"


class MainFrame(QtGui.QMainWindow):
    def __init__(self, argv=None):
        super(MainFrame, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Восстанавливаем состояние окна
        settings = QtCore.QSettings(company_section, app_section)
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))

        self.sb_message = u"Схема обработки: %s" % task_scheme
        self.ui.statusbar.showMessage(self.sb_message)

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
        time_str = "%02d:%02d:%02d" % (hours, mins, secs)
        return time_str


    def update_func(self, msecs):
        time_str = self.convert_time(msecs)
        self.ui.statusbar.showMessage(u"%s   |   Processing %s" % (self.sb_message, time_str))


    def ending_func(self, msecs, message=None):
        time_str = self.convert_time(msecs)
        self.ui.statusbar.showMessage(u"%s   |   Processed in %s   |   %s" % (self.sb_message, time_str, message))

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
            self.sb_message = selected_dir
            self.update_func(0)

            # Запускаем обработку
            th.start(Proceed, selected_dir, self.ui.tree)


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
            self.sb_message = selected_file
            self.update_func(0)

            # Запускаем обработку
            th.start(Proceed, selected_file, self.ui.tree)


    def OnClose(self):
        if th.isRunning():
            print "running..."
            return

        self.ui.tree.clear()


    def OnAbout(self):
        print "PySide version: %s; Qt version: %s" % (__version__, QtCore.__version__)
        print "Core: rev20120311"


    def OnAbout_Qt(self):
        QtGui.QApplication.aboutQt()


    def OnTreeItemSelected(self):
        ti = self.ui.tree.currentItem()
        text1 = ti.data(0, QtCore.Qt.UserRole)
        text2 = ti.data(1, QtCore.Qt.UserRole)

        if not isinstance(text1, basestring):
            text1s = ""
            for key in dir(text1):
                if key[0] != '_':
                    try:
                        text1s += u"%s: %s\n" % (key, getattr(text1, key))
                    except:
                        text1s += u"%s: %r\n" % (key, getattr(text1, key))
            text1 = text1s

        if not isinstance(text2, basestring):
            text2 = repr(text2)

        self.ui.text1.setPlainText(text1)
        self.ui.text2.setPlainText(text2)


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
