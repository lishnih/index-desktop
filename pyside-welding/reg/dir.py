#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import Dir
from lib.items import DirItem


def reg_dir(dirname, TASK=None):
    DIR = Dir(
        name   = dirname,
        nfiles = 0,
        volume = 0,
        task   = TASK
    )

    DBSession.add(DIR)

    # Графика
    if hasattr(TASK, 'tree_item'):
        DIR.tree_item = DirItem(TASK.tree_item, dirname, summary=DIR)

    return DIR
