#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-08

import sys, subprocess, multiprocessing, logging
from PySide import QtCore, QtGui


# from dialog_settings_test_ui import Ui_Dialog
from dialog_sources import Sources

from task_item import redraw_task, mark_task_deleted


def worker(*args):
    args, indexscript = args
    logging.info(u"Cwd: {}".format(indexscript))

    # Кодируем строки в пендосовскою кодировку
    newargs = []
    for arg in args:
        if isinstance(arg, unicode):
            arg = arg.encode('utf-8')
        newargs.append(arg)
    args = newargs
    logging.info(u"Запуск процесса с параметрами: {!r}".format(args))

#   args = [sys.executable, 'main.py', '--help']
    proc = subprocess.Popen(args, stderr=subprocess.STDOUT, cwd=indexscript)
    proc.communicate()


class Settings(QtGui.QDialog):
    def __init__(self, parent, taskData, settings=None):
        super(Settings, self).__init__(parent)
        self.parent = parent
        self.taskData = taskData
        self.settings = settings

        # Загружаем элементы диалога
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Восстанавливаем состояние окна
        self.loadDialogSettings()

        # Добавляем виджеты
        Dialog = self
        formLayout = self.ui.formLayout

        i = 0
        for key in sorted(taskData.keys()):
            value = taskData.get(key)
            tt = str(type(value)).replace('<', '&lt;').replace('>', '&gt;')
            text = u'{}<br/><span style="color:#aaaaaa;">{}</span>'.format(key, tt)
            label = QtGui.QLabel(text, Dialog)
#           label.setFrameStyle(QtGui.QFrame.Panel)
#           label.setLineWidth(1)
#           formLayout.setWidget(i, QtGui.QFormLayout.LabelRole, label)

            lineEdit = QtGui.QLineEdit(unicode(value), Dialog)
            lineEdit.setObjectName("le_{}".format(key))
            if not self.may_change(value):
                lineEdit.setDisabled(True)
#           formLayout.setWidget(i, QtGui.QFormLayout.FieldRole, lineEdit)

#           label.setBuddy(lineEdit)
            formLayout.addRow(label, lineEdit)

            line = QtGui.QFrame(Dialog)
            line.setFrameShape(QtGui.QFrame.HLine)
            line.setFrameShadow(QtGui.QFrame.Sunken)
#           formLayout.setWidget(i+1, QtGui.QFormLayout.SpanningRole, line)

            formLayout.addRow(line)
            i += 2


# События


    def accept(self):
        for key, value in self.taskData.items():
            if self.may_change(value):
                le = self.findChild(QtGui.QLineEdit, "le_{}".format(key))
                le_value = le.text()
                if self.is_changed(self.taskData.get(key), le_value):
                    self.taskData[key] = le_value

        redraw_task(self.taskData)

        self.saveDialogSettings()
        self.done(True)


    def reject(self):
        self.saveDialogSettings()
        self.done(False)


    def closeEvent(self, event):
        self.saveDialogSettings()


    def OnViewSources(self):
        dialog = Sources(self.parent, self.taskData, self.window().settings)
        res = dialog.exec_()


    def OnProceed(self):
        indexscript = self.settings.value("indexscript")
        if indexscript:
            args = [sys.executable, 'main.py']

            name = self.taskData.get('name')
            if name:
                args.extend(['--task', name])

            method = self.taskData.get('method')
            if method:
                args.extend(['--method', method])

            sources = [i for i in self.taskData.get('sources', [])]
            if sources:
                args.extend(sources)

            p = multiprocessing.Process(target=worker, args=(args, indexscript))
            p.start()
        else:
            QtGui.QMessageBox.warning(None, "Warning",
                u"""Скрипт index не задан!
Задать директорию скрипта можно с помощью команды:"
main.py --setindexscript DIR""")


    def OnDelete(self):
        # !!!
        mark_task_deleted(self.taskData)


# Сервисные функции


    # Восстанавливаем состояние окна
    def loadDialogSettings(self):
        if self.settings:
            self.restoreGeometry(self.settings.value("geometry_settings"))
#           self.restoreState(self.settings.value("windowState_settings"))


    # Сохраняем состояние окна
    def saveDialogSettings(self):
        if self.settings:
            self.settings.setValue("geometry_settings", self.saveGeometry())
#           self.settings.setValue("windowState_settings", self.saveState())


    def may_change(self, value):
        if isinstance(value, (int, float, basestring)):
            return True


    def is_changed(self, value1, value2):
        type1 = unicode if isinstance(value1, basestring) else type(value1)
        type2 = type(value2)

        if type1 != type2:
            try:
                value2 = type1(value2)
            except:
                print(u"Не могу конвертировать {} в тип {}".format(value2, type1))
                return

        if value1 != value2:
            return True



# Form implementation

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 300)

        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")

        ###

        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.proceedButton = QtGui.QPushButton(Dialog)
        self.proceedButton.setObjectName("proceedButton")
        self.verticalLayout.addWidget(self.proceedButton)
        self.methodButton = QtGui.QPushButton(Dialog)
        self.methodButton.setObjectName("methodButton")
        self.verticalLayout.addWidget(self.methodButton)
        self.sourcesButton = QtGui.QPushButton(Dialog)
        self.sourcesButton.setObjectName("sourcesButton")
        self.verticalLayout.addWidget(self.sourcesButton)
        self.deleteButton = QtGui.QPushButton(Dialog)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QObject.connect(self.sourcesButton, QtCore.SIGNAL("clicked()"), Dialog.OnViewSources)
        QtCore.QObject.connect(self.proceedButton, QtCore.SIGNAL("clicked()"), Dialog.OnProceed)
        QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL("clicked()"), Dialog.OnDelete)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.proceedButton.setText(QtGui.QApplication.translate("Dialog", "Proceed", None, QtGui.QApplication.UnicodeUTF8))
        self.methodButton.setText(QtGui.QApplication.translate("Dialog", "Select Method", None, QtGui.QApplication.UnicodeUTF8))
        self.sourcesButton.setText(QtGui.QApplication.translate("Dialog", "View sources", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("Dialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
