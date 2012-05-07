#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

import sys, os, logging

from models import DBSession
from models.db import initdb
from reg.task   import reg_task
from reg.dir    import reg_dir
from reg.result import reg_error
from proceed.file import proceed_file

from export_default import get_sources, get_taskname, get_default
from lib.data_funcs import filter_match, filter_list


def Proceed(source, taskname=get_taskname(), options=get_default(), tree_widget=None):
    initdb()

    filename = os.path.abspath(source)
    filename = filename.replace('\\', '/')    # приводим к стилю PySide

    # Регистрируем
    TASK = reg_task(filename, taskname, tree_widget)

    # Options
#   if options:
#       OPTIONS = reg_options(options, TASK)

    if os.path.isdir(filename):
        logging.info(u"Обработка директории '{}'".format(filename))

        dirs_filter = options.get('dirs_filter')
        files_filter = options.get('files_filter')

        # Dir
        for root, dirs, files in os.walk(filename):
            DIR = reg_dir(root, TASK)

            for dirname in dirs:
                if filter_match(dirname, dirs_filter):
                    DIR.ndirs += 1
                else:
                    dirs.remove(dirname)

            files_filtered = filter_list(files, files_filter)

            for filename in files_filtered:

                # File
                filename = os.path.join(root, filename)
                proceed_file(filename, options, DIR)

    elif os.path.isfile(filename):
        logging.info(u"Обработка файла '{}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, TASK)
 
        # File
        proceed_file(filename, options, DIR)

    else:
        logging.warning(u"Не найден файл/директория '{}'!".format(filename))

    try:
        DBSession.commit()
    except Exception, e:    # StatementError
        reg_error(TASK, e)


def main():
    for source, taskname, options in get_sources():
        Proceed(source, taskname, options)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
