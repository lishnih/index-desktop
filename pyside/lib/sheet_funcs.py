#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import re, time, calendar
import xlrd


def get_value(sh, row, col):
    try:
        typ = sh.cell_type(row, col)
        val = None if typ == xlrd.XL_CELL_ERROR else sh.cell_value(row, col)
        if isinstance(val, basestring):
            val = val.strip()
    except IndexError:
        val = None
    return val


def get_index(letter):
    index_len = len(letter)
    if index_len == 1:
        return ord(letter.upper()) - 65
    elif index_len == 2:
        i1 = (get_index(letter[0]) + 1) * 26
        i2 = get_index(letter[1])
        return i1 + i2
    else:
        assert "get_index error"


def get_date(date_str):
    date = 0
    try:            # пытаемся распознать дату из числа
        date_tuple = xlrd.xldate_as_tuple(int(date_str), 0)
        date_list = list(date_tuple)
        date_list.extend([0, 0, 0])
        date = int(time.mktime(date_list))
        date_str = ("%02u.%02u.%02u") % (date_tuple[2], date_tuple[1], date_tuple[0])
    except:         # дата, возможно, записана в текстовом формате
        res = re.search(ur"(\d{1,2}).(\d{1,2}).(\d{4}|\d{2})", date_str)
        if res:
            reslist = res.groups()
            day, month, year = reslist
            date_str = "{}.{}.{}".format(day, month, year)
            year = int(year)
            date = calendar.timegm(time.strptime(date_str, "%d.%m.%Y")) if year >= 100 else \
                   calendar.timegm(time.strptime(date_str, "%d.%m.%y"))

    return date, date_str
