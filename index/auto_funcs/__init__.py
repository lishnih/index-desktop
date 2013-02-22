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
            logging.warning(u"Функция '{}' уже загружена!".format(i))


def empty_func(*args, **kargs):
    logging.warning(u"Вызвана заглушка!")


def get(func_name):
    global functions

    if func_name not in functions:
        logging.warning(u"Функция не найдена: {}, используем заглушку!".format(func_name))

    func = functions.get(func_name, empty_func)
    return func


def call(func_name, *args, **kargs):
    func = get(func_name)
    error_callback = kargs.pop('error_callback', None)

    try:
        res = func(*args, **kargs)
    except Exception, e:
        if error_callback:
            error_callback(func_name, Exception, e, *args, **kargs)
        else:
            msg = u"""(((((((
Функция '{}' вызвала ошибку:
{} ({!r})!
Были переданый следующие параметры:
args: {!r}
kargs: {!r}
)))))))\n""".format(func_name, e, Exception, args, kargs)
            logging.exception(msg)
        res = None

    return res
