#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-28

from proceed.auto_funcs import proceed_date


def get_sources():
    yield (
        u'../../Сварка/2_ALL_Log of welding3.xls',
        get_taskname(),
        get_default(),
    )


def get_taskname():
    return u'Сварка'


def get_default():
    return {
#       'dirs_filter':        None,
#       'files_filter':       None,
        'sheets_filter':      '/^[A-Z]{2,3}$/',
        'row_start':          5,
        'check_column':       'B',
        'cols_names': [
            'y',                  # A
            'date',
            't',
            ['d1', 'd2'],         # D
            ['th1', 'th2'],
            '',
            '',                   # G gost
            'wt',
            'kp',                 # I
            'type',
            'seq',
            ['elem1', 'elem2'],   # L
            ['code1', 'code2'],
            '',
            '',
            '',
            '',
            ['sn1', 'sn2'],       # R
            ['len1', 'len2'],
            ['', 'scheme'],       # T
        ],
        'cols_funcs': {
            'date': proceed_date,
        }
    }
