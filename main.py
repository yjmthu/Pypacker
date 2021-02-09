# -*- coding: utf-8 -*-
# @Date    : 2021-02-06 23:34:01
# @Author  : Megix Wiley (yjmthu@gmail.com)
# @Link    : https://github.com/Wiley2046
# @Version : 3.5

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt
import sys, os, ctypes

from myWindow import Qmywindow

Path = Path = os.path.dirname(os.path.realpath(sys.argv[0])) + '\\' + 'Wait.runfile'
if not os.path.exists(Path):
    File = open(Path, 'w')
    File.close()
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    while True:
        app = QApplication(sys.argv)
        form = Qmywindow()
        form.show()
        exitCode = app.exec_()
        if exitCode == 9420233:
            del form
            del app
        else:
            break
    os.remove(Path)
    if exitCode == 2339420:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
else:
    pass
