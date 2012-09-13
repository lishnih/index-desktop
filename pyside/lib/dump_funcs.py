# coding=utf-8
# Stan 2007-08-02, 2012-05-08

import logging
from inspect import ismethod
from xml.sax.saxutils import escape, prepare_input_source

""" Отладочный вывод переменных различных типов
plain      возвращает строковое представление объекта
html       html-версия
html_type  возвращает тип объекта для html

plain_l    нумерует каждую строку и возвращает
html_l     html-версия

plain_r    возвращает строковое представление объекта (развёрнуто)
html_r     html-версия
"""


def plain(obj):
    if obj is None:
        buf = u''
    elif isinstance(obj, int) or isinstance(obj, float):
        buf = unicode(obj)
    else:
        try:
            buf = unicode(obj)
        except:
            buf = repr(obj)
            buf = buf.replace(r'\n', '\n')
            buf = buf.replace(r'\r', '')

    return buf


def html_type(obj):
    return escape(plain(type(obj)))


def html_val(obj):
    return escape(plain(obj))


def html(obj):
    if obj is None:
        buf = u'<i>None</i>'
    elif isinstance(obj, basestring):
        type_obj = html_type(obj)
        obj = html_val(obj)
        buf = u'<pre>{}</pre>'.format(obj) if '\n' in obj else \
              u'<span title="{}">{}</span>'.format(type_obj, obj)
    elif isinstance(obj, int) or isinstance(obj, float):
        type_obj = html_type(obj)
        buf = u'<span title="{}">{}</span>'.format(type_obj, obj)
    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, dict):
        type_obj = html_type(obj)
        obj = html_val(obj)
        buf = u'<span title="{}">{}</span>'.format(type_obj, obj)
    else:
        type_obj = html_type(obj)
        obj = html_val(obj)
        buf = u'<span title="{}">{}</span>'.format(type_obj, obj)

    return buf


def plain_l(obj):
    buf = u''

    if isinstance(obj, basestring):
        obj = obj.replace('\r', '')
        obj_list = obj.split('\n')

        line = 1
        for s in obj_list:
            buf += u'{:05}: {}'.format(line, s) if s else \
                   u'{:05}:-'.format(line)
            line += 1
    else:
        logging.warning(u'Переменная должна быть строкой: {!r}'.format(obj))

    return buf


def html_l(obj):
    buf = u''

    if isinstance(obj, basestring):
        obj = obj.replace('\r', '')
        obj_list = obj.split('\n')

        buf = u'<table border="1">\n'
        line = 1
        for s in obj_list:
            if not s:
                s = '<i>пустая строка</i>'
            buf += u'  <tr><td>{:05}</td><td>{}</td></tr>\n'.format(line, s)
            line += 1
        buf += u'</table>\n'
    else:
        logging.warning(u'Переменная должна быть строкой: {!r}'.format(obj))

    return buf


def plain_r(obj):
    buf = u''

    # === ITER ===
    if not isinstance(obj, basestring):
        list_buf = u''
        try:
            for val in obj:
                list_buf += "{}\n".format(plain(val))
        except:
            pass
        if list_buf:
            buf += u'Iter свойства:\n{}\n'.format(list_buf)

    # === DICT ===
    if hasattr(obj, '__dict__'):
        buf += u'Dict свойства:\n'
        d = obj.__dict__
        for key in sorted(d.keys()):
            if key[0:2] != '__':
                val = d.get(key)
                buf += u'{:20}: {}\n'.format(key, plain(val))

    # === DIRS ===
    dirs_buf = u''
    for key in dir(obj):
        val = getattr(obj, key)
        if not ismethod(val):
            if key[0:2] != '__':
                dirs_buf += u'{:20}: {}\n'.format(key, plain(val))

    if dirs_buf:
        buf += u'Dirs свойства:\n{}\n'.format(dirs_buf)

    return buf


def html_r(obj):
    buf = u''

    buf = u'<table border="1">\n'

    # === ITER ===
    if not isinstance(obj, basestring):
        list_buf = u''
        try:
            for val in obj:
                list_buf += u'  <tr><td></td><td>{}</td></tr>\n'.format(html(val))
        except:
            pass
        if list_buf:
            buf += u'  <tr><th colspan="2" style="background-color: yellow">Iter свойства:</th></tr>\n{}'.format(list_buf)

    # === DICT ===
    if hasattr(obj, '__dict__'):
        buf += u'  <tr><th colspan="2" style="background-color: yellow">Dict свойства:</th></tr>\n'
        d = obj.__dict__
        for key in sorted(d.keys()):
            if key[0:2] != '__':
                val = d.get(key)
                buf += u'  <tr><td style="color: blue"><b>{}</b></td><td>{}</td></tr>\n'.format(key, html(val))

    # === DIRS ===
    dirs_buf = u''
    for key in dir(obj):
        val = getattr(obj, key)
        if not ismethod(val):
            if key[0:2] != '__':
                dirs_buf += u'  <tr><td style="color: blue"><b>{}</b></td><td>{}</td></tr>\n'.format(key, html(val))

    if dirs_buf:
        buf += u'  <tr><th colspan="2" style="background-color: yellow">Dirs свойства:</th></tr>\n{}'.format(dirs_buf)

    buf += u'</table>\n'

    return buf
