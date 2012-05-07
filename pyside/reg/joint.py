#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from models import DBSession, Joint
from lib.items import FileItem


def reg_joint(joint_dict, SHEET=None, show=True):
    JOINT = Joint(**joint_dict)

    JOINT.sheet = SHEET

    DBSession.add(JOINT)

    # Графика
    if show and hasattr(SHEET, 'tree_item'):
        JOINT.tree_item = FileItem(SHEET.tree_item, JOINT.name, summary=JOINT)
        JOINT.tree_item.setOk()

    return JOINT
