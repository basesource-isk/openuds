# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setup-dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UdsActorSetupDialog(object):
    def setupUi(self, UdsActorSetupDialog):
        UdsActorSetupDialog.setObjectName("UdsActorSetupDialog")
        UdsActorSetupDialog.setWindowModality(QtCore.Qt.WindowModal)
        UdsActorSetupDialog.resize(590, 307)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UdsActorSetupDialog.sizePolicy().hasHeightForWidth())
        UdsActorSetupDialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        UdsActorSetupDialog.setFont(font)
        UdsActorSetupDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/uds-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UdsActorSetupDialog.setWindowIcon(icon)
        UdsActorSetupDialog.setAutoFillBackground(False)
        UdsActorSetupDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        UdsActorSetupDialog.setSizeGripEnabled(False)
        UdsActorSetupDialog.setModal(True)
        self.registerButton = QtWidgets.QPushButton(UdsActorSetupDialog)
        self.registerButton.setEnabled(False)
        self.registerButton.setGeometry(QtCore.QRect(10, 270, 181, 23))
        self.registerButton.setMinimumSize(QtCore.QSize(181, 0))
        self.registerButton.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.registerButton.setObjectName("registerButton")
        self.closeButton = QtWidgets.QPushButton(UdsActorSetupDialog)
        self.closeButton.setGeometry(QtCore.QRect(410, 270, 171, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy)
        self.closeButton.setMinimumSize(QtCore.QSize(171, 0))
        self.closeButton.setObjectName("closeButton")
        self.tabWidget = QtWidgets.QTabWidget(UdsActorSetupDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 571, 241))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_uds = QtWidgets.QWidget()
        self.tab_uds.setObjectName("tab_uds")
        self.layoutWidget = QtWidgets.QWidget(self.tab_uds)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 551, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(16)
        self.formLayout.setObjectName("formLayout")
        self.label_host = QtWidgets.QLabel(self.layoutWidget)
        self.label_host.setObjectName("label_host")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_host)
        self.host = QtWidgets.QLineEdit(self.layoutWidget)
        self.host.setAcceptDrops(False)
        self.host.setObjectName("host")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.host)
        self.label_auth = QtWidgets.QLabel(self.layoutWidget)
        self.label_auth.setObjectName("label_auth")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_auth)
        self.authenticators = QtWidgets.QComboBox(self.layoutWidget)
        self.authenticators.setObjectName("authenticators")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.authenticators)
        self.label_username = QtWidgets.QLabel(self.layoutWidget)
        self.label_username.setObjectName("label_username")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_username)
        self.username = QtWidgets.QLineEdit(self.layoutWidget)
        self.username.setObjectName("username")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.username)
        self.label_password = QtWidgets.QLabel(self.layoutWidget)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.password = QtWidgets.QLineEdit(self.layoutWidget)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.password)
        self.validateCertificate = QtWidgets.QComboBox(self.layoutWidget)
        self.validateCertificate.setObjectName("validateCertificate")
        self.validateCertificate.addItem("")
        self.validateCertificate.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.validateCertificate)
        self.label_security = QtWidgets.QLabel(self.layoutWidget)
        self.label_security.setObjectName("label_security")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_security)
        self.label_host.raise_()
        self.host.raise_()
        self.label_auth.raise_()
        self.label_username.raise_()
        self.username.raise_()
        self.label_password.raise_()
        self.password.raise_()
        self.validateCertificate.raise_()
        self.label_security.raise_()
        self.authenticators.raise_()
        self.tabWidget.addTab(self.tab_uds, "")
        self.tab_advanced = QtWidgets.QWidget()
        self.tab_advanced.setObjectName("tab_advanced")
        self.layoutWidget_2 = QtWidgets.QWidget(self.tab_advanced)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 10, 551, 161))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget_2)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setVerticalSpacing(16)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_host_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_host_2.setObjectName("label_host_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_host_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.preCommand = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.preCommand.setAcceptDrops(False)
        self.preCommand.setWhatsThis("")
        self.preCommand.setObjectName("preCommand")
        self.horizontalLayout.addWidget(self.preCommand)
        self.browsePreconnectButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.browsePreconnectButton.setAutoDefault(False)
        self.browsePreconnectButton.setFlat(False)
        self.browsePreconnectButton.setObjectName("browsePreconnectButton")
        self.horizontalLayout.addWidget(self.browsePreconnectButton)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_username_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_username_2.setObjectName("label_username_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_username_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.runonceCommand = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.runonceCommand.setWhatsThis("")
        self.runonceCommand.setObjectName("runonceCommand")
        self.horizontalLayout_2.addWidget(self.runonceCommand)
        self.browseRunOnceButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.browseRunOnceButton.setAutoDefault(False)
        self.browseRunOnceButton.setObjectName("browseRunOnceButton")
        self.horizontalLayout_2.addWidget(self.browseRunOnceButton)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_password_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_password_2.setObjectName("label_password_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_password_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.postConfigCommand = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.postConfigCommand.setWhatsThis("")
        self.postConfigCommand.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.postConfigCommand.setObjectName("postConfigCommand")
        self.horizontalLayout_3.addWidget(self.postConfigCommand)
        self.browsePostConfigButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.browsePostConfigButton.setAutoDefault(False)
        self.browsePostConfigButton.setObjectName("browsePostConfigButton")
        self.horizontalLayout_3.addWidget(self.browsePostConfigButton)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_loglevel = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_loglevel.setObjectName("label_loglevel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_loglevel)
        self.logLevelComboBox = QtWidgets.QComboBox(self.layoutWidget_2)
        self.logLevelComboBox.setFrame(True)
        self.logLevelComboBox.setObjectName("logLevelComboBox")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.setItemText(0, "DEBUG")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.setItemText(1, "INFO")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.setItemText(2, "ERROR")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.setItemText(3, "FATAL")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.logLevelComboBox)
        self.tabWidget.addTab(self.tab_advanced, "")
        self.testButton = QtWidgets.QPushButton(UdsActorSetupDialog)
        self.testButton.setEnabled(False)
        self.testButton.setGeometry(QtCore.QRect(210, 270, 181, 23))
        self.testButton.setMinimumSize(QtCore.QSize(181, 0))
        self.testButton.setObjectName("testButton")

        self.retranslateUi(UdsActorSetupDialog)
        self.tabWidget.setCurrentIndex(0)
        self.logLevelComboBox.setCurrentIndex(1)
        self.closeButton.clicked.connect(UdsActorSetupDialog.finish)
        self.registerButton.clicked.connect(UdsActorSetupDialog.registerWithUDS)
        self.host.textChanged['QString'].connect(UdsActorSetupDialog.textChanged)
        self.username.textChanged['QString'].connect(UdsActorSetupDialog.textChanged)
        self.password.textChanged['QString'].connect(UdsActorSetupDialog.textChanged)
        self.browsePreconnectButton.clicked.connect(UdsActorSetupDialog.browsePreconnect)
        self.browsePostConfigButton.clicked.connect(UdsActorSetupDialog.browsePostConfig)
        self.browseRunOnceButton.clicked.connect(UdsActorSetupDialog.browseRunOnce)
        self.host.editingFinished.connect(UdsActorSetupDialog.updateAuthenticators)
        self.authenticators.currentTextChanged['QString'].connect(UdsActorSetupDialog.textChanged)
        self.testButton.clicked.connect(UdsActorSetupDialog.testUDSServer)
        QtCore.QMetaObject.connectSlotsByName(UdsActorSetupDialog)

    def retranslateUi(self, UdsActorSetupDialog):
        _translate = QtCore.QCoreApplication.translate
        UdsActorSetupDialog.setWindowTitle(_translate("UdsActorSetupDialog", "UDS Actor Configuration Tool"))
        self.registerButton.setToolTip(_translate("UdsActorSetupDialog", "Click to register Actor with UDS Broker"))
        self.registerButton.setWhatsThis(_translate("UdsActorSetupDialog", "<html><head/><body><p>Click on this button to register Actor with UDS Broker.</p></body></html>"))
        self.registerButton.setText(_translate("UdsActorSetupDialog", "Register with UDS"))
        self.closeButton.setToolTip(_translate("UdsActorSetupDialog", "Closes UDS Actor Configuration (discard pending changes if any)"))
        self.closeButton.setWhatsThis(_translate("UdsActorSetupDialog", "<html><head/><body><p>Exits the UDS Actor Configuration Tool</p></body></html>"))
        self.closeButton.setText(_translate("UdsActorSetupDialog", "Close"))
        self.label_host.setText(_translate("UdsActorSetupDialog", "UDS Server"))
        self.host.setToolTip(_translate("UdsActorSetupDialog", "Uds Broker Server Addres. Use IP or FQDN"))
        self.host.setWhatsThis(_translate("UdsActorSetupDialog", "Enter here the UDS Broker Addres using either its IP address or its FQDN address"))
        self.label_auth.setText(_translate("UdsActorSetupDialog", "Authenticator"))
        self.authenticators.setWhatsThis(_translate("UdsActorSetupDialog", "<html><head/><body><p>Select the UDS Broker authenticator for credentials validation</p></body></html>"))
        self.label_username.setText(_translate("UdsActorSetupDialog", "Username"))
        self.username.setToolTip(_translate("UdsActorSetupDialog", "UDS user with administration rights (Will not be stored on template)"))
        self.username.setWhatsThis(_translate("UdsActorSetupDialog", "<html><head/><body><p>Administrator user on UDS Server.</p><p>Note: This credential will not be stored on client. Will be used to obtain an unique token for this image.</p></body></html>"))
        self.label_password.setText(_translate("UdsActorSetupDialog", "Password"))
        self.password.setToolTip(_translate("UdsActorSetupDialog", "Password for user (Will not be stored on template)"))
        self.password.setWhatsThis(_translate("UdsActorSetupDialog", "<html><head/><body><p>Administrator password for the user on UDS Server.</p><p>Note: This credential will not be stored on client. Will be used to obtain an unique key for this image.</p></body></html>"))
        self.validateCertificate.setToolTip(_translate("UdsActorSetupDialog", "Select communication security with broker"))
        self.validateCertificate.setWhatsThis(_translate("UdsActorSetupDialog", "<html><head/><body><p>Select the security for communications with UDS Broker.</p><p>The recommended method of communication is <span style=\" font-weight:600;\">Use SSL</span>, but selection needs to be acording to your broker configuration.</p></body></html>"))
        self.validateCertificate.setItemText(0, _translate("UdsActorSetupDialog", "Ignore certificate"))
        self.validateCertificate.setItemText(1, _translate("UdsActorSetupDialog", "Verify certificate"))
        self.label_security.setText(_translate("UdsActorSetupDialog", "SSL Validation"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_uds), _translate("UdsActorSetupDialog", "UDS Server"))
        self.label_host_2.setText(_translate("UdsActorSetupDialog", "Preconnect"))
        self.preCommand.setToolTip(_translate("UdsActorSetupDialog", "Pre connection command. Executed just before the user is connected to machine."))
        self.browsePreconnectButton.setText(_translate("UdsActorSetupDialog", "Browse"))
        self.label_username_2.setText(_translate("UdsActorSetupDialog", "Runonce"))
        self.runonceCommand.setToolTip(_translate("UdsActorSetupDialog", "Run once command. Executed on first boot, just before UDS does anything."))
        self.browseRunOnceButton.setText(_translate("UdsActorSetupDialog", "Browse"))
        self.label_password_2.setText(_translate("UdsActorSetupDialog", "Postconfig"))
        self.postConfigCommand.setToolTip(_translate("UdsActorSetupDialog", "Command to execute after UDS finalizes the VM configuration."))
        self.browsePostConfigButton.setText(_translate("UdsActorSetupDialog", "Browse"))
        self.label_loglevel.setText(_translate("UdsActorSetupDialog", "Log Level"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_advanced), _translate("UdsActorSetupDialog", "Advanced"))
        self.testButton.setToolTip(_translate("UdsActorSetupDialog", "Click to test existing configuration (disabled if no config found)"))
        self.testButton.setWhatsThis(_translate("UdsActorSetupDialog", "<html><head/><body><p>Click on this button to test the server host and assigned toen.</p></body></html>"))
        self.testButton.setText(_translate("UdsActorSetupDialog", "Test configuration"))
from ui import uds_rc