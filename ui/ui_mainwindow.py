# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowview.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QSizePolicy, QStatusBar, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1421, 600)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSync = QAction(MainWindow)
        self.actionSync.setObjectName(u"actionSync")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.callsignEdit = QLineEdit(self.widget_2)
        self.callsignEdit.setObjectName(u"callsignEdit")

        self.horizontalLayout_2.addWidget(self.callsignEdit)

        self.txRxSelect = QComboBox(self.widget_2)
        self.txRxSelect.addItem("")
        self.txRxSelect.addItem("")
        self.txRxSelect.setObjectName(u"txRxSelect")
        self.txRxSelect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.txRxSelect)


        self.verticalLayout.addWidget(self.widget_2)

        self.signalTableView = QTableView(self.widget)
        self.signalTableView.setObjectName(u"signalTableView")

        self.verticalLayout.addWidget(self.signalTableView)


        self.horizontalLayout.addWidget(self.widget)

        self.relayPathTextView = QPlainTextEdit(self.centralwidget)
        self.relayPathTextView.setObjectName(u"relayPathTextView")
        font = QFont()
        font.setFamilies([u"Source Code Pro"])
        self.relayPathTextView.setFont(font)
        self.relayPathTextView.setReadOnly(True)

        self.horizontalLayout.addWidget(self.relayPathTextView)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1421, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuData = QMenu(self.menubar)
        self.menuData.setObjectName(u"menuData")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuData.addAction(self.actionSync)
        self.menuAbout.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.txRxSelect.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"IEGMRS ERC", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionSync.setText(QCoreApplication.translate("MainWindow", u"Sync...", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.callsignEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Callsign...", None))
        self.txRxSelect.setItemText(0, QCoreApplication.translate("MainWindow", u"TX", None))
        self.txRxSelect.setItemText(1, QCoreApplication.translate("MainWindow", u"RX", None))

        self.txRxSelect.setCurrentText(QCoreApplication.translate("MainWindow", u"TX", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"Data", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"Other", None))
    # retranslateUi

