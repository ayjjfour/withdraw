# -*- encoding=utf-8 -*-

from ui.ui_instance import *
import sys

def Start():
    app = QApplication(sys.argv)
    mytable = UIFrame()
    mytable.show()
    app.exec_()

Start()