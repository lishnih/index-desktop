#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import os
import xlrd

from reg.file  import reg_file
from proceed.sheet import proceed_sheet
from lib.data_funcs import filter_list


def proceed_file(filename, options, DIR):
    root, ext = os.path.splitext(filename)
    if ext == '.xls':
        FILE = reg_file(filename, DIR)

        basename = os.path.basename(filename)
        if basename[0] == '_':
            FILE.message = u"Файл не обрабатывается!"

        else:
            # Sheet
            book = xlrd.open_workbook(filename, on_demand=True)
    
            nsheets = book.nsheets
            FILE.nsheets = nsheets
    
            sheets = book.sheet_names()
            sheets_seq = options.get('sheets_seq', None)
    
            if sheets_seq:
                sheets_list = filter_list(sheets, sheets_seq)
            else:
                sheets_list = sheets
    
            for name in sheets_list:
                sh = book.sheet_by_name(name)
                i = sheets.index(name) if name in sheets else None
                proceed_sheet(sh, options, FILE, i)
                book.unload_sheet(name)
