#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import sys
from PySide import QtCore, QtGui

import mainframe                # Основное окно


# def init_translator():
#     translator = QtCore.QTranslator()
#     translator.load("ru")
#     app.installTranslator(translator)


def main():
#   init_translator()                       # Настройка i18n

    app = QtGui.QApplication(sys.argv)      # Приложение
    frame = mainframe.MainFrame(sys.argv)   # Интерфейс
    frame.show()                            # Показываем
    res = app.exec_()                       # Цикл

    return res


if __name__ == '__main__':
    sys.exit(main())
