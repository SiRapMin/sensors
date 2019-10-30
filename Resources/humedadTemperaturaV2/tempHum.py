#Importante
#Este proyecto esta elaborado sobre Python 3.7
import time
import serial

# Iniciando conexión serial
arduinoPort = serial.Serial('COM3', 9600)
#Esperamos a que el arduino se reinicie correctamente
time.sleep(0.1)
#Verificamos que el puerto este abierto
print(arduinoPort.is_open)


while (10):
    valorSerial = arduinoPort.readline().decode(encoding='UTF-8',errors='strict')
    print('Valor serial: '+valorSerial)

arduinoPort.close()
