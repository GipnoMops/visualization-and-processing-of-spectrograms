# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Asus\Desktop\kursach\error_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ErrorWindow(object):
    def setupUi(self, ErrorWindow):
        ErrorWindow.setObjectName("ErrorWindow")
        self.centralwidget = QtWidgets.QWidget(ErrorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.error_btn = QtWidgets.QPushButton(self.centralwidget)
        self.error_btn.setObjectName("error_btn")
        self.error_btn.clicked.connect(ErrorWindow.close)
        self.verticalLayout.addWidget(self.error_btn)
        ErrorWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ErrorWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 202, 26))
        self.menubar.setObjectName("menubar")
        ErrorWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ErrorWindow)
        self.statusbar.setObjectName("statusbar")
        ErrorWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ErrorWindow)
        QtCore.QMetaObject.connectSlotsByName(ErrorWindow)

    def retranslateUi(self, ErrorWindow):
        _translate = QtCore.QCoreApplication.translate
        ErrorWindow.setWindowTitle(_translate("ErrorWindow", "MainWindow"))
        self.label.setText(_translate("ErrorWindow", "Сначала нужно выбрать файл"))
        self.error_btn.setText(_translate("ErrorWindow", "OK"))
