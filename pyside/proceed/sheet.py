#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import re
import xlrd

from reg.sheet import reg_sheet
from proceed.joint import proceed_joint

from lib.sheet_funcs import get_int, get_str, get_value, get_index, get_date


def proceed_sheet(sh, options, FILE, i=None):
    SHEET = reg_sheet(sh, FILE, i)

    if 'cols_names' not in options:
        msg = u"Параметры поиска стыков не указаны для '{}', пропускаем!".format(sh.name)
        reg_warning(SHEET, msg)
        return

    sheet_test = options.get('sheet_test')
    if sheet_test:
        row, col, test_pattern = sheet_test
        test_cell = get_str(sh, row, col)
        res = re.search(test_pattern, test_cell)
        if res:
            proceed_joint(sh, options, SHEET)
            SHEET.sheet_test = test_cell
    else:
        proceed_joint(sh, options, SHEET)
