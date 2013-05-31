#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-14

import sys, os
from PySide import QtCore, QtGui
from sqlalchemy import types

import dragwidget_rc


def init_task(parent, sources=None, pos=None):
    count = len(sources)
    name = os.path.basename(sources[0]) if sources else u"Новая задача"
    if count > 1:
        name = u"{0} [{1}]".format(name, count)

    task = dict(name=name, img=":/images/file.png", pos=pos, offset='*half*',
                sources=sources)
    return task


def draw_task(parent, task):
    name   = task.get('name', u"/Без имени/")
    img    = task.get('img', ":/images/file.png")
    pos    = task.get('pos')
    offset = task.get('offset')

    if isinstance(pos, QtCore.QPoint):
        pos = pos.toTuple()
    if isinstance(offset, QtCore.QPoint):
        offset = offset.toTuple()

    taskIcon = QtGui.QLabel(parent)

    if pos:
        if offset == '*half*':
            rect = QtGui.QPixmap(img).rect()
            offset = (rect.width() // 2, rect.height() // 2)
        if offset:
            pos = correct_pos(pos, offset)
        taskIcon.move(*pos)
        task['pos'] = pos

    # Данные задачи
    task['name'] = name
    task['img'] = img
    task['pos'] = pos
    task['offset'] = offset
    taskIcon.taskData = task
    taskIcon.taskData['icon'] = taskIcon

    redraw_task(taskIcon.taskData)

    taskIcon.show()
    taskIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    return taskIcon


def redraw_task(taskData):
    taskIcon = taskData.get('icon')
    img = taskData.get('img', '')
    name = taskData.get('name', '')

#   taskIcon.setPixmap(QtGui.QPixmap(img))
    taskIcon.setText(u'<p align="center"><img src="{}"/><br/>{}</p>'.format(img, name))


def mark_task_deleted(taskData):
    taskIcon = taskData.get('icon')
    pixmap = QtGui.QPixmap(taskData.get('img'))
    painter = QtGui.QPainter()
    painter.begin(pixmap)
    painter.fillRect(pixmap.rect(), QtGui.QColor(127, 127, 127, 127))
    painter.end()
    taskIcon.setPixmap(pixmap)


def correct_pos(pos, offset=None):
    if offset:
        pos = (pos[0] - offset[0], pos[1] - offset[1])
    return pos
