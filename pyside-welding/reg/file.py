#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import File


def reg_file(filename, dir=None):
    tip = dir.tree_item if hasattr(dir, 'tree_item') else None
    file = File(
        name = filename,
        tip  = tip,
    )

    if dir:
        dir.file.append(file)
        dir.files  += 1
        dir.volume += file.size if file.size else 0

    DBSession.add(file)

    return file
