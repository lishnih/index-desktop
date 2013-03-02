#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10, 2012-09-28

import pickle, logging

from reg import reg_object1, set_object
from models import DBSession, Task, Source, Option
from reg.result import reg_exception


def proceed_task(taskname, filename, options, tree_widget=None):
    task_dict = dict(name=taskname)
    TASK = reg_object1(Task, task_dict, tree_widget)

    source_dict = dict(_task=TASK, name=filename)
    SOURCE = reg_object1(Source, source_dict, TASK, brief=options)

    for key, value in options.items():
        if value is None or isinstance(value, (int, float, long, basestring, bytearray)):
            pass
        elif isinstance(value, (list, tuple)):
            value = pickle.dumps(value)
        elif isinstance(value, dict):
            value = pickle.dumps(value)
        else:
            logging.warning(u"Неподдерживаемый тип данных: {!r}{!r}".format(type(value), value))
        OPTION = Option(
            _source = SOURCE,
            name = key,
            value = value,
        )
        DBSession.add(OPTION)

    return SOURCE
