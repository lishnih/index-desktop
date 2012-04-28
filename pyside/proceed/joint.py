#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import logging
import xlrd

from reg.joint  import reg_joint
from reg.result import reg_warning, reg_error, reg_exception

from lib.sheet_funcs import get_int, get_str, get_value, get_index, get_date


def proceed_joint(sh, options, SHEET):
    row_start    = options.get('row_start', 1)
    cols_names   = options.get('cols_names', [])
    cols_funcs   = options.get('cols_funcs', {})

    check_name = options.get('check_name')
    col_index1 = cols_names.index(check_name) if check_name else None

    check_column = options.get('check_column', 'A')
    col_index2 = get_index(check_column)

    typical_index = col_index1 or col_index2

    for i in xrange(row_start - 1, sh.nrows - 1):
        typical_column = get_value(sh, i, typical_index)
        if typical_column:
            joint_dict = dict()
            col = 0
            test = u""

            for col_name in cols_names:
                if col_name:
                    if isinstance(col_name, basestring):
                        val = get_value(sh, i, col)
                        joint_dict[col_name] = val
                        test += u"({}:{}) '{}': '{}'\n".format(i, col, col_name, val)
                    if isinstance(col_name, list):
                        inner_row = 0
                        for inner_col_name in col_name:
                            if inner_col_name:
                                val = get_value(sh, i + inner_row, col)
                                joint_dict[inner_col_name] = val
                            inner_row += 1
                col += 1

            for item in cols_funcs:
                try:
                    joint_dict[item] = cols_funcs[item](joint_dict, item)
                except Exception, e:
                    logging.exception(u"Ошибка при обработке элемента '{}' функцией: '{}'!".format(item, e))

            if joint_dict:
                JOINT = reg_joint(joint_dict, SHEET)
                JOINT.test = test
