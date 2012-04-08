#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

import os, sys
import xlrd
from PySide import QtCore

from sql.session import DBSession
from sql.model import *
from reg.task  import reg_task
from reg.dir   import reg_dir
from reg.file  import reg_file
from reg.sheet import reg_sheet
from proceed.sheet import proceed_sheet


def Proceed(entry, tree_item=None):
    filename = entry
    if isinstance(entry, QtCore.QFileInfo):
        filename = entry.absoluteFilePath()

    if os.path.isdir(filename):
        # Task
        task = reg_task(filename, u'Сварочный журнал', tree_item)

        # Dir
        for root, dirs, files in os.walk(filename):
            dir = reg_dir(root, task)

            for filename in files:
                # File
                filename = os.path.join(root, filename)
                ProceedFile(filename, dir)

    elif os.path.isfile(filename):
        # Task
        task = reg_task(filename, u'Сварочный журнал', tree_item)
    
        # Dir
        dirname = os.path.dirname(filename)
        dir = reg_dir(dirname, task)

        # File
        ProceedFile(filename, dir)

    else:
        print u'Не найден файл/директория!'

    DBSession.commit()


def ProceedFile(filename, dir):
    ext = os.path.splitext(filename)[1]
    if ext == '.xls':
        file = reg_file(filename, dir)

        # Sheet
        book = xlrd.open_workbook(filename)
        sheets = book.nsheets

        file.sheets = sheets

        for i in range(sheets):
            sh = book.sheet_by_index(i)
            if sh.name[0] != '_':

                sheet = reg_sheet(sh, file, i)
                proceed_sheet(sh, sheet)


def main(filename):
    filename = os.path.abspath(filename)
    print u"Обработка файла '{}'".format(filename)

    import transaction
    with transaction.manager:
        Proceed(filename)


if __name__ == '__main__':
    filename = u'../2_ALL_Log of welding.xls'
    sys.exit(main(filename))
