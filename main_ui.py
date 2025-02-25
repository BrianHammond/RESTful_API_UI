# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(794, 645)
        icon = QIcon()
        icon.addFile(u":/images/ms_icon.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about_qt = QAction(MainWindow)
        self.action_about_qt.setObjectName(u"action_about_qt")
        self.action_dark_mode = QAction(MainWindow)
        self.action_dark_mode.setObjectName(u"action_dark_mode")
        self.action_dark_mode.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.line_server = QLineEdit(self.groupBox_2)
        self.line_server.setObjectName(u"line_server")

        self.verticalLayout.addWidget(self.line_server)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.line_firstname = QLineEdit(self.groupBox)
        self.line_firstname.setObjectName(u"line_firstname")

        self.horizontalLayout.addWidget(self.line_firstname)

        self.line_middlename = QLineEdit(self.groupBox)
        self.line_middlename.setObjectName(u"line_middlename")

        self.horizontalLayout.addWidget(self.line_middlename)

        self.line_lastname = QLineEdit(self.groupBox)
        self.line_lastname.setObjectName(u"line_lastname")

        self.horizontalLayout.addWidget(self.line_lastname)

        self.line_age = QLineEdit(self.groupBox)
        self.line_age.setObjectName(u"line_age")

        self.horizontalLayout.addWidget(self.line_age)

        self.line_title = QLineEdit(self.groupBox)
        self.line_title.setObjectName(u"line_title")

        self.horizontalLayout.addWidget(self.line_title)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.line_misc = QLineEdit(self.groupBox)
        self.line_misc.setObjectName(u"line_misc")

        self.gridLayout.addWidget(self.line_misc, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.line_address1 = QLineEdit(self.groupBox)
        self.line_address1.setObjectName(u"line_address1")

        self.horizontalLayout_2.addWidget(self.line_address1)

        self.line_address2 = QLineEdit(self.groupBox)
        self.line_address2.setObjectName(u"line_address2")

        self.horizontalLayout_2.addWidget(self.line_address2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.button_post = QPushButton(self.centralwidget)
        self.button_post.setObjectName(u"button_post")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_post.sizePolicy().hasHeightForWidth())
        self.button_post.setSizePolicy(sizePolicy)
        self.button_post.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_post)

        self.button_get = QPushButton(self.centralwidget)
        self.button_get.setObjectName(u"button_get")
        sizePolicy.setHeightForWidth(self.button_get.sizePolicy().hasHeightForWidth())
        self.button_get.setSizePolicy(sizePolicy)
        self.button_get.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_get)

        self.button_put = QPushButton(self.centralwidget)
        self.button_put.setObjectName(u"button_put")
        sizePolicy.setHeightForWidth(self.button_put.sizePolicy().hasHeightForWidth())
        self.button_put.setSizePolicy(sizePolicy)
        self.button_put.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_put)

        self.button_delete = QPushButton(self.centralwidget)
        self.button_delete.setObjectName(u"button_delete")
        sizePolicy.setHeightForWidth(self.button_delete.sizePolicy().hasHeightForWidth())
        self.button_delete.setSizePolicy(sizePolicy)
        self.button_delete.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_delete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.table = QTableWidget(self.centralwidget)
        self.table.setObjectName(u"table")
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.table)

        self.label_connection = QLabel(self.centralwidget)
        self.label_connection.setObjectName(u"label_connection")

        self.verticalLayout_2.addWidget(self.label_connection)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 794, 22))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_server, self.line_firstname)
        QWidget.setTabOrder(self.line_firstname, self.line_middlename)
        QWidget.setTabOrder(self.line_middlename, self.line_lastname)
        QWidget.setTabOrder(self.line_lastname, self.line_age)
        QWidget.setTabOrder(self.line_age, self.line_title)
        QWidget.setTabOrder(self.line_title, self.line_address1)
        QWidget.setTabOrder(self.line_address1, self.line_address2)
        QWidget.setTabOrder(self.line_address2, self.line_misc)
        QWidget.setTabOrder(self.line_misc, self.button_post)
        QWidget.setTabOrder(self.button_post, self.button_get)
        QWidget.setTabOrder(self.button_get, self.button_put)
        QWidget.setTabOrder(self.button_put, self.button_delete)
        QWidget.setTabOrder(self.button_delete, self.table)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menuHelp.addAction(self.action_about_qt)
        self.menuSettings.addAction(self.action_dark_mode)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RESTful API Tester", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_about_qt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.action_dark_mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Server Info", None))
        self.line_server.setPlaceholderText(QCoreApplication.translate("MainWindow", u"server ip:port", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Employee Information", None))
        self.line_firstname.setPlaceholderText(QCoreApplication.translate("MainWindow", u"First Name", None))
        self.line_middlename.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Middle Name", None))
        self.line_lastname.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Last Name", None))
        self.line_age.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Age", None))
        self.line_title.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.line_misc.setText("")
        self.line_misc.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Misc Info", None))
        self.line_address1.setText("")
        self.line_address1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Address 1", None))
        self.line_address2.setText("")
        self.line_address2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Address 2", None))
#if QT_CONFIG(tooltip)
        self.button_post.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.button_post.setStatusTip(QCoreApplication.translate("MainWindow", u"Send Info", None))
#endif // QT_CONFIG(statustip)
        self.button_post.setText(QCoreApplication.translate("MainWindow", u"Post", None))
#if QT_CONFIG(statustip)
        self.button_get.setStatusTip(QCoreApplication.translate("MainWindow", u"Get Info", None))
#endif // QT_CONFIG(statustip)
        self.button_get.setText(QCoreApplication.translate("MainWindow", u"Get", None))
#if QT_CONFIG(statustip)
        self.button_put.setStatusTip(QCoreApplication.translate("MainWindow", u"Update Info", None))
#endif // QT_CONFIG(statustip)
        self.button_put.setText(QCoreApplication.translate("MainWindow", u"Put", None))
#if QT_CONFIG(statustip)
        self.button_delete.setStatusTip(QCoreApplication.translate("MainWindow", u"Delete Info", None))
#endif // QT_CONFIG(statustip)
        self.button_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label_connection.setText(QCoreApplication.translate("MainWindow", u"FlaskAPI Connection Status Label", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

