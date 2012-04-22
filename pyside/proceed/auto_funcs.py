#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-07

from lib.sheet_funcs import get_date


def proceed_date(joint_dict, item):
    date = joint_dict.get(item)
    if date:
        date, date_str = get_date(date)
        joint_dict[item] = date
        joint_dict[item+'_str'] = date_str
