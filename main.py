# -*- encoding=utf-8 -*-

from ui.ui_instance import *
import sys
import os

g_path = ["db",
          "svm",
          "pic"]

def create_dirs():
    for i in range(len(g_path)):
        if not os.path.exists(g_path[i]):
            os.makedirs(g_path[i])

def Start():
    create_dirs()
    app = QApplication(sys.argv)
    mytable = UIFrame()
    mytable.show()
    app.exec_()

Start()