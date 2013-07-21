# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\opt\home\index\desktop\mainframe\dialog_settings_test.ui'
#
# Created: Fri Mar 15 20:31:28 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.line1LineEdit = QtGui.QLineEdit(Dialog)
        self.line1LineEdit.setObjectName("line1LineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.line1LineEdit)
        self.line2Label = QtGui.QLabel(Dialog)
        self.line2Label.setObjectName("line2Label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.line2Label)
        self.line2LineEdit = QtGui.QLineEdit(Dialog)
        self.line2LineEdit.setObjectName("line2LineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.line2LineEdit)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.line_2)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.line)
        self.line1Label = QtGui.QLabel(Dialog)
        self.line1Label.setObjectName("line1Label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.line1Label)
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
        self.line2Label.setText(QtGui.QApplication.translate("Dialog", "Line2", None, QtGui.QApplication.UnicodeUTF8))
        self.line1Label.setText(QtGui.QApplication.translate("Dialog", "Line1", None, QtGui.QApplication.UnicodeUTF8))
        self.proceedButton.setText(QtGui.QApplication.translate("Dialog", "Proceed", None, QtGui.QApplication.UnicodeUTF8))
        self.methodButton.setText(QtGui.QApplication.translate("Dialog", "Select Method", None, QtGui.QApplication.UnicodeUTF8))
        self.sourcesButton.setText(QtGui.QApplication.translate("Dialog", "View sources", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("Dialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))

