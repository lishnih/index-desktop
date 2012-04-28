#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import os
import xlrd

from reg.file import reg_file
from reg.result import reg_warning, reg_error, reg_exception
from proceed.sheet import proceed_sheet

from lib.data_funcs import filter_match, filter_list


def proceed_file(filename, options, DIR):
    root, ext = os.path.splitext(filename)

    if ext == '.xlsx':
        reg_warning(DIR, u"Файлы с расширением {} не поддерживаются!".format(ext))
        return

    if ext == '.xls':
        FILE = reg_file(filename, DIR)

        # Sheet
        book = xlrd.open_workbook(filename, on_demand=True)

        nsheets = book.nsheets
        FILE.nsheets = nsheets

        sheets = book.sheet_names()
        sheets_filter = options.get('sheets_filter')

        sheets_list = filter_list(sheets, sheets_filter)

        for name in sheets_list:
            sh = book.sheet_by_name(name)
            i = sheets.index(name)
            proceed_sheet(sh, options, FILE, i)
            book.unload_sheet(name)
