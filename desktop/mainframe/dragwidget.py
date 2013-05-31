#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-02

import sys
from PySide import QtCore, QtGui

import dragwidget_rc
from dialog_settings import Settings
from task_item import init_task, draw_task


class DragWidget(QtGui.QFrame):
    def __init__(self, parent=None):
        super(DragWidget, self).__init__(parent)
        self.parent = parent
        self.settings = self.window().settings

        self.setMinimumSize(320, 240)
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.setAcceptDrops(True)

        # Текущий перетаскиваемый объект
        self.taskData = None


# События


    # Событие, возникающее при перенесении объекта над другим объектом
    def dragEnterEvent(self, event):
        if event.source() == self:
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            return

        urls = event.mimeData().urls()
        if urls:
            event.acceptProposedAction()
        else:
            event.ignore()


#   dragMoveEvent = dragEnterEvent


    # Событие, возникающее при отпускании объекта
    def dropEvent(self, event):
        if event.source() == self:
            self.taskData['pos'] = event.pos()
            draw_task(self, self.taskData)
            self.taskData = None

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            return

        urls = event.mimeData().urls()
        if urls:
            sources = [i.path() for i in urls]
            task = init_task(self, sources, event.pos())
            draw_task(self, task)

            event.accept()
        else:
            event.ignore()


    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        offset = event.pos() - child.pos()
        child.taskData['offset'] = offset

        mimeData = QtCore.QMimeData()

        # Сохраняем данные активной задачи
        self.taskData = child.taskData
#         taskData = QtCore.QByteArray()
#         dataStream = QtCore.QDataStream(taskData, QtCore.QIODevice.WriteOnly)
#         dataStream << child.taskData
#         mimeData.setData('application/x-taskdata', taskData)

        # Извлекаем отображение иконки
        pixmap = QtGui.QPixmap(self.taskData.get('img'))

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

        child.setPixmap(tempPixmap)

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(pixmap)


    def mouseDoubleClickEvent(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        offset = event.pos() - child.pos()
        child.taskData['offset'] = offset

        dialog = Settings(self.parent, child.taskData, self.settings)
        res = dialog.exec_()


# Сервисные функции


    def tasks_list(self):
        for child in self.children():
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
