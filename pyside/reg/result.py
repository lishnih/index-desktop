#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

import logging


def reg_ok(OBJ, msg=''):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setOk(msg)


def reg_warning(OBJ, msg=''):
    logging.warning(msg)
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setWarning(msg)


def reg_error(OBJ, msg=''):
    logging.error(msg)
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setError(msg)


def reg_exception(OBJ, msg=''):
    logging.exception(msg)
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setError(msg)
