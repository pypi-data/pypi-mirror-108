# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainduSgYO.ui'
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
        MainDis.resize(445, 288)
        MainDis.setStyleSheet(u"font: 12pt \"Tahoma\";\n"
"border-color: rgb(85, 255, 0);\n"
"background-color: rgb(170, 154, 72);")
        self.centralwidget = QWidget(MainDis)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(230, 30, 211, 221))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_4.addWidget(self.pushButton_3)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.lbvalue_2 = QLabel(self.layoutWidget)
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
        self.pushButton_4 = QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)


        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cb2 = QComboBox(self.layoutWidget)
        self.cb2.setObjectName(u"cb2")
        self.cb2.setStyleSheet(u"background-color: rgrgb(85, 255, 255);\n"
"border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255), stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92), stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));\n"
"\n"
"")

        self.verticalLayout.addWidget(self.cb2)

        self.btnKetNoi_2 = QPushButton(self.layoutWidget)
        self.btnKetNoi_2.setObjectName(u"btnKetNoi_2")

        self.verticalLayout.addWidget(self.btnKetNoi_2)

        self.btnThoat_2 = QPushButton(self.layoutWidget)
        self.btnThoat_2.setObjectName(u"btnThoat_2")

        self.verticalLayout.addWidget(self.btnThoat_2)


        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 10, 61, 19))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(230, 10, 61, 19))
        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 30, 211, 221))
        self.gridLayout_2 = QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.lbvalue = QLabel(self.layoutWidget1)
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
        self.pushButton_2 = QPushButton(self.layoutWidget1)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.cb1 = QComboBox(self.layoutWidget1)
        self.cb1.setObjectName(u"cb1")
        self.cb1.setStyleSheet(u"background-color: rgrgb(85, 255, 255);\n"
"border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255), stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92), stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));\n"
"\n"
"")

        self.verticalLayout_3.addWidget(self.cb1)

        self.btnKetNoi = QPushButton(self.layoutWidget1)
        self.btnKetNoi.setObjectName(u"btnKetNoi")

        self.verticalLayout_3.addWidget(self.btnKetNoi)

        self.btnThoat = QPushButton(self.layoutWidget1)
        self.btnThoat.setObjectName(u"btnThoat")

        self.verticalLayout_3.addWidget(self.btnThoat)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 3, 0, 1, 1)

        self.lbTime = QLabel(self.centralwidget)
        self.lbTime.setObjectName(u"lbTime")
        self.lbTime.setGeometry(QRect(10, 260, 431, 20))
        MainDis.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainDis)

        QMetaObject.connectSlotsByName(MainDis)
    # setupUi

    def retranslateUi(self, MainDis):
        MainDis.setWindowTitle(QCoreApplication.translate("MainDis", u"MainWindow", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainDis", u"Get DL", None))
        self.label_3.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue_2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">0.000</span></p></body></html>", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainDis", u"Get CL", None))
        self.label_4.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.cb2.setCurrentText("")
        self.btnKetNoi_2.setText(QCoreApplication.translate("MainDis", u"K\u1ebft N\u1ed1i", None))
        self.btnThoat_2.setText(QCoreApplication.translate("MainDis", u"Reset K\u1ebft N\u1ed1i", None))
        self.label_5.setText(QCoreApplication.translate("MainDis", u"Th\u01b0\u1edbc 1", None))
        self.label_6.setText(QCoreApplication.translate("MainDis", u"Th\u01b0\u1edbc 2", None))
        self.pushButton.setText(QCoreApplication.translate("MainDis", u"Get DL", None))
        self.label.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">0.000</span></p></body></html>", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainDis", u"Get CL", None))
        self.label_2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.cb1.setCurrentText("")
        self.btnKetNoi.setText(QCoreApplication.translate("MainDis", u"K\u1ebft N\u1ed1i", None))
        self.btnThoat.setText(QCoreApplication.translate("MainDis", u"Reset K\u1ebft N\u1ed1i", None))
        self.lbTime.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffffff;\">...</span></p></body></html>", None))
    # retranslateUi

