#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from models import DBSession, Dir
from lib.items import DirItem


def reg_dir(dirname, TASK=None):
    DIR = Dir(
        name = dirname,
        task = TASK
    )

    DBSession.add(DIR)

    # Графика
    if hasattr(TASK, 'tree_item'):
        DIR.tree_item = DirItem(TASK.tree_item, DIR.name, summary=DIR)

    return DIR
