#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-14

import sys, os
from PySide import QtCore, QtGui
from sqlalchemy import types

import dragwidget_rc

from models import Task, Source
from reg import reg_object, reg_object1


# class TaskItem(object):
#     def __init__(self, parent=None):
#         super(DragWidget, self).__init__(parent)
#         self.parent = parent


# Инициализует все переменные таблицы Task
def init_from_schema(Schema):
    task = dict()
    for Column in Schema.c:
        i = Column.key
        if i != 'id':
            t = type(Column.type)
            if t == types.Integer:
                value = 0
            else:
                value = ''
            task[i] = value
    return task


def init_task_item_from_db(parent, TASK):
    task_schema = Task.__table__
    task = init_from_schema(task_schema)

    task['_ROW'] = TASK

    for Column in task_schema.c:
        i = Column.key
        if i != 'id':
            value = getattr(TASK, i)
            if value:
                task[i] = value

    try:
        task['pos'] = TASK.pos_x, TASK.pos_y
    except:
        task['pos'] = 0, 0

    draw_task(parent, task)

#   return task


def init_task_item_from_dnd(parent, sources=None, pos=None):
    task_schema = Task.__table__
    task = init_from_schema(task_schema)

    count = len(sources)
    name = os.path.basename(sources[0]) if sources else u"Новая задача"
    if count > 1:
        name = u"{} и др.".format(name)

#     task = dict(name=name, pos=pos, count=count, offset='*half*')
    task['name']   = name
    task['img']    = ":/images/file.png"
    task['pos']    = pos
    task['count']  = count
    task['offset'] = '*half*'
    taskIcon = draw_task(parent, task)

    task = taskIcon.taskData    # без этого не работает
    pos = task.get('pos')
    if pos:
        task['pos_x'], task['pos_y'] = pos

    TASK = reg_object(Task, task)

    task['_ROW'] = TASK
    task['icon'] = taskIcon

    append_source(TASK, sources)

    return task


def update_row(task):
    TASK = task.get('_ROW')
    if not TASK:
        print("Error in task: {!r}".format(task))

    pos = task.get('pos')
    if pos:
        TASK.pos_x, TASK.pos_y = pos

    TASK.name = task.get('name')


def update_column(task, key, value):
    print(key, task.get(key), value)
    task[key] = value

#   task_schema = Task.__table__
    TASK = task.get('_ROW')
    try:
        setattr(TASK, key, value)
    except Exception as e:
        print(u"Не удалось обновить запись".format(e))


def append_source(TASK, sources):
    if sources:
        for filename in sources:
            if os.name == 'nt': # !!! Через командную строку без этого не распознаётся
                filename = filename[1:]
            source = dict(
                _task = TASK,
                name = filename,
            )
            SOURCE = reg_object(Source, source)


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


# Для отображения значка задачи нам необходимы следующие данные:
# name, img, pos, offset
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
