#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

import sys, os, logging

from models       import DBSession
from models.db    import initdb
from reg.task     import reg_task
from reg.dir      import reg_dir
from reg.result   import reg_error
from proceed.file import proceed_file

from presets        import has_preset, get_preset, get_presets, tracing
from lib.data_funcs import filter_match, filter_list


def Proceed(source, taskname=None, options={}, tree_widget=None):
    engine = initdb()
    if not engine:
        return

    filename = os.path.abspath(source)
    filename = filename.replace('\\', '/')    # приводим к стилю Qt

    # Регистрируем
    TASK = reg_task(filename, taskname, tree_widget)

    # Options
    if options:
#       OPTIONS = reg_options(options, TASK)
        pass
    else:
        logging.warning(u"Настройки не заданы для '{}', используем по умолчанию!".format(source))

        if has_preset(source):
            enabled, taskname, options = get_preset(source)
        else:
            logging.warning(u"Настройки по умолчанию также не заданы!")

    if os.path.isdir(filename):
        logging.info(u"Обработка директории '{}'".format(filename))

        dirs_filter = options.get('dirs_filter')
        files_filter = options.get('files_filter')

        # Dir
        for root, dirs, files in os.walk(filename):
            DIR = reg_dir(root, TASK)
            tracing.append(root)

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
    for source, enabled, taskname, options in get_presets():
        if enabled:
            Proceed(source, taskname, options)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
