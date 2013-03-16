#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import logging

import models
from reg.result import reg_warning, reg_error, reg_exception


def reg_object(Object, object_dict, PARENT=None, style='', brief=None):
    if isinstance(Object, basestring):
        try:
            Object = getattr(models, Object)
        except:
#           OBJECT = set_object(object_dict, PARENT, style, brief)
            reg_error(OBJECT, u"Объект не найден: '{}'!".format(Object), Object, object_dict)
            return OBJECT

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


def reg_object1(Object, object_dict, PARENT=None, style='', brief=None):
    if isinstance(Object, basestring):
        try:
            Object = models.__getattribute__(Object)
        except:
#           OBJECT = set_object(object_dict, PARENT, style, brief)
            reg_error(OBJECT, u"Объект не найден: '{}'!".format(Object), Object, object_dict)
            return OBJECT

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
#           show_object(OBJECT, PARENT, style=style, brief=brief)
            return OBJECT
    except Exception as e:
        reg_exception(PARENT, e, Object, object_find)

    OBJECT = reg_object(Object, object_dict, PARENT=PARENT, style=style, brief=brief)

    return OBJECT


class aObject():
    def __init__(self, **kargs):
        for key, val in kargs.items():
            setattr(self, key, val)
