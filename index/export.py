#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

import sys, os, logging

from models             import DBSession, Base
from models.db          import initDb
from proceed.task       import proceed_task
from proceed.dir        import proceed_dir
from proceed.file       import proceed_file
from reg                import set_object
from reg.result         import reg_exception

from lib.settings       import Settings
from lib.data_funcs     import get_list, filter_match, filter_list
from lib.options_funcs  import get_options
from lib.items          import DirItem
from lib.dump           import plain


tracing = []


def ProceedInit(sources, settings=None, args=None, tree_widget=None):
    datadir  = settings.get("datadir", '.')
    taskname = args.get("task", "default")
    method   = args.get("method", "default")

    # Получаем настройки метода
    options = get_options(datadir, method)
    if not options:
        print u"Настройки задачи не найдены!"
        print "settings:", settings
        print "datadir: ", datadir
        print
        print "args:    ", plain(args)
        print "method:  ", method

    dbpath = options.get('dbpath', datadir)
    dbname = options.get('dbname', "index.sqlite")
    db_path = os.path.join(dbpath, dbname)
    db_uri_default = u'sqlite:///{0}'.format(db_path)
    db_uri = options.get('db_uri', db_uri_default)
    try:
        initDb(db_uri, DBSession, Base)
    except Exception as e:
        root_dict = dict(name="Root")
        tree_item = set_object(root_dict, tree_widget, brief=[sources, datadir])
        reg_exception(tree_item, e)
        return

    sources = get_list(sources)
    for source in sources:
        Proceed(source, taskname, options, tree_widget)


def Proceed(source, taskname=None, options=None, tree_widget=None):
    filename = os.path.abspath(source)
    filename = filename.replace('\\', '/')    # приводим к стилю Qt

    # Регистрируем задание
    SOURCE = proceed_task(taskname, filename, options, tree_widget)

    if os.path.isdir(filename):
        logging.info(u"Обработка директории '{0}'".format(filename))

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
        logging.info(u"Обработка файла '{0}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = proceed_dir(dirname, options, SOURCE)

        # File
        proceed_file(filename, options, DIR)

    else:
        logging.warning(u"Не найден файл/директория '{0}'!".format(filename))

    try:
        DBSession.commit()
    except Exception as e:    # StatementError
        reg_exception(SOURCE, e)


def main(args=None):
    if args.files:
        s = Settings()
        s.saveEnv()

        args = dict(args._get_kwargs())
        ProceedInit(args['files'], self.s, args)
    else:
        logging.warning(u"Файлы не заданы!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    import argparse
    from lib.argparse_funcs import readable_file_or_dir_list

    parser = argparse.ArgumentParser(description='Indexing files and directories.')
    parser.add_argument('files', action=readable_file_or_dir_list, nargs='*',
                        help='files and directories to proceed')
    parser.add_argument('-t', '--task',
                        help='specify the task name')
    parser.add_argument('-m', '--method',
                        help='specify the method name')

    if sys.version_info >= (3,):
        argv = sys.argv
    else:
        fse = sys.getfilesystemencoding()
        argv = [i.decode(fse) for i in sys.argv]

    args = parser.parse_args(argv[1:])

    sys.exit(main(args))
