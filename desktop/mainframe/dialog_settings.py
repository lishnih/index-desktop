#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-08

from PySide import QtCore, QtGui


# from dialog_settings_test_ui import Ui_Dialog
from dialog_sources import Sources

from lib.backwardcompat import *
from task_item import redraw, proceed_task


class Settings(QtGui.QDialog):
    def __init__(self, parent, child, settings=None, s=None):
        super(Settings, self).__init__(parent)
        self.parent = parent
        self.child = child
        self.settings = settings
#       self.s = s

        # Загружаем элементы диалога
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Восстанавливаем состояние окна
        self.loadDialogSettings()

        # Добавляем виджеты
        Dialog = self
        formLayout = self.ui.formLayout

        i = 0
        for key in sorted(self.child.taskData.keys()):
            value = self.child.taskData.get(key)
            tt = str(type(value)).replace('<', '&lt;').replace('>', '&gt;')
            text = u'{0}<br/><span style="color:#aaaaaa;">{1}</span>'.format(key, tt)
            label = QtGui.QLabel(text, Dialog)
#           label.setFrameStyle(QtGui.QFrame.Panel)
#           label.setLineWidth(1)
#           formLayout.setWidget(i, QtGui.QFormLayout.LabelRole, label)

            lineEdit = QtGui.QLineEdit(unicode(value), Dialog)
            lineEdit.setObjectName("le_{0}".format(key))
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
        if self.child.isHidden():
            self.child.close()
        else:
            for key, value in self.child.taskData.items():
                if self.may_change(value):
                    le = self.findChild(QtGui.QLineEdit, "le_{0}".format(key))
                    le_value = le.text()
                    if self.is_changed(self.child.taskData.get(key), le_value):
                        self.child.taskData[key] = le_value

            redraw(self.child)

        self.saveDialogSettings()
        self.done(True)


    def reject(self):
        if self.child.isHidden():
            self.child.show()

        redraw(self.child)

        self.saveDialogSettings()
        self.done(False)


    def closeEvent(self, event):
        self.reject()


    def OnViewSources(self):
        dialog = Sources(self.parent, self.child.taskData, self.window().settings)
        res = dialog.exec_()


    def OnProceed(self):
        proceed_task(self.child.taskData)


    def OnDelete(self):
        self.child.hide()


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
        if isinstance(value, simple_types):
            return True


    def is_changed(self, value1, value2):
        type1 = unicode if isinstance(value1, basestring) else type(value1)
        type2 = type(value2)

        if type1 != type2:
            try:
                value2 = type1(value2)
            except:
                print(u"Не могу конвертировать {0} в тип {1}".format(value2, type1))
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
