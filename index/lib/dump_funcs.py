# coding=utf-8
# Stan 2007-08-02

import logging
from inspect import ismethod
from xml.sax.saxutils import escape, prepare_input_source

""" Отладочный вывод переменных различных типов
plain_val  возвращает строковое представление объекта
plain      возвращает развёрнутое представление объекта

html_type  возвращает тип объекта для html
html_val   html-версия функции plain_val
html       html-версия функции plain
html_r     вспомогательная функция для функции html

plain_l    нумерует каждую строку в заданной
html_l     html-версия функции plain_l
"""


def plain_val(obj):
    if obj is None:
        buf = u'/is None/'
    elif isinstance(obj, (int, float, long, complex)):
        buf = unicode(obj)
    else:
        try:
            buf = unicode(obj)
        except:
            buf = repr(obj)
            buf = buf.replace(r'\n', '\n')
            buf = buf.replace(r'\r', '')

    return buf


def plain(obj):
    buf = u'\n'

    # === Iter ===
    buf += u'Iter свойства:\n==============\n'
    list_buf = u''
    if not isinstance(obj, basestring):
        try:
            for val in obj:
                list_buf += "{}\n".format(plain_val(val))
        except:
            pass

    if list_buf:
        buf += list_buf
    buf += u'\n'

    # === Dict ===
    buf += u'Dict свойства:\n==============\n'
    list_buf = u''
    if not isinstance(obj, basestring):
        try:
            for key, val in obj.items():
                list_buf += u'{:20}: {}\n'.format(key, plain_val(val))
        except:
            pass

    if list_buf:
        buf += list_buf
    buf += u'\n'

    # === dict ===
    buf += u'dict свойства:\n==============\n'
    if hasattr(obj, '__dict__'):
        d = obj.__dict__
        for key in sorted(d.keys()):
            if key[0:2] != '__':
                val = d.get(key)
                buf += u'{:20}: {}\n'.format(key, plain_val(val))

    buf += u'\n'

    # === dir ===
    buf += u'dir свойства:\n=============\n'
    dirs_buf = u''
    for key in dir(obj):
        val = getattr(obj, key)
        if not callable(val):
            if key[0:2] != '__':
                dirs_buf += u'{:20}: {}\n'.format(key, plain_val(val))

    if dirs_buf:
        buf += dirs_buf
    buf += u'\n'

    # === Callable ===
    buf += u'Callable свойства:\n==================\n'
    dirs_buf = u''
    for key in dir(obj):
        val = getattr(obj, key)
        if callable(val):
            if key[0:2] != '__':
                dirs_buf += u'{:20}: {}\n'.format(key, plain_val(val))

    if dirs_buf:
        buf += dirs_buf
    buf += u'\n'

    return buf


def html_type(obj):
    return escape(plain_val(type(obj)))


def html_val(obj, color=""):
    type_obj = html_type(obj)
    obj = escape(plain_val(obj))
    obj = obj.replace('\r\n', '<br />')
    obj = obj.replace('\r',   '<br />')
    obj = obj.replace('\n',   '<br />')
    if color:
        buf = u'<span title="{}" style="color: {}">{}</span>'.format(type_obj, color, obj)
    else:
        buf = u'<span title="{}">{}</span>'.format(type_obj, obj)

    return buf


def html(obj, it=1, root=None, collection=[]):
    # Переменная collection постоянно накопляется, поэтому сбрасываем её при
    # новом использовании функции html
    if root is None:
        collection = []

    if root is obj:
        return u'<span style="color: red"><i>on self</i></span>'

    buf = ""

    if obj is None:
        buf = u'<span style="color: Gray"><i>is None</i></span>'
    elif isinstance(obj, (int, float, long, complex)):
        buf = html_val(obj, 'blue')
    elif isinstance(obj, (basestring, bytearray)):
        buf = html_val(obj)

    if buf:
        return buf

    # Использование "if obj in collection" в некоторых случаях недопустимо!
    for i in collection:
        if i is obj:
            return html_val(obj, "red")
    collection.append(obj)

    if isinstance(obj, (list, tuple)):
        buf = u'<ul>\n'
        for value in obj:
            buf += u'<li>{}</li>'.format(html(value, it, obj, collection))
        buf += u'</ul>\n'
    elif isinstance(obj, dict):
        buf = u'<ul>\n'
        for key, value in obj.items():
            buf += u'<li>{}: {}</li>'.format(key, html(value, it, obj, collection))
        buf += u'</ul>\n'

    if buf:
        return buf

    # Итерацию проверяем только для объектов
    if not it:
        return html_val(obj, "Dimgray")
    it -= 1

    buf = html_r(obj, it, root, collection)

    return buf


def html_r(obj, it=1, root=None, collection=[]):
    buf = u'<table border="1">\n'
    buf += u'  <tr><th colspan="2" style="background-color: Cornflowerblue">{}</th></tr>\n'.format(html_val(obj))

    # === DIR ===
    dirs_buf = u''
    for key in dir(obj):
        val = getattr(obj, key)
        if not ismethod(val):
            if key[0:2] != '__':
                dirs_buf += u'  <tr><td style="color: blue"><b>{}</b></td><td>{}</td></tr>\n'.format(key, html(val, it, obj, collection))
    if dirs_buf:
#       buf += u'  <tr><th colspan="2" style="background-color: yellow">Dirs свойства:</th></tr>\n{}'.format(dirs_buf)
        buf += dirs_buf

    # === ITER ===
#     if not isinstance(obj, basestring):
#         list_buf = u''
#         try:
#             for val in obj:
#                 list_buf += u'  <tr><td></td><td>{}</td></tr>\n'.format(html(val, it, obj, collection))
#         except:
#             pass
#         if list_buf:
#             buf += u'  <tr><th colspan="2" style="background-color: yellow">Iter свойства:</th></tr>\n{}'.format(list_buf)

    # === DICT ===
#     if hasattr(obj, '__dict__'):
#         buf += u'  <tr><th colspan="2" style="background-color: yellow">Dict свойства:</th></tr>\n'
#         d = obj.__dict__
#         for key in sorted(d.keys()):
#             if key[0:2] != '__':
#                 val = d.get(key)
#                 buf += u'  <tr><td style="color: blue"><b>{}</b></td><td>{}</td></tr>\n'.format(key, html(val, it, obj, collection))

    buf += u'</table>\n'

    return buf


def plain_l(obj):
    buf = u''

    if isinstance(obj, basestring):
        obj = obj.replace('\r\n', '\n')
        obj = obj.replace('\r',   '\n')
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
        obj = obj.replace('\r\n', '\n')
        obj = obj.replace('\r',   '\n')
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
