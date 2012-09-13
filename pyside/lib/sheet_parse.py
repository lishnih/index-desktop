#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-01

import logging
import xlrd

from lib.sheet_funcs import get_int, get_str, get_value, get_index, get_date
from reg.object import reg_object


def parse_report(sh, options, SHEET):
    test = ''
    report_dict = dict(_sheet=SHEET)
    for key, params in report_options.items():
        l = len(params)
        if l == 2:
            row, col = params
            val = get_str(sh, row, col)
            report_dict[key] = val
            test += u"{} [{},{}]: '{}'\n".format(key, row, col, val)
        elif l == 3:
            row, col, pattern = params
            val = get_str(sh, row, col)
            report_dict[key] = val
            test += u"{} [{},{},{}]: '{}'\n".format(key, row, col, pattern, val)

    REPORT = reg_object(Report, report_dict, SHEET)
    REPORT.test = test


def parse_table(sh, options, SHEET):
    for i in parse_table_iter(sh, options, SHEET):
        pass


def parse_table_iter(sh, options, SHEET):
    row_start  = options.get('row_start',  1)
    cols_names = options.get('cols_names', [])
    cols_funcs = options.get('cols_funcs', {})

    check_name = options.get('check_name')
    col_index1 = cols_names.index(check_name) if check_name else None

    check_column = options.get('check_column', 'A')
    col_index2 = get_index(check_column)

    typical_index = col_index1 or col_index2

    row_object = options.get('row_object')

    for i in xrange(row_start - 1, sh.nrows):
        typical_column = get_value(sh, i, typical_index)
        if typical_column:
            row_dict = dict(_sheet=SHEET)
            col = 0

            test = ''
            for col_name in cols_names:
                if col_name:
                    if isinstance(col_name, basestring):
                        val = get_value(sh, i, col)
                        row_dict[col_name] = val
                        test += u"({}:{}) '{}': '{}'\n".format(i, col, col_name, val)
                    if isinstance(col_name, list):
                        inner_row = 0
                        for inner_col_name in col_name:
                            if inner_col_name:
                                val = get_value(sh, i + inner_row, col)
                                row_dict[inner_col_name] = val
                            inner_row += 1
                col += 1

            for item in cols_funcs:
                try:
                    cols_funcs[item](row_dict, item)
                except Exception, e:
                    logging.exception(u"Ошибка при обработке элемента '{}' функцией: '{}'!".format(item, e))

            if test:
                row_dict['test'] = test

            if row_dict:
                if row_object:
                    ROW = reg_object(row_object, row_dict, SHEET)
                else:
                    ROW = None
                yield row_dict, ROW
