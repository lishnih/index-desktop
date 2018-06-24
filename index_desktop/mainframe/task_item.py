#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-14

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
import os
import subprocess
import multiprocessing
import logging
from PySide import QtCore, QtGui
from sqlalchemy import types

from . import dragwidget_rc


def init_task(parent, sources=[], pos=None):
    name = os.path.basename(sources[0]) if sources else "Новая задача"
    count = len(sources)
    if count > 1:
        name = name + "+"

    sources = set(sources)
    proceed = ""
    method  = ""
    task = dict(name=name, pos=pos, img=":/images/file.png",
           sources=sources, proceed=proceed, method=method)
    return task


def draw_task(parent, task, offset=None, middle=None):
    taskIcon = QtGui.QLabel(parent)
    pos = task.get('pos')
    img = task.get('img', ":/images/file.png")

    if isinstance(pos, QtCore.QPoint):
        pos = pos.toTuple()
    if isinstance(offset, QtCore.QPoint):
        offset = offset.toTuple()

    taskIcon.taskData = task
    taskIcon.taskData['icon'] = taskIcon

    redraw(taskIcon)
    taskIcon.show()

    if pos:
        if middle:
            rect = taskIcon.rect()
            offset = (rect.width() // 2, rect.height() // 2)
        if offset:
            pos = correct_pos(pos, offset)
            task['pos'] = pos
        taskIcon.move(*pos)

    taskIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    return taskIcon


def redraw(child):
    taskData = child.taskData
    name = taskData.get('name', "/Без имени/")
    img  = taskData.get('img',  ":/images/file.png")
    taskIcon = taskData.get('icon')

    sources = taskData.get('sources', [])
    count = len(sources)

    taskIcon.setText('<p align="center"><img src="{0}"/><br/>{1}<br/>Всего {2} элем.</p>'.format(img, name, count))


def highlight(child):
    rect = child.rect()
    w, h = rect.width(), rect.height()
    pixmap = QtGui.QPixmap(w, h)
    pixmap.fill(QtGui.QColor(127, 127, 127, 63))

    taskData = child.taskData
    taskIcon = taskData.get('icon')
    taskIcon.setPixmap(pixmap)


def correct_pos(pos, offset):
    if offset:
        pos = (pos[0] - offset[0], pos[1] - offset[1])
    return pos


def proceed_task(taskData):
    proceed = taskData.get('proceed')
    name    = taskData.get('name')
    method  = taskData.get('method')
    sources = taskData.get('sources')

    if proceed:
        args = [sys.executable, proceed]

        name = taskData.get('name')
        if name:
            args.extend(['--task', name])

        method = taskData.get('method')
        if method:
            args.extend(['--method', method])

        sources = [i for i in taskData.get('sources', [])]
        if sources:
            args.extend(sources)

        p = multiprocessing.Process(target=worker, args=args)
        p.start()
    else:
        QtGui.QMessageBox.warning(None, "Warning", """Скрипт proceed не задан!""")


def worker(*args):
    print(args)

    fse = sys.getfilesystemencoding()
    args = [i.encode(fse) for i in args]

#   args = [sys.executable, '--help']
    proc = subprocess.Popen(args, stderr=subprocess.STDOUT)
    proc.communicate()
