#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import Sheet
from lib.items import FileItem


def reg_sheet(sh, FILE=None, seq=None):
    SHEET = Sheet(
        sh = sh,
        seq = seq,
        file = FILE
    )

    DBSession.add(SHEET)

    # Графика
    if hasattr(FILE, 'tree_item'):
        SHEET.tree_item = FileItem(FILE.tree_item, SHEET.name, summary=SHEET)

    return SHEET
