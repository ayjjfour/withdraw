# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiframe.ui'
#
# Created: Mon Mar 27 10:39:42 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(989, 615)
        self.m_txt_log = QtGui.QTextBrowser(Dialog)
        self.m_txt_log.setGeometry(QtCore.QRect(375, 61, 611, 551))
        self.m_txt_log.setObjectName(_fromUtf8("m_txt_log"))
        self.m_lab_user = QtGui.QLabel(Dialog)
        self.m_lab_user.setGeometry(QtCore.QRect(10, 40, 54, 12))
        self.m_lab_user.setObjectName(_fromUtf8("m_lab_user"))
        self.m_lab_log = QtGui.QLabel(Dialog)
        self.m_lab_log.setGeometry(QtCore.QRect(380, 40, 54, 12))
        self.m_lab_log.setObjectName(_fromUtf8("m_lab_log"))
        self.m_btn_save = QtGui.QPushButton(Dialog)
        self.m_btn_save.setGeometry(QtCore.QRect(80, 10, 75, 23))
        self.m_btn_save.setObjectName(_fromUtf8("m_btn_save"))
        self.m_btn_delet = QtGui.QPushButton(Dialog)
        self.m_btn_delet.setGeometry(QtCore.QRect(210, 10, 75, 23))
        self.m_btn_delet.setObjectName(_fromUtf8("m_btn_delet"))
        self.m_tbl_user = QtGui.QTableView(Dialog)
        self.m_tbl_user.setGeometry(QtCore.QRect(5, 61, 361, 551))
        self.m_tbl_user.setObjectName(_fromUtf8("m_tbl_user"))
        self.m_btn_reset = QtGui.QPushButton(Dialog)
        self.m_btn_reset.setGeometry(QtCore.QRect(530, 10, 75, 23))
        self.m_btn_reset.setObjectName(_fromUtf8("m_btn_reset"))
        self.m_btn_start = QtGui.QPushButton(Dialog)
        self.m_btn_start.setGeometry(QtCore.QRect(740, 10, 75, 23))
        self.m_btn_start.setObjectName(_fromUtf8("m_btn_start"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.m_btn_reset, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.user_state_reset)
        QtCore.QObject.connect(self.m_btn_start, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.fetch_money_start)
        QtCore.QObject.connect(self.m_btn_save, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.save_user_info)
        QtCore.QObject.connect(self.m_btn_delet, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.delete_user_info)
        QtCore.QObject.connect(self.m_tbl_user, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), self.m_tbl_user.edit)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.m_lab_user.setText(_translate("Dialog", "用户列表：", None))
        self.m_lab_log.setText(_translate("Dialog", "运行日志：", None))
        self.m_btn_save.setText(_translate("Dialog", "保存", None))
        self.m_btn_delet.setText(_translate("Dialog", "删除", None))
        self.m_btn_reset.setText(_translate("Dialog", "重置", None))
        self.m_btn_start.setText(_translate("Dialog", "开始", None))

