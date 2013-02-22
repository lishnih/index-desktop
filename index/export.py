#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

import sys, os, logging

from models         import DBSession, Base
from models.db      import initdb
from models.links   import initlinks
from proceed.task   import proceed_task
from proceed.dir    import proceed_dir
from proceed.file   import proceed_file
from reg.result     import reg_exception

from presets        import has_preset, get_preset, get_presets, tracing
from lib.data_funcs import filter_match, filter_list


def Proceed(source, taskname=None, options=None, tree_widget=None):
    engine = initdb(DBSession, Base)
    if not engine:
        return
    initlinks(engine, Base)

    filename = os.path.abspath(source)
    filename = filename.replace('\\', '/')    # приводим к стилю Qt

    if has_preset(source):
        enabled, taskname1, options1 = get_preset(source)
        taskname = taskname or taskname1
        options  = options  or options1

    if options == None:
        logging.warning(u"Настройки для '{}' не заданы!".format(source))
        options = {}

    # Регистрируем
    TASK = proceed_task(filename, taskname, tree_widget)

    if os.path.isdir(filename):
        logging.info(u"Обработка директории '{}'".format(filename))

        dirs_filter = options.get('dirs_filter')
        files_filter = options.get('files_filter')

        # Dir
        for root, dirs, files in os.walk(filename):
            tracing.append(root)
            DIR = proceed_dir(root, options, TASK)
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
        DIR = proceed_dir(dirname, options, TASK)
 
        # File
        proceed_file(filename, options, DIR)

    else:
        logging.warning(u"Не найден файл/директория '{}'!".format(filename))

    try:
        DBSession.commit()
    except Exception, e:    # StatementError
        reg_exception(TASK, Exception, e)


def main():
    for source, enabled, taskname, options in get_presets():
        if enabled:
            Proceed(source, taskname, options)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
