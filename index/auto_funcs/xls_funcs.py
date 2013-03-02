#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-07

import re, logging

from lib.sheet_funcs import get_date


def proceed_int(_dict, item, OBJ):
    val = _dict.get(item)
    if val == None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    else:
        return int(val)


def proceed_int_str(_dict, item, OBJ):
    val = _dict.get(item)
    if val == None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    elif isinstance(val, basestring):
        _dict[item] = int(val) if val.isdigit() else val
    else:
        _dict[item] = int(val)


def proceed_float(_dict, item, OBJ):
    val = _dict.get(item)
    if val == None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    else:
        _dict[item] = float(val)


def proceed_date(_dict, item, OBJ):
    val = _dict.get(item)
    if val:
        date, date_str = get_date(val)
        _dict[item] = date
        _dict[item+'_str'] = date_str


def prepare_doc_vt_act(_dict, item, OBJ):
    _dict['type'] = u"Акт ВК"

    val = _dict.get(item)
    if val:
        _dict['doc_pre'] = ""
        _dict['doc_seq'] = val


def prepare_doc_invoice(_dict, item, OBJ):
    _dict['type'] = u"Накладная"

    val = _dict.get(item)
    if val:
        _dict['doc_pre'] = ""
        _dict['doc_seq'] = val


def proceed_piece(_dict, item, OBJ):
    if 'piece_type' not in _dict:
        _dict['piece_type'] = None
    if 'piece_scheme' not in _dict:
        _dict['piece_scheme'] = None
    name_list = filter(lambda x: x, [_dict['piece_type'], _dict['piece_name'], _dict['piece_scheme']])
    name_list = map(unicode, name_list)
    _dict['piece'] = u" ".join(name_list)


def proceed_joint(_dict, item, OBJ):
    val = _dict.get(item)
    _dict[item+'_pre']  = None
    _dict[item+'_line'] = None
    _dict[item+'_seq']  = None

    if val:
        res = re.match(u'([\w.-]+)-(\w+)-(\d+)', val, re.UNICODE)
        if res:
            joint_pre, joint_line, joint_seq = res.groups()
            _dict[item+'_pre']  = joint_pre
            _dict[item+'_line'] = joint_line
            _dict[item+'_seq']  = joint_seq
            return

        res = re.match(u'(\d+)-(\d+)', val)
        if res:
            joint_pre, joint_seq = res.groups()
            _dict[item+'_pre']  = joint_pre
            _dict[item+'_seq']  = joint_seq
            return

    logging.warning('proceed_joint')
    logging.warning(val)


def proceed_d_w_th(_dict, item, OBJ):
    val = _dict.get(item)
    _dict['diameter1']  = None
    _dict['thickness1'] = None
    _dict['diameter2']  = None
    _dict['thickness2'] = None

    if val:
        if val == '---':
            return

        if isinstance(val, basestring):
            res = re.match(u'(\d+) *[XХxх*] *(\d+) *(?:/(?:Ду)?(\d+) *[XХxх*] *(\d+))?', val)   # 273x10/Ду80x4
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
                _dict['thickness1'] = float(th1)
                return

        elif isinstance(val, (float, int)):
            _dict['thickness1'] = val
            return

    logging.warning('proceed_d_w_th')
    logging.warning(val)


def proceed_report_w_date(_dict, item, OBJ):
    _dict['report_pre'] = None
    _dict['report_seq'] = None
    _dict['date']       = None
    _dict['date_str']   = None

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

    logging.warning('proceed_report_w_date')
    logging.warning(val)


def proceed_dt_doc_name(_dict, item, OBJ):
    _dict['type'] = u"Протокол МИ"

    name_list = _dict[item+'_list']
    if name_list:
        pre, null, seq = name_list

        _dict['doc_pre'] = pre
        _dict['doc_seq'] = seq
