#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-28


__revision__ = 20121029


import os

from models import Doc                  # Общее для всех (документ)
from models import Piece, Piece_entry   # Входной контроль
from models import Joint, Joint_entry   # Сварка, НК


if os.name == 'posix':
    homepath = u'/home/stan/pgu235'
elif os.name == 'nt':
    homepath = u'D:/opt/home/pgu235'


tracing = []


################################
### Входной контроль         ###
################################

vt_register_config = {
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'/^Журнал ВК.*$/',
#   'sheet_test':       [0, 0, u''],
    'table': {
        'row_start':        5,
        'check_column':     'C',
        'row_objects':      Piece_entry,
        'row_objects1':     (Doc, Piece),
        'col_names': [
            'y',                # A
            'date',
            '',
            '',
            'mfr',
            'invoice',
            '',
            'order',            # H
            '',
            '',
            'doc_pre',          # K
            'doc_seq',
            '',
            'piece_type',       # N
            'piece_name',
            'qnt',
            'meas',
            '',
            'cert_type',        # S
            'cert',
        ],
        'col_funcs': {
            'date':             'proceed_date',
            'doc_pre':          'proceed_int_str',
            'doc_seq':          ('proceed_int_str', 'prepare_doc_vt_act'),
            'piece_name':       'proceed_piece',
        }
    },
}


packlist_21_config = {
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'/^\d{3}.*$/',
#   'sheet_test':       [0, 0, u''],
    'table':    {
        'row_start':        3,
        'check_column':     'D',
        'row_objects':      Piece_entry,
        'row_objects1':     Piece,
        'col_names': [
            '',
            '',
            'y',
            'piece_name',
            'piece_scheme',
            'qnt',
            'meas',
        ],
        'col_funcs': {
            'y':                'proceed_int',
            'piece_name':       'proceed_piece',
        }
    },
}


ss_report_config = {
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'Сводная таблица',
#   'sheet_test':       [0, 0, u''],
    'table':    {
        'row_start':        6,
        'check_column':     'D',
        'row_objects':      Piece_entry,
        'row_objects1':     (Doc, Piece),
        'col_names': [
            'y',                # A
            '',
            'piece_name',
            'piece_type',
            'meas',
            'qnt',
            '',
            '',
            '',
            'invoice',
            'object',
            'date',
            'cert',
        ],
        'col_funcs': {
            'y':                'proceed_int',
            'piece_name':       'proceed_piece',
            'qnt':              'proceed_float',
            'invoice':          ('proceed_int_str', 'prepare_doc_invoice'),
            'date':             'proceed_date',
            'cert':             'proceed_int_str',
        },
    },
}


################################
### Сварка                   ###
################################

welding_config = {
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'Сварка',
#   'sheet_test':       [0, 0, u''],
    'table':    {
        'row_start':        3,
        'check_column':     'C',
        'row_objects':      Joint_entry,
        'row_objects1':     Joint,
        'col_names': [
            'date',
            '',
            'joint',
            '',
            '',
            '',
            '',
            'welder',
            '',
            '',
            'decision',
            '',
            '',
            '',
            'piece',
            'd',
            'th',
            'steel',
        ],
        'col_funcs': {
            'date':             'proceed_date',
            'joint':            'proceed_joint',
            'd':                'proceed_float',
            'th':               'proceed_float',
        },
    },
}


################################
### Неразрушающий контроль   ###
################################

ndt_register_config = {
#   'dirs_filter':      None,
#   'dirs_level':       0,
#   'files_filter':     None,
    'sheets_filter':    u'/^Журнал НК$/',
#   'sheet_test':       [0, 0, u''],
    'table':    {
        'row_start':        4,
        'check_column':     'I',
        'row_objects':      Joint_entry,
        'row_objects1':     (Doc, Joint),
        'col_names': [
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
        'col_funcs': {
            'y':                'proceed_int',
            'joint':            'proceed_joint',
            'd_w_th':           'proceed_d_w_th',
            'report_w_date':    'proceed_report_w_date',
        }
    },
}


presets = {
    u'{}/Входной контроль/cache'.format(homepath):
    {
        'enabled':      1,
        'taskname':     u'Журналы ВК',
        'config':       vt_register_config,
    },

    u'{}/photo/Входной контроль (21) КУ'.format(homepath):
    {
        'enabled':      1,
        'taskname':     u'Журналы ВК',
        'config':       packlist_21_config,
    },

    u'{}/Входной контроль/cache/Consolidated Report Steel Structure.xls'.format(homepath):
    {
        'enabled':      1,
        'taskname':     u'Накладные МК',
        'config':       ss_report_config,
    },

    u'{}/Сводная таблица/Сварочные журналы'.format(homepath):
    {
        'enabled':      1,
        'taskname':     u'Накладные МК',
        'config':       welding_config,
    },

    u'{}/Сводная таблица/Журналы контроля'.format(homepath):
    {
        'enabled':      1,
        'taskname':     u'Журналы контроля',
        'config':       ndt_register_config,
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


version_info = (0, 3, __revision__)
__version__  = '.'.join(map(str, version_info))
version      = __version__
