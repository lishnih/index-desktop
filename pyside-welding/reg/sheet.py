#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import Sheet


def reg_sheet(sh, file=None, i=-1):
    sheet = Sheet(
        seq = i,
        sh  = sh,
        tip = file.tree_item,
    )

    if file:
        file.sheet.append(sheet)

    DBSession.add(sheet)

    return sheet
