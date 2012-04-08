#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sql.session import DBSession
from sql.model import Task


def reg_task(source, name='', tip=None):
    task = Task(
        name   = name,
        source = source,
        tip    = tip,
    )

#     query = DBSession.query(Task).filter_by(name = task.name).count()
#     if query:
#         print u'Обновляем задание...'

    DBSession.add(task)

    return task
