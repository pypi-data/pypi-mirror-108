# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_grab_from_clipboard = QAction(MainWindow)
        self.action_grab_from_clipboard.setObjectName(u"action_grab_from_clipboard")
        icon = QIcon(QIcon.fromTheme(u"edit-copy"))
        self.action_grab_from_clipboard.setIcon(icon)
        self.action_screenshot = QAction(MainWindow)
        self.action_screenshot.setObjectName(u"action_screenshot")
        icon1 = QIcon(QIcon.fromTheme(u"monitor"))
        self.action_screenshot.setIcon(icon1)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        icon2 = QIcon(QIcon.fromTheme(u"document-open"))
        self.action_open.setIcon(icon2)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.graphics_view = QGraphicsView(self.central_widget)
        self.graphics_view.setObjectName(u"graphics_view")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphics_view.sizePolicy().hasHeightForWidth())
        self.graphics_view.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.graphics_view)

        self.text_edit = QTextEdit(self.central_widget)
        self.text_edit.setObjectName(u"text_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.text_edit.sizePolicy().hasHeightForWidth())
        self.text_edit.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.text_edit)

        MainWindow.setCentralWidget(self.central_widget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_grab_from_clipboard)
        self.toolBar.addAction(self.action_screenshot)
        self.toolBar.addAction(self.action_open)

        self.retranslateUi(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Text Grab", None))
        self.action_grab_from_clipboard.setText(QCoreApplication.translate("MainWindow", u"Grab From Clipboard", None))
#if QT_CONFIG(shortcut)
        self.action_grab_from_clipboard.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.action_screenshot.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
#if QT_CONFIG(shortcut)
        self.action_screenshot.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.action_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

