from PyQt5 import QtCore, QtGui, QtWidgets
from ventana import Ui_MainWindow
# Importante
#  Este proyecto esta elaborado sobre Python 3.7
import time
import serial
import sys
import threading

class sensores:
    def __init__(self):
        self.conarduino = False
        self.humedad = 0
        self.temperatura = 0
        self.CO2 = 0
        self.TVOC = 0
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.acciones()
        self.arduinoPort = None
        MainWindow.show()
        sys.exit(app.exec_())

    def conectarArduino(self):
        # Iniciando conexión serial
        self.arduinoPort = serial.Serial('COM3', 9600)
        # Esperamos a que el arduino se reinicie correctamente
        time.sleep(2)
        self.conarduino = True
        self.iniciarHilo()

    def iniciarHilo(self):
        Hilo = threading.Thread(target=self.correrHilo)
        Hilo.start()

    def correrHilo(self):
        # Verificamos que el puerto este abierto
        while(self.arduinoPort.is_open):
            self.CO2aux = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
            print('Valor CO2: ' + str(round(self.CO2aux)))
            self.TVOCaux = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
            print('Valor TVOC: ' + str(self.TVOCaux))
            self.humedadaux = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
            print('Valor humedad: ' + str(round(self.humedadaux)))
            self.temperaturaaux = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
            print('Valor temperatura: ' + str(self.temperaturaaux))
            #self.actualizarParam()
            time.sleep(1)



    def desconectarArduino(self):
        self.arduinoPort.close()
        self.conarduino = False

    def acciones(self):
        #self.ui.Actualizar.clicked.connect(self.actualizar)
        self.ui.conectar.clicked.connect(self.conectarArduino)
        self.ui.desconectar.clicked.connect(self.desconectarArduino)

    def actualizarParam(self):
        self.ui.CO2.setText(str(self.CO2aux) + "ppm")
        self.ui.TVOC.setText(str(self.TVOCaux) + "mg/m3")
        self.ui.humedad.setValue(round(self.humedadaux))
        self.ui.temperatura.setText(str(self.temperaturaaux)+"°C")

        self.temperatura=self.temperaturaaux
        self.CO2 = self.CO2aux
        self.humedad =self.humedadaux
        self.TVOC = self.TVOCaux

    def actualizar(self):
        self.ui.CO2.setText(str(self.CO2) + "ppm")
        self.ui.TVOC.setText(str(self.TVOC) + "mg/m3")
        self.ui.humedad.setValue(round(self.humedad))
        self.ui.temperatura.setText(str(self.temperatura)+"°C")



if __name__ == "__main__":
    ventanaSensores = sensores()
