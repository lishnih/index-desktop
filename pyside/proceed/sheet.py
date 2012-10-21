#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import re
import xlrd

from reg.sheet import reg_sheet
from reg import reg_object
from lib.sheet_parse import parse_report, parse_table


def proceed_sheet(sh, options, FILE, i=None):
    SHEET = reg_sheet(sh, FILE, i)

    sheet_test = options.get('sheet_test')
    if sheet_test:
        row, col, test_pattern = sheet_test
        test_cell = get_str(sh, row, col)
        res = re.search(test_pattern, test_cell)
        if res:
            SHEET.sheet_test = test_cell

    if 'report' in options:
        report_options = options.get('report')
        parse_report(sh, table_options, SHEET)

    if 'table' in options:
        table_options = options.get('table')
        parse_table(sh, table_options, SHEET)
