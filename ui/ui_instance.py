# -*- encoding=utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from uiframe import *
from routine.run import *
import Queue
    
class UIFrame(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(UIFrame,self).__init__(parent)
        self.setupUi(self)
        self.queue = Queue.Queue(20)

        #添加表头：
        self.model = QtGui.QStandardItemModel(self.m_tbl_user)

        #设置表格属性：
        self.model.setRowCount(0)
        self.model.setColumnCount(4)

        self.model.setHeaderData(0,QtCore.Qt.Horizontal,u"用户名称")
        self.model.setHeaderData(1,QtCore.Qt.Horizontal,u"登录密码")
        self.model.setHeaderData(2,QtCore.Qt.Horizontal,u"二级密码")
        self.model.setHeaderData(3,QtCore.Qt.Horizontal,u"执行状态")
        self.m_tbl_user.setModel(self.model)  
 
        #设置列宽
        self.m_tbl_user.setColumnWidth(0, 60)
        self.m_tbl_user.setColumnWidth(1, 60)
        self.m_tbl_user.setColumnWidth(2, 60)
        self.m_tbl_user.setColumnWidth(3, 160)
        
        self.run = Run(self, self.queue)
        
        self.connect(self.run, SIGNAL("SIG_load_data()"), self.slot_load_data)
        self.connect(self.run, SIGNAL("SIG_update_state(QString, int)"), self.slot_update_state)
        self.connect(self.run, SIGNAL("SIG_add_log(QString)"), self.slot_add_log)
        
        self.run.start()
        
        self._load_user_info()
        
    def _load_user_info(self):
        self.queue.put(["load"])

    def user_state_reset(self):
        self.queue.put(["reset", -9999])
        rowcount = self.model.rowCount()
        for i in range(rowcount):
            self.model.setItem(i, 3, QtGui.QStandardItem(self.run.error_msg[-9999]))
        return
    
    def fetch_money_start(self):
        self.queue.put(["start"], block=True, timeout=None)
        return
    
    def save_user_info(self):
        return
    
    def delete_user_info(self):
        return
    
    ############## slot #############
    def slot_load_data(self):
        list_info = self.run.list_info
        self.dicinfo = {}
        print "slot_load_data", list_info
        
        for i in range(len(list_info)):
            row = list_info[i]
            self.dicinfo[list_info[i][0]] = i
            for j in range(len(row)):
                self.model.setItem(i,j,QtGui.QStandardItem(row[j]))
                if j == (len(row) - 1):
                    if self.run.error_msg.has_key(row[j]):
                        self.model.setItem(i,j,QtGui.QStandardItem(self.run.error_msg[row[j]]))
                    else:
                        row[j] = -9999
                        self.model.setItem(i,j,QtGui.QStandardItem(u"未知"))
                        
    def slot_update_state(self, nickname, state):
        print "slot_update_state ", nickname, state
        keystr = unicode(nickname.toUtf8(), 'utf-8', 'ignore')
        index = self.dicinfo[keystr]
        if self.run.error_msg.has_key(state):
            self.model.setItem(index, 3, QtGui.QStandardItem(self.run.error_msg[state]))
        else:
            self.model.setItem(index, 3, QtGui.QStandardItem(u"未知"))
                    
    def slot_add_log(self, log):
        #print "slot_add_log ", log
        pystr = unicode(log.toUtf8(), 'utf-8', 'ignore')
        self.m_txt_log.append(pystr)
        
    