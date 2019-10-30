import serial, os, time
arduino = serial.Serial(port='COM3', baudrate=9600)
rawString = arduino.readline().decode('utf-8')
print (rawString)
arduino.close()