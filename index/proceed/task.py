#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10, 2012-09-28

import logging

from reg import set_object
from models import DBSession, Task, Source, Option
from reg.result import reg_exception


def proceed_task(taskname, filename, options, tree_widget=None):
    TASK = Task(
        name = taskname,
    )
    DBSession.add(TASK)

    SOURCE = Source(
        _task = TASK,
        name = filename,
    )
    DBSession.add(SOURCE)

    for key, value in options.items():
        OPTION = Option(
            _source = SOURCE,
            name = key,
            value = value,
        )
        DBSession.add(OPTION)

    # Графика
    TASK = set_object(TASK, tree_widget)
    SOURCE = set_object(SOURCE, TASK)

    return SOURCE
