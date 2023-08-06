# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainvuxNbK.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainDis(object):
    def setupUi(self, MainDis):
        if MainDis.objectName():
            MainDis.setObjectName(u"MainDis")
        MainDis.resize(434, 273)
        MainDis.setStyleSheet(u"font: 12pt \"Tahoma\";\n"
"border-color: rgb(85, 255, 0);")
        self.centralwidget = QWidget(MainDis)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 421, 261))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridFrame = QFrame(self.horizontalLayoutWidget)
        self.gridFrame.setObjectName(u"gridFrame")
        self.gridFrame.setFrameShape(QFrame.Box)
        self.gridFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.gridFrame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_3.setHorizontalSpacing(10)
        self.gridLayout_3.setVerticalSpacing(0)
        self.label_6 = QLabel(self.gridFrame)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)

        self.MainMain = QVBoxLayout()
        self.MainMain.setSpacing(0)
        self.MainMain.setObjectName(u"MainMain")
        self.MainMain.setSizeConstraint(QLayout.SetFixedSize)
        self.btnMain = QPushButton(self.gridFrame)
        self.btnMain.setObjectName(u"btnMain")

        self.MainMain.addWidget(self.btnMain)

        self.btnChart = QPushButton(self.gridFrame)
        self.btnChart.setObjectName(u"btnChart")

        self.MainMain.addWidget(self.btnChart)

        self.btnUpdate = QPushButton(self.gridFrame)
        self.btnUpdate.setObjectName(u"btnUpdate")

        self.MainMain.addWidget(self.btnUpdate)

        self.btnExit = QPushButton(self.gridFrame)
        self.btnExit.setObjectName(u"btnExit")

        self.MainMain.addWidget(self.btnExit)


        self.gridLayout_3.addLayout(self.MainMain, 1, 2, 1, 1)

        self.label_5 = QLabel(self.gridFrame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lbuplimit2 = QLabel(self.gridFrame)
        self.lbuplimit2.setObjectName(u"lbuplimit2")

        self.horizontalLayout_4.addWidget(self.lbuplimit2)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.lbvalue_2 = QLabel(self.gridFrame)
        self.lbvalue_2.setObjectName(u"lbvalue_2")
        font = QFont()
        font.setFamily(u"Tahoma")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbvalue_2.setFont(font)
        self.lbvalue_2.setStyleSheet(u"color: rgb(115, 185, 255); padding: 0px; background-color: none;")
        self.lbvalue_2.setAlignment(Qt.AlignCenter)
        self.lbvalue_2.setIndent(-1)

        self.gridLayout.addWidget(self.lbvalue_2, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lbDlimit2 = QLabel(self.gridFrame)
        self.lbDlimit2.setObjectName(u"lbDlimit2")

        self.horizontalLayout_5.addWidget(self.lbDlimit2)


        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cb2 = QComboBox(self.gridFrame)
        self.cb2.setObjectName(u"cb2")
        self.cb2.setStyleSheet(u"background-color: rgrgb(85, 255, 255);\n"
"border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255), stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92), stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));\n"
"\n"
"")

        self.verticalLayout.addWidget(self.cb2)

        self.btnKetNoi_2 = QPushButton(self.gridFrame)
        self.btnKetNoi_2.setObjectName(u"btnKetNoi_2")

        self.verticalLayout.addWidget(self.btnKetNoi_2)

        self.btnThoat_2 = QPushButton(self.gridFrame)
        self.btnThoat_2.setObjectName(u"btnThoat_2")

        self.verticalLayout.addWidget(self.btnThoat_2)


        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.lbTime = QLabel(self.gridFrame)
        self.lbTime.setObjectName(u"lbTime")

        self.gridLayout_3.addWidget(self.lbTime, 2, 0, 1, 2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lbuplimit1 = QLabel(self.gridFrame)
        self.lbuplimit1.setObjectName(u"lbuplimit1")

        self.horizontalLayout_2.addWidget(self.lbuplimit1)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.lbvalue = QLabel(self.gridFrame)
        self.lbvalue.setObjectName(u"lbvalue")
        self.lbvalue.setFont(font)
        self.lbvalue.setStyleSheet(u"color: rgb(115, 185, 255); padding: 0px; background-color: none;")
        self.lbvalue.setAlignment(Qt.AlignCenter)
        self.lbvalue.setIndent(-1)

        self.gridLayout_2.addWidget(self.lbvalue, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.lbDlimit1 = QLabel(self.gridFrame)
        self.lbDlimit1.setObjectName(u"lbDlimit1")

        self.horizontalLayout.addWidget(self.lbDlimit1)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.cb1 = QComboBox(self.gridFrame)
        self.cb1.setObjectName(u"cb1")
        self.cb1.setStyleSheet(u"background-color: rgrgb(85, 255, 255);\n"
"border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255), stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92), stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));\n"
"\n"
"")

        self.verticalLayout_3.addWidget(self.cb1)

        self.btnKetNoi = QPushButton(self.gridFrame)
        self.btnKetNoi.setObjectName(u"btnKetNoi")

        self.verticalLayout_3.addWidget(self.btnKetNoi)

        self.btnThoat = QPushButton(self.gridFrame)
        self.btnThoat.setObjectName(u"btnThoat")

        self.verticalLayout_3.addWidget(self.btnThoat)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 3, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 1, 1, 1)

        self.lbsoluong = QLabel(self.gridFrame)
        self.lbsoluong.setObjectName(u"lbsoluong")

        self.gridLayout_3.addWidget(self.lbsoluong, 0, 2, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 12)
        self.gridLayout_3.setColumnStretch(1, 12)
        self.gridLayout_3.setColumnStretch(2, 5)
        self.gridLayout_3.setColumnMinimumWidth(0, 12)
        self.gridLayout_3.setColumnMinimumWidth(1, 12)
        self.gridLayout_3.setColumnMinimumWidth(2, 12)

        self.horizontalLayout_3.addWidget(self.gridFrame)

        MainDis.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainDis)

        QMetaObject.connectSlotsByName(MainDis)
    # setupUi

    def retranslateUi(self, MainDis):
        MainDis.setWindowTitle(QCoreApplication.translate("MainDis", u"MainWindow", None))
        self.label_6.setText(QCoreApplication.translate("MainDis", u"Th\u01b0\u1edbc 1", None))
        self.btnMain.setText(QCoreApplication.translate("MainDis", u"Main", None))
        self.btnChart.setText(QCoreApplication.translate("MainDis", u"Chart", None))
        self.btnUpdate.setText(QCoreApplication.translate("MainDis", u"Update", None))
        self.btnExit.setText(QCoreApplication.translate("MainDis", u"Exit", None))
        self.label_5.setText(QCoreApplication.translate("MainDis", u"Th\u01b0\u1edbc 2", None))
        self.lbuplimit2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue_2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">0.000</span></p></body></html>", None))
        self.lbDlimit2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.cb2.setCurrentText("")
        self.btnKetNoi_2.setText(QCoreApplication.translate("MainDis", u"K\u1ebft N\u1ed1i", None))
        self.btnThoat_2.setText(QCoreApplication.translate("MainDis", u"Reset K\u1ebft N\u1ed1i", None))
        self.lbTime.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffffff;\">...</span></p></body></html>", None))
        self.lbuplimit1.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">0.000</span></p></body></html>", None))
        self.lbDlimit1.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.cb1.setCurrentText("")
        self.btnKetNoi.setText(QCoreApplication.translate("MainDis", u"K\u1ebft N\u1ed1i", None))
        self.btnThoat.setText(QCoreApplication.translate("MainDis", u"Reset K\u1ebft N\u1ed1i", None))
        self.lbsoluong.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" color:#0000ff;\">...</span></p></body></html>", None))
    # retranslateUi

