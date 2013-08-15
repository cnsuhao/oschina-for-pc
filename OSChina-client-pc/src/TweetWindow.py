#! /usr/bin/env python  
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from bs4 import BeautifulSoup
import httplib2
import AppProperty
import Utils

class TweetWindow(QWidget):
    def __init__(self):  
        super(TweetWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Popup|Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.resize(550,520)
        point = Utils.getDesktopCenterPoint(self)
        self.move(point["x"],point["y"])
        self.webview = QWebView(self)
        self.webview.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.webview.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        self.webview.settings().setLocalStoragePath(AppProperty.HomeDir+"/data")
        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.settings().setDefaultTextEncoding("utf-8")
        self.webview.setGeometry(1,1,self.width()-2,self.height()-2)
        self.webview.page().mainFrame().javaScriptWindowObjectCleared.connect(self.setJavaScriptObject)
        self.webview.setStyleSheet("QWebView{background-color: rgba(255, 193, 245, 0%); }")
        self.webview.page().networkAccessManager().setCookieJar(AppProperty.CookieJar)
        self.webview.load(QUrl.fromLocalFile(AppProperty.HomeDir+"/html/tweetWindow.html"))
        
    def setJavaScriptObject(self):
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_window_", self)
        #self.webview.page().mainFrame().addToJavaScriptWindowObject("_service_", self._service_)
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_notifications_", AppProperty._notifications_)
          
    @pyqtSignature("")
    def quit(self):
        self.close()
    
    @pyqtSignature("int,int")
    def moveTo(self,offsetX,offsetY):
        self.move(self.x()+offsetX,self.y()+offsetY)
    
    @pyqtSignature("",result="QString")
    def loadHtml(self):
        if AppProperty.NewTweetHtml!="":
            return AppProperty.NewTweetHtml
        #过滤html
        soup = BeautifulSoup(AppProperty.HomeSpaceHtml)
        for el in soup.findAll("div",id=("OSC_Banner","OSC_Topbar","OSC_Footer","topcontrol","SpaceLeft","SpaceRight","TopBlogs","Logs")):
            el.extract()
        soup.find("meta").insert_before(soup.new_tag("base", href="http://my.oschina.net"))
        soup.find("div",id="OSC_Screen")["style"] = "width:538px;padding:0px;margin-bootom:0px;"
        soup.find("div",id="SpaceMain")["style"] = "margin:0px;"
        soup.find("div",id="OSC_Content")["style"] = "margin:0px;"
        soup.body["style"]="background:none;"
        soup.head.style.string = soup.head.style.string +'''
        div{-webkit-user-select: none;}
        #MyTweetForm{
            background:none;
            padding:10px;
            border:0px;
        }
        ''' 
        ssoup = str(soup).replace("今天你动弹了吗？", "&nbsp;")
        ssoup = ssoup[0:ssoup.find("//插入新日志")] +"parent.tweetSuccess();"+ ssoup[ssoup.find("var before_upload_image = function(event){")-180:]
        AppProperty.NewTweetHtml = ssoup
        return ssoup
