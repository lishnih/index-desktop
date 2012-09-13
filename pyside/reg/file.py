#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from models import DBSession, File
from lib.items import FileItem


def reg_file(filename, DIR=None):
    FILE = File(
        name = filename,
        dir  = DIR
    )

    if DIR:
        if DIR.nfiles is None:
            DIR.nfiles = 0
        if DIR.volume is None:
            DIR.volume = 0

        if FILE.size is not None:
            DIR.nfiles += 1
            DIR.volume += FILE.size

    DBSession.add(FILE)

    # Графика
    if hasattr(DIR, 'tree_item'):
        FILE.tree_item = FileItem(DIR.tree_item, FILE.name, summary=FILE)

    return FILE
