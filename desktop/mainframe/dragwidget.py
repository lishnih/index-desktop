#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-02

import sys
from PySide import QtCore, QtGui

import dragwidget_rc
from dialog_settings import Settings
from task_item import init_task, draw_task


class DragWidget(QtGui.QFrame):
    def __init__(self, parent=None, settings=None, s=None):
        super(DragWidget, self).__init__(parent)
        self.parent = parent
        self.settings = settings
        self.s = s

        self.setMinimumSize(320, 240)
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.setAcceptDrops(True)

        # Выпадающее меню
        self.actionDelete = QtGui.QAction(self)
        QtCore.QObject.connect(self.actionDelete, QtCore.SIGNAL("triggered()"), self.deleteEvent)
        self.actionDelete.setText(QtGui.QApplication.translate("DragWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))

        self.menuTask = QtGui.QMenu()
        self.menuTask.addAction(self.actionDelete)

        # Текущий (перетаскиваемый) объект
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

        if source == None:
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

        if source == self:
            self.selected.taskData['pos'] = event.pos()
            draw_task(self, self.selected.taskData)
            self.selected = None

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            return

        if source == None:
            urls = event.mimeData().urls()
            if urls:
                sources = [i.path() for i in urls]
                task = init_task(self, sources, event.pos())
                draw_task(self, task)
    
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

        offset = event.pos() - self.selected.pos()
        self.selected.taskData['offset'] = offset

        mimeData = QtCore.QMimeData()

        # Извлекаем отображение иконки
        pixmap = QtGui.QPixmap(self.selected.taskData.get('img'))

        # Создаём QDrag
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(offset)

        # Затемняем иконку
        tempPixmap = QtGui.QPixmap(pixmap)
        painter = QtGui.QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QtGui.QColor(127, 127, 127, 127))
        painter.end()

        self.selected.setPixmap(tempPixmap)

        res = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.MoveAction)
#       print res
        if res == QtCore.Qt.MoveAction:
            self.selected.close()
        else:
            self.selected.show()
            self.selected.setPixmap(pixmap)


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

        self.selected = child

        offset = event.pos() - self.selected.pos()
        self.selected.taskData['offset'] = offset

        dialog = Settings(self.parent, self.selected.taskData, self.settings)
        res = dialog.exec_()


    def deleteEvent(self):
        print self.selected
        self.selected.close()
        self.selected = None


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
