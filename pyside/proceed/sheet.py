#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import xlrd

from reg.sheet import reg_sheet
from proceed.joint import proceed_joint

from lib.sheet_funcs import get_value, get_index, get_date


def proceed_sheet(sh, options, FILE, i=None):
    SHEET = reg_sheet(sh, FILE, i)

    if 'cols_names' not in options:
        msg = u"Параметры поиска стыков не указаны для '{}', пропускаем!".format(sh.name)
        reg_warning(SHEET, msg)
        return

    proceed_joint(sh, options, SHEET)
