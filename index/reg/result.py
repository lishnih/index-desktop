#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import logging, traceback


def reg_ok(OBJ, msg=''):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setOk(msg)
    else:
        logging.warning(msg)


def reg_warning(OBJ, msg=''):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setWarning(msg)
    else:
        logging.warning(msg)


def reg_error(OBJ, msg='', *args, **kargs):
    msg = u"""(((((((
Ошибка '{}'!
Были переданый следующие параметры:
args: {!r}
kargs: {!r}
)))))))\n""".format(msg, args, kargs)

    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setError(msg)
    else:
        logging.error(msg)


def reg_exception(OBJ, e, *args, **kargs):
    tb_msg = traceback.format_exc()

    msg = u"""(((((((
Ошибка '{}'!
Были переданый следующие параметры:
args: {!r}
kargs: {!r}
===\n""".format(e, args, kargs)
    try:    msg += tb_msg
    except: msg += repr(tb_msg)
    msg += u")))))))\n"

    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setError(msg)
    else:
        logging.exception(msg)


def set_bold(OBJ):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.set_bold()


def set_italic(OBJ):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.set_italic()
