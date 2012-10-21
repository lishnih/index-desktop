#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-01

import logging
import xlrd

from models import DBSession
from models.links import link_objects
from reg import reg_object, reg_object1
from reg.result import reg_warning, reg_error, reg_exception
from auto_funcs import call
from lib.data_funcs import get_list
from lib.sheet_funcs import get_int, get_str, get_value, get_index, get_date


def e_func(func_name, exception, e, *args, **kargs):
    msg = u"""
(((((((
Функция '{}' вызвала ошибку:
{} ({!r})!
Были переданый следующие параметры:
args: {!r}
kargs: {!r}
)))))))\n""".format(func_name, e, exception, args, kargs)
    OBJ = args[2]
    reg_error(OBJ, msg)


def parse_report(sh, options, SHEET):
    test = ''
    report_dict = dict(_task=TASK)
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

    if report_dict:
        ROWS = []
        for row_object in row_objects:
            ROWS.append(reg_object(row_object, row_dict, SHEET))
        for row_object in row_objects1:
            ROWS.append(reg_object1(row_object, row_dict, SHEET))

        link_objects(SHEET, *ROWS)


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

    row_objects  = get_list(options.get('row_objects'))
    row_objects1 = get_list(options.get('row_objects1'))

    for i in xrange(row_start - 1, sh.nrows):
        typical_column = get_value(sh, i, typical_index)
        if typical_column:
            TASK = SHEET._file._dir._task
            row_dict = dict(_task=TASK, i=i)
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

            for item, funcs_name in cols_funcs.items():
                for func_name in get_list(funcs_name):
                    call(func_name, row_dict, item, SHEET, error_callback=e_func)

            if test:
                row_dict['test'] = test

            if row_dict:
                ROWS = []
                for row_object in row_objects:
                    ROWS.append(reg_object(row_object, row_dict, SHEET))
                for row_object in row_objects1:
                    ROWS.append(reg_object1(row_object, row_dict, SHEET))

#                 try:
#                     DBSession.commit()
#                 except Exception, e:
#                     reg_exception(SHEET, Exception, e, name, source)

                link_objects(SHEET, *ROWS)

                yield row_dict, ROWS
