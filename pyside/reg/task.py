#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import logging

from models import DBSession, Task
from lib.items import DirItem


def reg_task(source, name='', tree_widget=None):
    TASK = Task(
        name   = name,
        source = source
    )

    try:
        rows = DBSession.query(Task).filter_by(name=name, source=source).all()
        for task in rows:
            DBSession.delete(task)
    except:
        logging.exception(u'Исключение во время поиска существующих заданий')
        logging.error(u'source:      {}'.format(source))
        logging.error(u'name:        {}'.format(name))
        logging.error(u'tree_widget: {}'.format(tree_widget))

    DBSession.add(TASK)

    # Графика
    if tree_widget:
        task_name = TASK.name if TASK.name else u'<без названия>'
        TASK.tree_item = DirItem(tree_widget, task_name, summary=TASK)
        TASK.tree_item.setExpanded(True)

    return TASK
