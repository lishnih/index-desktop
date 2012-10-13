#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-28


__revision__ = 20120929


import os

from models import Register_entry


if os.name == 'posix':
    homepath = u'/home/stan/pgu235'
elif os.name == 'nt':
    homepath = u'D:/opt/home/pgu235'


tracing = []


reports_config = {
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'ВИК.xls',
#   'sheets_filter':    u'',
    'sheet_test':       [0, 0, u'def: pgu235/СП_Астрахань_ОКК_Акт-ВИК-МК_001'],
    'report':    {
        'name_pre':         [9,  9],
        'name_seq':         [9, 11],
#       'name_sign':        [9,  9],
        'date':             [13, 0],
        'joints':           [24, 1],
        'cols_funcs': {
            'date': 'proceed_date',
        }
    },
}


registers_config = {
#   'dirs_filter':      None,
#   'dirs_level':       0,
#   'files_filter':     None,
    'sheets_filter':    u'/^Журнал НК$/',
#   'sheet_test':       [0, 0, u''],
    'table':    {
        'row_start':        4,
        'check_column':     'I',
        'row_object':       Register_entry,
        'cols_names': [
            'y',
            'joint',
            'welders',
            'method',
            'd_w_th',
            'conditon',
            'tools',
            'defects',
            'report_w_date',
            'decision',
        ],
        'cols_funcs': {
            'y':        'proceed_int',
            'joint':    'proceed_joint',
            'd_w_th':   'proceed_d_w_th',
            'report_w_date': 'proceed_report_w_date',
        }
    },
}


presets = {
    u'{}/Заключения'.format(homepath):
    {
        'enabled':      0,
        'taskname':     u'Заключения',
        'config':       reports_config,
    },

    u'{}/Журналы контроля'.format(homepath):
    {
        'enabled':      1,
        'taskname':     u'Журналы контроля',
        'config':       registers_config,
    },
}


def add_preset():
    return


def has_preset(preset):
    return preset in presets


def get_preset(preset):
    preset_dict = presets.get(preset, {})
    return (
             preset_dict.get('enabled'),
             preset_dict.get('taskname'),
             preset_dict.get('config', {})
           )


def get_presets():
    for preset in presets.keys():
        l = [preset]
        l.extend(get_preset(preset))
        yield l


version_info = (0, 1, __revision__)
__version__  = '.'.join(map(str, version_info))
version      = __version__
