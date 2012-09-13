#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import os
import xlrd

from reg.file import reg_file
from reg.object import reg_object, set_object, set_info
from reg.result import reg_warning, reg_error, reg_exception
from proceed.sheet import proceed_sheet

from lib.data_funcs import filter_match, filter_list


def proceed_file(filename, options, DIR):
    basename = os.path.basename(filename)
    root, ext = os.path.splitext(basename)
    ext = ext.lower()

    if ext == '.xlsx':
        FILE = set_object(DIR, brief=u"Файлы с расширением {} не поддерживаются!".format(ext), name=basename)
        return

    if ext == '.xls':
        FILE = reg_file(basename, DIR)

        # Sheet
        book = xlrd.open_workbook(filename, on_demand=True, formatting_info=True)

        nsheets = book.nsheets
        FILE.nsheets = nsheets

        sheets = book.sheet_names()
        sheets_filter = options.get('sheets_filter')
        sheets_list = filter_list(sheets, sheets_filter)

        set_info(FILE, brief=[sheets, sheets_list])

        for name in sheets_list:
            sh = book.sheet_by_name(name)
            i = sheets.index(name)
            proceed_sheet(sh, options, FILE, i)
            book.unload_sheet(name)
        return

    FILE = set_object(DIR, brief=u"Этот файл не индексируется!", name=basename)
