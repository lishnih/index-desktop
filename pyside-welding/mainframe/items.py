#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-30

from PySide import QtCore, QtGui


class Item(QtGui.QTreeWidgetItem):
    def __init__(self, parent, item_name, summary=None):
        super(Item, self).__init__(parent)
        self.setText(0, item_name)

        self.setSummary(summary)


# Условно принимаем следующие коды для res:
#   1 - обработка прошла, объект обработан
#   0 - обработка прошла, объект в обработке не нуждается
# - 1 - неопределено, присваевается перед обработкой, если не изменилось после
#       обработки, значит, что-то забыл обновить))
# - 2 - обработка прошла,   warning   во время обработки
# - 3 - обработка прошла,   error     во время обработки
# - 5 - обработка прервана, exception во время обработки

    def setResult(self, res=None):
        if   res ==  0:
            self.setForeground(0, QtGui.QBrush(QtCore.Qt.lightGray))
        elif res == -1:     # 11111111
            self.setForeground(0, QtGui.QBrush(QtCore.Qt.darkGray))
        elif res == -2:     # 11111110
            self.setForeground(0, QtGui.QBrush(QtCore.Qt.darkYellow))
        elif res == -3:     # 11111101
            self.setForeground(0, QtGui.QBrush(QtCore.Qt.red))
        elif res == -5:     # 11111011
            self.setForeground(0, QtGui.QBrush(QtCore.Qt.darkRed))


    def setSummary(self, summary=None):
        if summary:
            self.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))
            self.setData(0, QtCore.Qt.UserRole, summary)
        else:
            self.setForeground(0, QtGui.QBrush(QtCore.Qt.black))
            self.setData(0, QtCore.Qt.UserRole, None)



# Элемент дерева - директория
class DirItem(Item):
    def __init__(self, parent, item_name, summary=None):
        super(DirItem, self).__init__(parent, item_name, summary=summary)

        font = self.font(0)
        font.setBold(True)
        self.setFont(0, font)



# Элемент дерева - файл
class FileItem(Item):
    pass
