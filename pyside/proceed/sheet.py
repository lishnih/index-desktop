#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import xlrd

from reg.sheet  import reg_sheet
from reg.joint  import reg_joint
from reg.result import reg_ok, reg_warning, reg_error, reg_exception
from lib.sheet_funcs import get_value, get_index


def proceed_sheet(sh, options, FILE, i=None):
    SHEET = reg_sheet(sh, FILE, i)

    if 'cols_names' not in options:
        msg = u"Параметры поиска стыков не указаны для '{}', пропускаем!".format(sh.name)
        reg_warning(SHEET, msg)
        return

    for joint_dict in sheet_iter(sh, options):
        JOINT = reg_joint(joint_dict, SHEET)

    reg_ok(SHEET)



def sheet_iter(sh, options):
    row_start  = options.get('row_start', 1)
    col_check  = options.get('col_check', 'A')
    cols_names = options.get('cols_names', [])
    cols_funcs = options.get('cols_funcs', {})

    col_check_index = get_index(col_check)

    for i in xrange(row_start - 1, sh.nrows - 1):
        col_check = get_value(sh, i, col_check_index)
        if col_check:
            joint_dict = dict()
            col = 0
            for col_name in cols_names:
                if col_name:
                    if isinstance(col_name, basestring):
                        val = get_value(sh, i, col)
                        joint_dict[col_name] = val
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

            yield joint_dict
