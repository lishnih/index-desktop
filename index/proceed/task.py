#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10, 2012-09-28

import logging

from reg import set_root
from models import DBSession, Task
from reg.result import reg_exception


def proceed_task(source, name='', tree_widget=None):
    TASK = Task(
        name   = name,
        source = source
    )

    # Графика
    set_root(TASK, tree_widget)

    try:
        rows = DBSession.query(Task).filter_by(name=name, source=source).all()
        for task in rows:
            DBSession.delete(task)
    except Exception, e:
        reg_exception(TASK, Exception, e, name, source)

    DBSession.add(TASK)

    return TASK
