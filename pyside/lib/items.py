#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-30

from PySide import QtCore, QtGui


class Item(QtGui.QTreeWidgetItem):
    def __init__(self, parent, item_name, brief=None, summary=None):
        super(Item, self).__init__(parent)
        self.res = None
        self.parent = parent

        self.setText(0, item_name)

        self.setBrief(brief)
        self.setSummary(summary)


    def setBrief(self, brief=None):
        self.setData(0, QtCore.Qt.UserRole, brief)


    def setSummary(self, summary=None):
        self.setData(1, QtCore.Qt.UserRole, summary)


    def setOk(self, message=None):
        if not message:
            message = u"Обработка этого элемента прошла успешно!"

        brief = self.data(0, QtCore.Qt.UserRole)
        brief = u"{}\n---\n{}".format(message, brief)
        self.setBrief(brief)
        self.setResult(0)


    def setWarning(self, message=None):
        if not message:
            message = u"Обработка этого элемента прошла с замечаниями!"

        brief = self.data(0, QtCore.Qt.UserRole)
        brief = u"{}\n---\n{}".format(message, brief)
        self.setBrief(brief)
        self.setResult(-1)

        if isinstance(self.parent, Item):
            self.parent.setChildWarning(message, self)


    def setError(self, message=None):
        if not message:
            message = u"Обработка этого элемента прошла с ошибками!"

        brief = self.data(0, QtCore.Qt.UserRole)
        brief = u"{}\n---\n{}".format(message, brief)
        self.setBrief(brief)
        self.setResult(-2)

        if isinstance(self.parent, Item):
            self.parent.setChildError(message, self)


    def setChildWarning(self, message=None, reason_item=None):
        if not message:
            message = u"Обработка элемента прошла с замечаниями!"

        if reason_item:
            item_name = reason_item.text(0)
            message = u"[{}] {}".format(item_name, message)

        brief = self.data(0, QtCore.Qt.UserRole)
        brief = u"{}\n---\n{}".format(brief, message)
        self.setBrief(brief)
        self.setResult(-1)

        if isinstance(self.parent, Item):
            self.parent.setChildWarning(message)


    def setChildError(self, message=None, reason_item=None):
        if not message:
            message = u"Обработка элемента прошла с ошибками!"

        if reason_item:
            item_name = reason_item.text(0)
            message = u"[{}] {}".format(item_name, message)

        brief = self.data(0, QtCore.Qt.UserRole)
        brief = u"{}\n---\n{}".format(brief, message)
        self.setBrief(brief)
        self.setResult(-2)

        if isinstance(self.parent, Item):
            self.parent.setChildError(message)


# setResult - для внутреннего использования
# Коды для res:
# None - неопределено, значение по умолчанию
#    0 - объект/дочерние объекты обработаны успешно
#   -1 - warning во время обработки
#   -2 - error   во время обработки

    def setResult(self, res=None):
        if res == None:
            return

        if self.res == None or self.res > res:
            self.res = res

            if   res ==  0:
                self.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))
            elif res == -1:
                self.setForeground(0, QtGui.QBrush(QtCore.Qt.darkYellow))
            elif res == -2:
                self.setForeground(0, QtGui.QBrush(QtCore.Qt.red))

            if isinstance(self.parent, Item):
                self.parent.setResult(res)


    def set_bold(self):
        font = self.font(0)
        font.setBold(True)
        self.setFont(0, font)


    def set_italic(self):
        font = self.font(0)
        font.setItalic(True)
        self.setFont(0, font)


# Элемент дерева - директория
class DirItem(Item):
    def __init__(self, *args, **kargs):
        super(DirItem, self).__init__(*args, **kargs)

        self.set_bold()


# Элемент дерева - файл
class FileItem(Item):
    pass


# Элемент дерева - отключенный элемент
class DisabledItem(Item):
    def __init__(self, *args, **kargs):
        super(DisabledItem, self).__init__(*args, **kargs)

        self.set_italic()
