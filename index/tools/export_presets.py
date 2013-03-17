#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-22

import os, re, pickle, logging
from PySide import QtCore

from presets import *


# Настройки: [HKCU\Software\lishnih@gmail.com\<app_section>]
company_section = "lishnih@gmail.com"
app_section = re.sub(r'\W', '_', os.path.dirname(os.path.dirname(__file__)))


def save_entry(filename, entry):
    with open(filename, 'wb') as f:
        pickle.dump(entry, f)


def main():
    logging.basicConfig(level=logging.INFO)

    settings = QtCore.QSettings(company_section, app_section)
    logging.info(u"Settings: '{}' / '{}'".format(company_section, app_section))

    appdata = settings.value("appdata")
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
