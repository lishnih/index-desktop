#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, re, pickle, logging
from PySide import QtCore

try:
    from .lib.backwardcompat import *
    from .lib.settings import Settings
    from .lib.tkprop import propertyDialog
except:
    from lib.backwardcompat import *
    from lib.settings import Settings
    from lib.tkprop import propertyDialog

from presets import *


def save_entry(filename, entry):
    with open(filename, 'wb') as f:
        pickle.dump(entry, f)


def main():
    logging.basicConfig(level=logging.INFO)

    s = Settings()
    for i in [
        'home',
        'instance',
        'location',
        'app',
        'name',
        'path',
        'filename',
    ]:
        print("{0:20}: {1}".format(i, getattr(s, i)))

    print()

    appdata = s.get("app")
    if not appdata:
        logging.warning(u"Запустите скрипт index, чтобы инициализировать директорию с данными")
        return

    if not os.path.exists(appdata):
        logging.info(u"Creating directory: {}".format(appdata))
        os.makedirs(appdata)

    logging.info(u"Export to '{}'".format(appdata))

    for key, value in globals().items():
        if isinstance(value, dict):
            description = value.get('description', '')
            logging.info(u"{:20}: {}".format(key, description))
            filename = os.path.join(appdata, "{}.pickle".format(key))
            save_entry(filename, value)


if __name__ == '__main__':
    main()
