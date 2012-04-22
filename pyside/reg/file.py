#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import File
from lib.items import FileItem


def reg_file(filename, DIR=None):
    FILE = File(
        name = filename,
        dir  = DIR
    )

    if DIR:
        DIR.nfiles += 1
        if FILE.size:
            DIR.volume += FILE.size

    DBSession.add(FILE)

    # Графика
    if hasattr(DIR, 'tree_item'):
        FILE.tree_item = FileItem(DIR.tree_item, FILE.name, summary=FILE)

    return FILE
