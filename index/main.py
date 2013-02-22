#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22, 2013-01-28

import sys
from PySide import QtCore, QtGui

from mainframe import MainFrame             # Основное окно


# def init_translator():
#     translator = QtCore.QTranslator()
#     translator.load("ru")
#     app.installTranslator(translator)


# def init_trayicon():
#     if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
#         QtGui.QMessageBox.critical(None, "Systray",
#             "I couldn't detect any system tray on this system.")
#         return
#
#     QtGui.QApplication.setQuitOnLastWindowClosed(False)


def main():
#   init_translator()                       # i18n
#   init_trayicon()                         # Трей

    app = QtGui.QApplication(sys.argv)      # Приложение

    frame = MainFrame(sys.argv)             # Инициализируем
    frame.show()                            # Отображаем

    res = app.exec_()                       # Цикл
    return res


if __name__ == '__main__':
    sys.exit(main())
