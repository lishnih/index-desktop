#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import logging

import models
from reg.result import reg_warning, reg_error, reg_exception


def reg_object(Object, object_dict, PARENT=None, style='', brief=None, summary=None):
    object_reg = {}
    object_debug = {}
    for i in object_dict:
        if i in dir(Object):
            object_reg[i] = object_dict[i]
        else:
            object_debug[i] = object_dict[i]

    OBJECT = Object(**object_reg)

    models.DBSession.add(OBJECT)

    return OBJECT


def reg_object1(Object, object_dict, PARENT=None, style='', brief=None, summary=None):
    object_find = {}
    for i in object_dict:
        if i[0] != '_' and i in dir(Object):
            object_find[i] = object_dict[i]

    try:
        rows = models.DBSession.query(Object).filter_by(**object_find).all()
#       cond = [getattr(Object, i) == object_find[i] for i in object_find]
#       rows = models.DBSession.query(Object).filter(*cond).all()
        if rows:
            OBJECT = rows[0]
            l = len(rows)
            if l > 1:
#               cond_output = [unicode(i) for i in cond]
                reg_error(PARENT, u"Найдено несколько одинаковых записей ({})!".format(l), Object, object_find)
            return OBJECT
    except Exception, e:
        reg_exception(PARENT, Exception, e, Object, object_find)

    OBJECT = reg_object(Object, object_dict, PARENT=PARENT, style=style, brief=brief, summary=summary)

    return OBJECT


class aObject():
    def __init__(self, **kargs):
        for key, val in kargs.items():
            setattr(self, key, val)
