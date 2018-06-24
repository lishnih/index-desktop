#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
from PySide import QtCore, QtGui

from . import dragwidget_rc
from .dialog_settings import Settings
from .task_item import init_task, draw_task, redraw, highlight, proceed_task


class DragWidget(QtGui.QFrame):
    def __init__(self, parent=None, settings=None, s=None):
        super(DragWidget, self).__init__(parent)
        self.parent = parent
        self.settings = settings
        self.s = s

        self.setMinimumSize(320, 240)
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.setAcceptDrops(True)

        # Контекстное меню
        self.actionProceed = QtGui.QAction(self)
        QtCore.QObject.connect(self.actionProceed, QtCore.SIGNAL("triggered()"), self.OnProceed)
        self.actionProceed.setText(QtGui.QApplication.translate("DragWidget", "Proceed", None, QtGui.QApplication.UnicodeUTF8))

        self.actionDebug = QtGui.QAction(self)
        QtCore.QObject.connect(self.actionDebug, QtCore.SIGNAL("triggered()"), self.OnDebug)
        self.actionDebug.setText(QtGui.QApplication.translate("DragWidget", "Debug", None, QtGui.QApplication.UnicodeUTF8))

        self.actionDelete = QtGui.QAction(self)
        QtCore.QObject.connect(self.actionDelete, QtCore.SIGNAL("triggered()"), self.OnDelete)
        self.actionDelete.setText(QtGui.QApplication.translate("DragWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))

        self.menuTask = QtGui.QMenu()
        self.menuTask.addAction(self.actionProceed)
        self.menuTask.addAction(self.actionDebug)
        self.menuTask.addAction(self.actionDelete)

        # Выбранный объект
        self.selected = None


# События

    # Событие, возникающее при захватывании объекта
    def dragEnterEvent(self, event):
        source = event.source()

        if source == self:
            child = self.childAt(event.pos())
            if not child or child == self.selected:
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
            return

        if source is None:
            urls = event.mimeData().urls()
            if urls:
                event.acceptProposedAction()
            else:
                event.ignore()
            return

    # Событие, возникающее при передвижении объекта
#   dragMoveEvent = dragEnterEvent

    # Событие, возникающее при отпускании объекта
    def dropEvent(self, event):
        source = event.source()
        pos = event.pos()

        if source == self:
            offset = None
            if event.mimeData().hasFormat('application/x-dnditemdata'):
                itemData = event.mimeData().data('application/x-dnditemdata')
                dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)

                pixmap = QtGui.QPixmap()
                offset = QtCore.QPoint()
                dataStream >> offset

            self.selected.taskData['pos'] = pos
            draw_task(self, self.selected.taskData, offset=offset)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            return

        if source is None:
            urls = event.mimeData().urls()
            if urls:
                sources = [i.path()[1:] for i in urls]

                child = self.childAt(pos)
                if child:
                    child_sources = child.taskData.get('sources', [])
                    child_sources.update(sources)
                    redraw(child)
                else:
                    task = init_task(self, sources, pos)
                    draw_task(self, task, middle=1)

                event.accept()
            else:
                event.ignore()
            return

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mousePressEvent_Left(event)
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mousePressEvent_Right(event)

    def mousePressEvent_Left(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        self.selected = child

        # Извлекаем отображение иконки
#       pixmap = QtGui.QPixmap(child.pixmap())
        pixmap = QtGui.QPixmap(child.taskData.get('img'))

        offset = event.pos() - child.pos()

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << QtCore.QPoint(offset)

        mimeData = QtCore.QMimeData()
        mimeData.setData('application/x-dnditemdata', itemData)

        # Создаём QDrag
        rect = child.rect()
        w, h = rect.width(), rect.height()
        pixmap = QtGui.QPixmap(w, h)
        pixmap.fill(QtGui.QColor(255, 255, 255, 127))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(offset)

        # Выделяем иконку
        highlight(child)

        res = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.MoveAction)
#       print res
        if res == QtCore.Qt.MoveAction:
            child.close()
        else:
            redraw(child)

    def mousePressEvent_Right(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        self.selected = child

        pos = self.mapToGlobal(event.pos())
        self.menuTask.popup(pos)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseDoubleClickEvent_Left(event)

    def mouseDoubleClickEvent_Left(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        # Выделяем иконку
        highlight(child)

        dialog = Settings(self.parent, child, self.settings, self.s)
        res = dialog.exec_()

    def OnProceed(self):
        proceed_task(self.selected.taskData)

    def OnDebug(self):
        print(self.selected.taskData)
        print()

    def OnDelete(self):
        self.selected.close()


# Сервисные функции

    def tasks_list(self):
        for child in self.children():
            if hasattr(child, 'taskData'):
                yield child.taskData


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    mainWidget = QtGui.QWidget()
    vLayout = QtGui.QVBoxLayout()
    vLayout.addWidget(DragWidget())

    mainWidget.setLayout(vLayout)
    mainWidget.setWindowTitle(QtCore.QObject.tr(mainWidget, "MainWindow"))
    mainWidget.show()

    sys.exit(app.exec_())
