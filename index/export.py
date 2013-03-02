#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12, 2013-02-22

import sys, os, logging

from models             import DBSession, Base
from models.db          import initDb
from proceed.task       import proceed_task
from proceed.dir        import proceed_dir
from proceed.file       import proceed_file
from reg                import set_object
from reg.result         import reg_exception

from lib.data_funcs     import get_list, filter_match, filter_list
from lib.options_funcs  import get_options
from lib.items          import DirItem


tracing = []


def Proceed(sources, args, datadir=None, tree_widget=None):
    taskname = args.task
    method = args.method

    if not datadir:
        datadir = '.'

    # Получаем настройки метода
    options = get_options(datadir, method)

    dbpath = options.get('dbpath', datadir)
    dbname = options.get('dbname', "index.sqlite")
    db_path = os.path.join(dbpath, dbname)
    db_uri_default = u'sqlite:///{}'.format(db_path)
    db_uri = options.get('db_uri', db_uri_default)
    try:
        initDb(db_uri, DBSession, Base)
    except Exception, e:
        root_dict = dict(name="Root")
        tree_item = set_object(root_dict, tree_widget, brief=[sources, datadir])
        reg_exception(tree_item, Exception, e)
        return

    sources = get_list(sources)
    for source in sources:
        Proceed1(source, taskname, options, tree_widget)


def Proceed1(source, taskname=None, options=None, tree_widget=None):
    filename = os.path.abspath(source)
    filename = filename.replace('\\', '/')    # приводим к стилю Qt

    # Регистрируем задание
    SOURCE = proceed_task(taskname, filename, options, tree_widget)

    if os.path.isdir(filename):
        logging.info(u"Обработка директории '{}'".format(filename))

        dirs_filter = options.get('dirs_filter')
        files_filter = options.get('files_filter')

        # Dir
        for root, dirs, files in os.walk(filename):
            tracing.append(root)
            DIR = proceed_dir(root, options, SOURCE)
            DIR.ndirs = 0   # Обнуляем именно при обработке задания-директории

            for dirname in dirs:
                if filter_match(dirname, dirs_filter):
                    DIR.ndirs += 1
                else:
                    dirs.remove(dirname)

            files_filtered = filter_list(files, files_filter)

            for filename in files_filtered:
                tracing.append(filename)

                # File
                filename = os.path.join(root, filename)
                proceed_file(filename, options, DIR)

    elif os.path.isfile(filename):
        logging.info(u"Обработка файла '{}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = proceed_dir(dirname, options, SOURCE)
 
        # File
        proceed_file(filename, options, DIR)

    else:
        logging.warning(u"Не найден файл/директория '{}'!".format(filename))

    try:
        DBSession.commit()
    except Exception, e:    # StatementError
        reg_exception(SOURCE, Exception, e)


def main(args=None):
#     if has_preset(source):
#         enabled, taskname1, options1 = get_preset(source)
#         taskname = taskname or taskname1
#         options  = options  or options1
# 
#     for source, enabled, taskname, options in get_presets():
#         if enabled:
#             Proceed(source, taskname, options)

    if args.files:
        Proceed(args.files, "from console")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    import argparse
    from lib.argparse_funcs import readable_file_or_dir_list

    parser = argparse.ArgumentParser(description='Indexing files and directories.')
    parser.add_argument('files', action=readable_file_or_dir_list, nargs='*',
                        help='files and directories to proceed')

    args = parser.parse_args()

    sys.exit(main(args))
