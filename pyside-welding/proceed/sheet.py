#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import xlrd

from sql.session import DBSession
from sql.model import Joint
from sheet_funcs import get_index, get_date


cols_items = ['y',                  # A
              'date',
              't',
              ['d1', 'd2'],         # D
              ['th1', 'th2'],
              '',
              'gost',               # G
              'wt',
              'kp',                 # I
              'type',
              'seq',
              ['elem1', 'elem2'],
              ['code1', 'code2'],   # M
              '',
              '',
              '',
              '',
              ['sn1', 'sn2'],       # R
              ['len1', 'len2'],
              ['', 'scheme'],       # T
]


def proceed_sheet(sh, sheet=None):
    for joint_dict in sheet_iter(sh):
        try:
            joint = Joint(**joint_dict)
            DBSession.add(joint)

            if sheet:
                sheet.joint.append(joint)

        except Exception, e:
            print sh.name, e


def sheet_iter(sh):
    row_start = 4

    for i in xrange(row_start, sh.nrows - 1):
        date = sh.cell_value(i, get_index("B"))
        if date:
            joint_dict = dict()
            col = 0
            for col_name in cols_items:
                if col_name:
                    if isinstance(col_name, basestring):
                        val = sh.cell_value(i, col)
                        joint_dict[col_name] = val
                    if isinstance(col_name, list):
                        inner_row = 0
                        for inner_col_name in col_name:
                            if inner_col_name:
                                val = sh.cell_value(i + inner_row, col)
                                joint_dict[inner_col_name] = val
                            inner_row += 1
                col += 1

            if 'date' in joint_dict:
                date, date_str = get_date(joint_dict['date'])
                joint_dict['date'] = date
                joint_dict['date_str'] = date_str

            yield joint_dict
