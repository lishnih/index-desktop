#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import Task
from lib.items import DirItem


def reg_task(source, name='', tree_widget=None):
    TASK = Task(
        name   = name,
        source = source,
    )

    rows = DBSession.query(Task).filter_by(name=TASK.name, source=TASK.source).all()
    for task in rows:
        # Сначала удаляем резервные копии:
        res_name = u"{}_res".format(task.name)
        res_rows = DBSession.query(Task).filter_by(name=res_name, source=task.source).all()
        for res_task in res_rows:
            DBSession.delete(res_task)

        # Архивируем существующее задание
        task.name = u"{}_res".format(task.name)

    DBSession.add(TASK)

    # Графика
    if tree_widget:
        TASK.tree_item = DirItem(tree_widget, name, summary=TASK)
        TASK.tree_item.setExpanded(True)

    return TASK
