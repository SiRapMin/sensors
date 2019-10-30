# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(496, 203)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label.setObjectName("label")
        self.Actualizar = QtWidgets.QPushButton(self.centralwidget)
        self.Actualizar.setGeometry(QtCore.QRect(10, 140, 331, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Actualizar.setFont(font)
        self.Actualizar.setDefault(False)
        self.Actualizar.setObjectName("Actualizar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 10, 61, 31))
        self.label_2.setObjectName("label_2")
        self.humedad = QtWidgets.QProgressBar(self.centralwidget)
        self.humedad.setGeometry(QtCore.QRect(20, 40, 151, 23))
        self.humedad.setProperty("value", 24)
        self.humedad.setObjectName("humedad")
        self.temperatura = QtWidgets.QLabel(self.centralwidget)
        self.temperatura.setGeometry(QtCore.QRect(200, 30, 91, 41))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(16)
        self.temperatura.setFont(font)
        self.temperatura.setObjectName("temperatura")
        self.conectar = QtWidgets.QPushButton(self.centralwidget)
        self.conectar.setGeometry(QtCore.QRect(380, 70, 75, 23))
        self.conectar.setObjectName("conectar")
        self.desconectar = QtWidgets.QPushButton(self.centralwidget)
        self.desconectar.setGeometry(QtCore.QRect(380, 100, 75, 23))
        self.desconectar.setObjectName("desconectar")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(370, 40, 101, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(190, 80, 47, 13))
        self.label_5.setObjectName("label_5")
        self.CO2 = QtWidgets.QLabel(self.centralwidget)
        self.CO2.setGeometry(QtCore.QRect(20, 102, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.CO2.setFont(font)
        self.CO2.setObjectName("CO2")
        self.TVOC = QtWidgets.QLabel(self.centralwidget)
        self.TVOC.setGeometry(QtCore.QRect(190, 100, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.TVOC.setFont(font)
        self.TVOC.setObjectName("TVOC")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(343, 0, 20, 161))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 496, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Humedad:"))
        self.Actualizar.setText(_translate("MainWindow", "Actualizar"))
        self.label_2.setText(_translate("MainWindow", "Temperatura"))
        self.temperatura.setText(_translate("MainWindow", "0"))
        self.conectar.setText(_translate("MainWindow", "Conectar"))
        self.desconectar.setText(_translate("MainWindow", "Desconectar"))
        self.label_3.setText(_translate("MainWindow", "Conexion Arduino"))
        self.label_4.setText(_translate("MainWindow", "CO2"))
        self.label_5.setText(_translate("MainWindow", "TVOC"))
        self.CO2.setText(_translate("MainWindow", "0"))
        self.TVOC.setText(_translate("MainWindow", "0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
