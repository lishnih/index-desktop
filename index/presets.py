#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-28

import os, time

from presets_dict import presets


tracing = []


def add_preset():
    return


def has_preset(preset):
    return preset in presets


def get_preset(preset):
    preset_dict = presets.get(preset, {})
    return (
             preset_dict.get('enabled'),
             preset_dict.get('taskname'),
             preset_dict.get('config', {})
           )


def get_presets():
    for preset in presets.keys():
        l = [preset]
        l.extend(get_preset(preset))
        yield l


try:
    mtime = time.localtime(os.path.getmtime(__file__))
    rev = time.strftime("%Y%m%d", mtime)
except os.error:
    rev = "<undefined>"

version_info = (0, 4, rev)
__version__  = '.'.join(map(str, version_info))
version      = __version__
