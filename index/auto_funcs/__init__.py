#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-29

import logging

import xls_funcs


functions = dict()

for i in dir(xls_funcs):
    obj = getattr(xls_funcs, i)
    if callable(obj):
        if i not in functions:
            functions[i] = obj
        else:
            logging.warning(u"Функция '{0}' уже загружена!".format(i))


def empty_func(*args, **kargs):
    msg = u"""(((((((
Вызвана заглушка с параметрами:
args:  {0!r}
kargs: {1!r}
)))))))\n""".format(args, kargs)
    logging.warning(msg)


def default_error_callback(func_name, e, *args, **kargs):
    msg = u"""(((((((
Функция '{0}' вызвала ошибку:
{1}!
Были переданый следующие параметры:
args: {2!r}
kargs: {3!r}
)))))))\n""".format(func_name, e, args, kargs)
    logging.error(msg)


def get(func_name):
    if func_name not in functions:
        logging.warning(u"Функция не найдена: {0}, используем заглушку!".format(func_name))
        functions[func_name] = empty_func

    func = functions.get(func_name)
    return func


def call(func_name, *args, **kargs):
    func = get(func_name)
    error_callback = kargs.pop('error_callback', default_error_callback)

    try:
        res = func(*args, **kargs)
    except Exception as e:
        if error_callback:
            error_callback(func_name, e, *args, **kargs)
        res = None

    return res
