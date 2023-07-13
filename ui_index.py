# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'index.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ip = QLineEdit(Form)
        self.ip.setObjectName(u"ip")

        self.horizontalLayout.addWidget(self.ip)

        self.port = QLineEdit(Form)
        self.port.setObjectName(u"port")

        self.horizontalLayout.addWidget(self.port)

        self.startService = QPushButton(Form)
        self.startService.setObjectName(u"startService")

        self.horizontalLayout.addWidget(self.startService)

        self.horizontalLayout.setStretch(0, 6)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.startService.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb", None))
    # retranslateUi

