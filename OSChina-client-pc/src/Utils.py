#! /usr/bin/env python  
# -*- coding: utf-8 -*-
from PyQt4.QtGui import QSystemTrayIcon,QApplication,QAction,QIcon,QMenu

#根据字符串，获得QT的托盘图标
def getQtTrayIconFromString(str):
    if(str=="info"):
        return QSystemTrayIcon.Information
    if(str=="warn"):
        return QSystemTrayIcon.Warning
    if(str=="error"):
        return QSystemTrayIcon.Critical
    return QSystemTrayIcon.NoIcon