#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import re
import xlrd

from reg.sheet import reg_sheet
from reg.object import reg_object, reg_object1
from reg.result import reg_warning, reg_error, reg_exception
from models import DBSession, Report, Joint

from lib.sheet_funcs import get_int, get_str, get_value, get_index, get_date
from lib.sheet_parse import parse_report, parse_table_iter


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
#       parse_table(sh, table_options, SHEET)
        for row_dict, ROW in parse_table_iter(sh, table_options, SHEET):
            ROW._sheet = SHEET

            REPORT = reg_object1(Report, row_dict, SHEET)
            JOINT = reg_object1(Joint, row_dict, SHEET)
            if ROW:
                ROW._report = REPORT
                ROW._joint = JOINT

            try:
                DBSession.commit()
            except Exception, e:    # StatementError
                reg_error(ROW, e)
