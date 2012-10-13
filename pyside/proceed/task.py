#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10, 2012-09-28

import logging

from reg import set_root
from models import DBSession, Task


def proceed_task(source, name='', tree_widget=None):
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
    set_root(TASK, tree_widget)

    return TASK
