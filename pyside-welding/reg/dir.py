#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import Dir


def reg_dir(dirname, task=None):
    dir = Dir(
        name   = dirname,
        files  = 0,
        volume = 0,
        tip    = task.tree_item,
    )

    if task:
        task.dir.append(dir)

    DBSession.add(dir)

    return dir
