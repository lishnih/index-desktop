#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import sys, logging
from PySide import QtCore, QtGui

from mainframe import MainFrame             # Основное окно
# from systray import SysTray               # Трей


# def init_translator():
#     translator = QtCore.QTranslator()
#     translator.load("ru")
#     app.installTranslator(translator)


def main(args=None):
#   init_translator()                       # i18n
#   tray = SysTray()                        # Трей

    app = QtGui.QApplication(sys.argv)      # Приложение

    frame = MainFrame(args)                 # Инициализируем
    frame.show()                            # Отображаем

    res = app.exec_()                       # Цикл
    return res


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    import argparse

    parser = argparse.ArgumentParser(description='Tools for creating tasks.')

    if sys.version_info >= (3,):
        argv = sys.argv
    else:
        fse = sys.getfilesystemencoding()
        argv = [i.decode(fse) for i in sys.argv]

    args = parser.parse_args(argv[1:])

    sys.exit(main(args))
