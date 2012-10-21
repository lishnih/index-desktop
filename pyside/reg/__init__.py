#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import logging

from models import DBSession
from lib.items import DirItem, FileItem
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

    # Графика
    if style != None:
        show_object(OBJECT, PARENT, style=style, brief=brief, summary=summary)

        for key, val in object_debug.items():
            key = u"_debug_{}".format(key)
            setattr(OBJECT, key, val)

    DBSession.add(OBJECT)

    return OBJECT


def reg_object1(Object, object_dict, PARENT=None, style='', brief=None, summary=None):
    object_find = {}
    for i in object_dict:
        if i[0] != '_' and i in dir(Object):
            object_find[i] = object_dict[i]

    try:
        rows = DBSession.query(Object).filter_by(**object_find).all()
#         cond = [getattr(Object, i) == object_find[i] for i in object_find]
#         rows = DBSession.query(Object).filter(*cond).all()
        if rows:
            OBJECT = rows[0]
            l = len(rows)
            if l > 1:
#                 cond_output = [unicode(i) for i in cond]
                reg_error(PARENT, u"Найдено несколько одинаковых записей ({})!".format(l), Object, object_find)
            return OBJECT
    except Exception, e:
        reg_exception(PARENT, Exception, e, Object, object_find)

    OBJECT = reg_object(Object, object_dict, PARENT=PARENT, style=style, brief=brief, summary=summary)

    return OBJECT


def set_object(OBJECT, PARENT, style='', brief=None, summary=None):
    if isinstance(OBJECT, dict):
        OBJECT = aObject(**OBJECT)
    show_object(OBJECT, PARENT, style=style, brief=brief, summary=summary)

    return OBJECT


def set_object1(OBJECT, PARENT, style='', brief=None, summary=None):
    if isinstance(OBJECT, dict):
        OBJECT = aObject(**OBJECT)
    count = PARENT.tree_item.childCount()

    tree_item = None
    for i in range(count):
        child = PARENT.tree_item.child(i)
        name = child.text(0)
        if name == OBJECT.name:
            tree_item = child
            break

    if tree_item:
        OBJECT.tree_item = tree_item
    else:
        show_object(OBJECT, PARENT, style=style, brief=brief, summary=summary)

    return OBJECT


def show_object(OBJECT, PARENT, style='', brief=None, summary=None):
    if PARENT and hasattr(PARENT, 'tree_item'):
        if summary is None:
            summary = OBJECT
        if not hasattr(OBJECT, 'name'):
            setattr(OBJECT, 'name', 'noname')
        name = unicode(OBJECT.name)
        OBJECT.tree_item = FileItem(PARENT.tree_item, name, brief=brief, summary=summary)

        if style:
            OBJECT.tree_item.set_style(style)


def set_root(OBJECT, tree_widget, style='', brief=None, summary=None):
    if isinstance(OBJECT, dict):
        OBJECT = aObject(**OBJECT)
    show_root(OBJECT, tree_widget, style=style, brief=brief, summary=summary)

    return OBJECT


def show_root(OBJECT, tree_widget, style='', brief=None, summary=None):
    if tree_widget:
        if summary is None:
            summary = OBJECT
        if not hasattr(OBJECT, 'name'):
            setattr(OBJECT, 'name', 'noname')
        name = unicode(OBJECT.name)
        OBJECT.tree_item = DirItem(tree_widget, name, brief=brief, summary=summary)
        OBJECT.tree_item.setExpanded(True)

        if style:
            OBJECT.tree_item.set_style(style)


class aObject():
    def __init__(self, **kargs):
        for key, val in kargs.items():
            setattr(self, key, val)
