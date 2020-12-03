# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
import sys
from signup import auto_sign
from everyday_autusignup import everyday_auto_signup


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(300, 300)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.btn_print = QtWidgets.QPushButton(self.centralwidget)
        self.btn_print.setGeometry(QtCore.QRect(100, 50, 100, 30))
        self.btn_print.setObjectName("btn_print")
        self.btn_print.setText("打卡")
        self.btn_print.clicked.connect(self.JLU_auto_sign)

        self.btn_autosignup = QtWidgets.QPushButton(self.centralwidget)
        self.btn_autosignup.setGeometry(QtCore.QRect(100, 180, 100, 30))
        self.btn_autosignup.setObjectName("btn_auto_signup")
        self.btn_autosignup.setText("后台自动打卡")
        self.btn_autosignup.clicked.connect(self.JLU_back_auto_sign)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 23))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.sign_thread = self.SignThread()
        self.back_auto_signup_thread = self.BackAutoThread()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "一键打卡"))

    def JLU_auto_sign(self):
        self.sign_thread.start()

    def JLU_back_auto_sign(self):
        self.back_auto_signup_thread.start()

    class SignThread(QThread):

        def __init__(self):
            super(QThread, self).__init__()

        def run(self):
            auto_sign()

    class BackAutoThread(QThread):
        def __init__(self):
            super(QThread, self).__init__()

        def run(self):
            everyday_auto_signup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
    sys.exit(app.exec_())
