#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-22


# Rev.20130308


################################
### Входной контроль         ###
################################

vt_register = {
    'description':      u"Для обработки журналов входного контроля",
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'/^Журнал ВК.*$/',
#   'sheet_test':       [0, 0, u''],

    'table': {
        'row_start':        5,
        'check_column':     'C',
        'row_objects':      'Piece_entry',
        'row_objects1':     ('Doc', 'Piece'),
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
            'piece_name':       'prepare_piece',
        }
    },
}


packlist_21 = {
    'description':      u"Для обработки директории 'Входной контроль (21) КУ'",
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'/^\d{3}.*$/',
#   'sheet_test':       [0, 0, u''],

    'table':    {
        'row_start':        3,
        'check_column':     'D',
        'row_objects':      'Piece_entry',
        'row_objects1':     'Piece',
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
            'piece_name':       'prepare_piece',
        }
    },
}


ss_report = {
    'description':      u"Для обработки файла 'Consolidated Report Steel Structure.xls'",
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'Сводная таблица',
#   'sheet_test':       [0, 0, u''],

    'table':    {
        'row_start':        6,
        'check_column':     'D',
        'row_objects':      'Piece_entry',
        'row_objects1':     ('Doc', 'Piece'),
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
            'piece_name':       'prepare_piece',
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

welding = {
    'description':      u"Для обработки журналов сварки",
#   'dirs_filter':      u'',
#   'dirs_level':       0,
    'files_filter':     u'/^.+\.xlsx?$/',
    'sheets_filter':    u'Сварка',
#   'sheet_test':       [0, 0, u''],

    'table':    {
        'row_start':        3,
        'check_column':     'C',
        'row_objects':      'Joint_entry',
        'row_objects1':     'Joint',
        'col_names': [
            '',
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

ndt_register = {
    'description':      u"Для обработки журналов НК",
#   'dirs_filter':      None,
#   'dirs_level':       0,
#   'files_filter':     None,
    'sheets_filter':    u'/^Журнал НК$/',
#   'sheet_test':       [0, 0, u''],

    'table':    {
        'row_start':        4,
        'check_column':     'I',
        'row_objects':      'Joint_entry',
        'row_objects1':     ('Doc', 'Joint'),
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


ndt_reports = {
    'description':      u"Для обработки заключений НК",
#   'dirs_filter':      None,
#   'dirs_level':       0,
#   'files_filter':     None,
#   'sheets_filter':    None,
    'sheet_test':       [0, 0, u'{def: pgu235/(.+); rev: \w+}'],

    u'СП_Астрахань_ОКК_Акт-ВИК-МК_001': {
        'doc':    {
            'doc_values': {
                'doc_pre':        ( 9,  9),
                'doc_seq':        ( 9, 11),
            },
            'doc_funcs': {},
            'doc_objects':        'Doc',
#           'doc_objects1':       'Doc',

        },
#         'table':    {
#             'row_start':        4,
#             'check_column':     'I',
#             'row_objects':      'Joint_entry',
#             'row_objects1':     ('Doc', 'Joint'),
#             'col_names': [
#                 'y',
#                 'joint',
#                 'welders',
#                 'method',
#                 'd_w_th',
#                 'conditon',
#                 'tools',
#                 'defects',
#                 'report_w_date',
#                 'decision',
#             ],
#             'col_funcs': {
#                 'y':                'proceed_int',
#                 'joint':            'proceed_joint',
#                 'd_w_th':           'proceed_d_w_th',
#                 'report_w_date':    'proceed_report_w_date',
#             }
#         },
    }
}


def main():
    for key, value in globals().items():
        if isinstance(value, dict):
            print(key)


if __name__ == '__main__':
    main()
