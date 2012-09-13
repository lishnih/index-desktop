#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import logging

from models import DBSession
from lib.items import FileItem

from lib.dump_funcs import plain_r

def reg_object(Object, object_dict, PARENT=None, parent_attr=None, show=True, brief=None, summary=None):
    object_reg = {}
    object_debug = {}
    for i in object_dict:
        if i in dir(Object):
            object_reg[i] = object_dict[i]
        else:
            object_debug[i] = object_dict[i]
    OBJECT = Object(**object_reg)

#   if PARENT and parent_attr:
#       setattr(OBJECT, parent_attr, PARENT)

    # Графика
    if PARENT:
        if show and hasattr(PARENT, 'tree_item'):
            OBJECT = set_object(PARENT, OBJECT, brief=brief, summary=summary)

            for key, val in object_debug.items():
                key = "_debug_{}".format(key)
                setattr(OBJECT, key, val)

    DBSession.add(OBJECT)

    return OBJECT


def reg_object1(Object, object_dict, PARENT=None, show=True, brief=None, summary=None):
    object_find = {}
    for i in object_dict:
        if i in dir(Object):
            object_find[i] = object_dict[i]

    try:
        rows = DBSession.query(Object).filter_by(**object_find).all()
        if rows:
            return rows[0]          # !!!
    except:
        logging.error(unicode(DBSession.query(Object).filter_by(**object_find)))
        logging.error(unicode(object_find))

    OBJECT = reg_object(Object, object_dict, PARENT=PARENT, show=show, brief=brief, summary=summary)

    return OBJECT


def set_object(PARENT, OBJECT=None, brief=None, summary=None, **kargs):
    if OBJECT is None:
        OBJECT = emptyClass()

    for key, val in kargs.items():
        setattr(OBJECT, key, val)

    if hasattr(PARENT, 'tree_item'):
        if summary is None:
            summary = OBJECT
        if not hasattr(OBJECT, 'name'):
            setattr(OBJECT, 'name', 'noname')
        name = unicode(OBJECT.name)
        OBJECT.tree_item = FileItem(PARENT.tree_item, name, brief=brief, summary=summary)

    return OBJECT


def set_info(OBJECT, brief=None, summary=None):
#     if hasattr(OBJECT, '__parent__'):
#         PARENT = OBJECT.__parent__
# 
    if hasattr(OBJECT, 'tree_item'):
        if brief:
            OBJECT.tree_item.setBrief(brief)
        if summary:
            OBJECT.tree_item.setSummary(summary)


class emptyClass(object):
    pass
