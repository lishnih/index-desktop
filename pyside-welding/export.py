#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

import sys, os

from sql.session import DBSession
from reg.task import reg_task
from reg.dir  import reg_dir
from proceed.file import proceed_file

from proceed.auto_funcs import proceed_date


def Proceed(filename, taskname='default', options={}, tree_widget=None):
    filename = os.path.abspath(filename)

    # Регистрируем
    TASK = reg_task(filename, taskname, tree_widget)

    # Options
#   if options:
#       OPTIONS = reg_options(options, TASK)

    if os.path.isdir(filename):
        print u"Обработка директории '{}'".format(filename)

        # Dir
        for root, dirs, files in os.walk(filename):
            DIR = reg_dir(root, TASK)

            for filename in files:

                # File
                filename = os.path.join(root, filename)
                proceed_file(filename, options, DIR)

    elif os.path.isfile(filename):
        print u"Обработка файла '{}'".format(filename)

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, TASK)
 
        # File
        proceed_file(filename, options, DIR)

    else:
        print u"Не найден файл/директория '{}'!".format(filename)

    DBSession.commit()



def main():
    tasks_list = []


    tasks_list.append(
        (
            u'../2_ALL_Log of welding3.xls',
            u'Сварочный журнал',
            {
                'sheets_seq':   '/^[A-Z]{2,3}$/',
                'row_start':    5,
                'col_check':    'B',
                'cols_names':
                    [
                        'y',                  # A
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
                'cols_funcs':
                    {
                        'date':     proceed_date
                    }
            }
        )
    )


    for task_tuple in tasks_list:
        Proceed(*task_tuple)


if __name__ == '__main__':
    sys.exit(main())
