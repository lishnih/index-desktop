#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10, 2012-09-28

import os, re

from reg import reg_object
from models import Dir


def proceed_dir(dirname, options, TASK):
    basename = os.path.basename(dirname)

    dir_dict = dict(_task=TASK, name=dirname)
    DIR = reg_object(Dir, dir_dict, TASK, style='B')

    return DIR
