#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

import sys, os, logging
from sqlalchemy import MetaData, distinct

from models import DBSession
from lib.items import DirItem, FileItem


def view_db(tree_widget):
    if DBSession.bind:
        metadata = MetaData(DBSession.bind, reflect=True)

        for table in metadata.tables:
            tdata = metadata.tables.get(table)
            table_item = DirItem(tree_widget, table, summary=tdata)
            
            for column in tdata.c:
                if column.primary_key:
                    column_item = DirItem(table_item, column.name, summary=column)
                else:
                    column_item = FileItem(table_item, column.name, summary=column)
                    column_item.setBrief(get_distinct(column))

            table_item.setExpanded(True)


def get_distinct(column):
    query = DBSession.query(distinct(column))

    rows = query.all()
    rows_count = query.count()

    td_list = [unicode(row[0]) for row in rows]

    return u"\n".join(td_list)
