# -*- encoding=utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from uiframe import *
from routine.run import *
import Queue
    
version = 'V1.0.0.1'
    
class UIFrame(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(UIFrame,self).__init__(parent)
        self.setupUi(self)
        self.queue = Queue.Queue(20)
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.setFixedSize(self.width(), self.height())
        
        #设置窗口标题
        self.setWindowTitle(u"现金提取系统  %s" % version)

        #设置选择属性
        self.m_tbl_user.setSelectionBehavior(QAbstractItemView.SelectRows)

        #添加表头：
        self.model = QtGui.QStandardItemModel(self.m_tbl_user)

        #设置表格属性：
        self.model.setRowCount(0)
        self.model.setColumnCount(5)

        self.model.setHeaderData(0,QtCore.Qt.Horizontal,u"用户名称")
        self.model.setHeaderData(1,QtCore.Qt.Horizontal,u"登录密码")
        self.model.setHeaderData(2,QtCore.Qt.Horizontal,u"二级密码")
        self.model.setHeaderData(3,QtCore.Qt.Horizontal,u"执行状态")
        self.model.setHeaderData(4,QtCore.Qt.Horizontal,u"状态码")
        self.m_tbl_user.setModel(self.model)
 
        #设置列宽
        self.m_tbl_user.setColumnWidth(0, 60)
        self.m_tbl_user.setColumnWidth(1, 60)
        self.m_tbl_user.setColumnWidth(2, 60)
        self.m_tbl_user.setColumnWidth(3, 160)
        self.m_tbl_user.setColumnWidth(4, 50)
        
        self.run = Run(self, self.queue)
        
        self.connect(self.run, SIGNAL("SIG_load_data()"), self.slot_load_data)
        self.connect(self.run, SIGNAL("SIG_update_state(QString, int)"), self.slot_update_state)
        self.connect(self.run, SIGNAL("SIG_add_log(QString)"), self.slot_add_log)
        self.connect(self.run, SIGNAL("SIG_set_button_enable(bool)"), self.slot_set_button_enable)
        self.connect(self.m_tbl_user, SIGNAL("doubleClicked(QModelIndex)"), self.edit_table_item)
                
        self.run.start()
        
        self._load_user_info()
        
    def __del__(self):
        self.queue.put(["stop"], False)
        self.run.thread_stop = True
        
    def _set_button_enable(self, flag):
        self.m_btn_add.setEnabled(flag)
        self.m_btn_delet.setEnabled(flag)
        self.m_btn_save.setEnabled(flag)
        self.m_btn_reset.setEnabled(flag)
        self.m_btn_start.setEnabled(flag)
        #self.m_tbl_user.setEnabled(flag)
        if False == flag:
            print "no trigger", QAbstractItemView.NoEditTriggers
            self.m_tbl_user.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        else:
            print "trigger", QAbstractItemView.DoubleClicked
            self.m_tbl_user.setEditTriggers(QAbstractItemView.DoubleClicked)
        
    def _load_user_info(self):
        self.queue.put(["load"], False)
        
    def edit_table_item(self):
        self.m_btn_reset.setEnabled(False)
        self.m_btn_start.setEnabled(False)

    def user_state_reset(self):
        self.queue.put(["reset", -9999], False)
        rowcount = self.model.rowCount()
        for i in range(rowcount):
            self.model.setItem(i, 3, QtGui.QStandardItem(self.run.error_msg[-9999]))
            self.model.item(i, 3).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            self.model.setItem(i, 4, QtGui.QStandardItem("%s" % -9999))
        return
    
    def fetch_money_start(self):
        self.queue.put(["start"], block = True, timeout = None)
        self._set_button_enable(False)
        return
    
    def fetch_money_stop(self):
        self.run.routine_stop = True
    
    def add_user_info(self):
        list_of_QStandardItem = []
        list_of_QStandardItem.append(QtGui.QStandardItem(''))
        list_of_QStandardItem.append(QtGui.QStandardItem('555666'))
        list_of_QStandardItem.append(QtGui.QStandardItem('888999'))
        item = QtGui.QStandardItem(self.run.error_msg[-9999])
        item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        list_of_QStandardItem.append(item)
        list_of_QStandardItem.append(QtGui.QStandardItem('-9999'))
        
        self.model.appendRow(list_of_QStandardItem)
        self.m_btn_reset.setEnabled(False)
        self.m_btn_start.setEnabled(False)
    
    def save_user_info(self):
        #self.queue.put(["save"], block=True, timeout=None)
        list_info = []
        local_dicinfo = {}
        rowcount = self.model.rowCount()
        for i in range(rowcount):
            info = []
            nickname = unicode(self.model.item(i, 0).text(), 'utf-8', 'ignore').strip()
            passwd = unicode(self.model.item(i, 1).text(), 'utf-8', 'ignore').strip()
            secondpwd = unicode(self.model.item(i, 2).text(), 'utf-8', 'ignore').strip()
            errcode = unicode(self.model.item(i, 4).text(), 'utf-8', 'ignore').strip()
            if nickname == '':                      #用户名为空
                QMessageBox.critical(self, u"保存", u'列表中不能存在空的用户名!')
                return
            
            if local_dicinfo.has_key(nickname):      #用户名重复了
                QMessageBox.critical(self, u"保存", u"用户名[%s]已经存在了!" % nickname)
                return
            
            local_dicinfo[nickname] = i
            info.append(nickname)
            info.append(passwd)
            info.append(secondpwd)
            info.append(int(errcode))
            list_info.append(info)
            
        self.dicinfo = local_dicinfo
        self.queue.put(["save", list_info], block = True, timeout = None)
        self.m_btn_reset.setEnabled(True)
        self.m_btn_start.setEnabled(True)
                
        return
    
    def delete_user_info(self):
        index = self.m_tbl_user.selectedIndexes()
        if 0 >= len(index):
            QMessageBox.critical(self, u"删除", u'请选中要删除的记录!')
            return
            
        rows = []
        for i in range(len(index)):
            print "index[i].column = ", index[i].column(), index[i].row()
            if index[i].column() == 0:
                rows.append(index[i].row())
                
        rows.sort()
        rows.reverse()
        print "rows = ", rows
                
        for i in range(len(rows)):
            self.model.removeRow(rows[i])
        
        self.m_btn_reset.setEnabled(False)
        self.m_btn_start.setEnabled(False)
            
        return
    
    ############## slot #############
    def slot_load_data(self):
        list_info = self.run.list_info
        self.dicinfo = {}   # key = nickname, value = rownumber
        print "slot_load_data", list_info
        
        for i in range(len(list_info)):
            row = list_info[i]
            self.dicinfo[list_info[i][0]] = i
            for j in range(len(row)):
                
                if j == (len(row) - 1):
                    if self.run.error_msg.has_key(row[j]):
                        self.model.setItem(i,j,QtGui.QStandardItem(self.run.error_msg[row[j]]))
                        if row[j] < 0:
                            self.model.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                        else:
                            self.model.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
                    else:
                        row[j] = -9999
                        self.model.setItem(i,j,QtGui.QStandardItem(u"未知"))
                        
                    self.model.setItem(i,j+1,QtGui.QStandardItem("%d" % row[j]))
                else:
                    self.model.setItem(i,j,QtGui.QStandardItem(row[j]))
                        
    def slot_update_state(self, nickname, state):
        #print "slot_update_state ", nickname, state
        keystr = unicode(nickname.toUtf8(), 'utf-8', 'ignore')
        index = self.dicinfo[keystr]
        if self.run.error_msg.has_key(state):
            self.model.setItem(index, 3, QtGui.QStandardItem(self.run.error_msg[state]))
            if state < 0:
                self.model.item(index, 3).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            else:
                self.model.item(index, 3).setForeground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
        else:
            self.model.setItem(index, 3, QtGui.QStandardItem(u"未知"))
        self.model.setItem(index, 4, QtGui.QStandardItem("%d" % state))
                    
    def slot_add_log(self, log):
        #print "slot_add_log ", log
        pystr = unicode(log.toUtf8(), 'utf-8', 'ignore')
        self.m_txt_log.append(pystr)
        
    def slot_set_button_enable(self, flag):
        self._set_button_enable(flag)
        
    