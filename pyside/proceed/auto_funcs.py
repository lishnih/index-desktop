#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-07

import re, logging

from lib.data_funcs import get_int_str
from lib.sheet_funcs import get_date


def proceed_date(_dict, item):
    val = _dict.get(item)
    if val:
        date, date_str = get_date(val)
        _dict[item] = date
        _dict[item+'_str'] = date_str


def proceed_joint(_dict, item):
    val = _dict.get(item)
    if val:
        res = re.match(u'(\w+)-(.*)-(\d+)', val, re.UNICODE)
        if res:
            joint_pre, joint_line, joint_seq = res.groups()
            _dict[item+'_pre']  = joint_pre
            _dict[item+'_line'] = joint_line
            _dict[item+'_seq']  = joint_seq
            return

        res = re.match(u'(\d+)-(\d+)', val)
        if res:
            joint_pre, joint_seq = res.groups()
            _dict[item+'_pre'] = joint_pre
            _dict[item+'_seq'] = joint_seq
            return

        logging.warning(val)


def proceed_d_w_th(_dict, item):
    val = _dict.get(item)
    if val:
        if val == '---':
            return
# 273Х10/Ду80Х4
        if isinstance(val, basestring):
            res = re.match(u'(\d+) *[XХxх*] *(\d+) *(?:/(?:Ду)?(\d+) *[XХxх*] *(\d+))?', val)
            if res:
                d1, th1, d2, th2 = res.groups()
                _dict['diameter1']  = d1
                _dict['thickness1'] = th1
                _dict['diameter2']  = d2
                _dict['thickness2'] = th2
                return
            res = re.match(u'(\d+\.?\d*)', val)
            if res:
                th1, = res.groups()
                th1 = float(th1)
                _dict['thickness1'] = th1
                return
        elif isinstance(val, float) or isinstance(val, int):
            th1 = val
            _dict['thickness1'] = th1
            return

        logging.warning(val)


def proceed_report_w_date(_dict, item):
    val = _dict.get(item)
    if val:
        res = re.match(u'(.*) от (.*)', val)
        if res:
            report_str, date_str = res.groups()

            date, date_str = get_date(date_str)
            _dict['date'] = date
            _dict['date_str'] = date_str

            _dict['report'] = report_str
            res = re.match(u'(?:(.*)/)?(.*)', report_str)
            if res:
                report_pre, report_seq = res.groups()

                _dict['report_pre'] = report_pre
                _dict['report_seq'] = report_seq
            return

        logging.warning(val)
