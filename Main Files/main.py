date######################## IMPORTS ########################
from pygame.locals import *
from tkinter import *
from datetime import date
from datetime import datetime
from pymongo import MongoClient
import matplotlib.backends.backend_agg as agg
import easygui as eg
import pygame
import sys
import threading
import time
import serial
import pylab
import matplotlib
matplotlib.use("Agg")

######################## CLASS ########################

class Sensor():
    def __init__(self):

        #Se inicializan las variables que guardan los datos de los sensores
        self.humiditylist = []
        self.humidity = 0
        self.temperaturelist = []
        self.temperature = 0
        self.CO2list = []
        self.CO2 = 0
        self.TVOClist = []
        self.TVOC = 0

        self.stop = False

        self.graphicHum = None
        self.canvas1 = None
        self.graphicCO2 = None
        self.canvas2 = None
        self.graphicTemp = None
        self.canvas3 = None
        self.graphicTVOC = None
        self.canvas4 = None
        self.db = None

######################## METHODS ########################
    def mongoConnect(self):
        con = MongoClient('localhost', 27017)
        self.db = con.sensors

    def uploadDataMongoDb(self):
        date = str(datetime.now())
        self.db.CO2.insert_one({'value': self.CO2, 'date': date})
        self.db.TVOC.insert_one({'value': self.TVOC, 'date': date})
        self.db.humidity.insert_one({'value': self.humidity, 'date': date})
        self.db.temperature.insert_one({'value': self.temperature, 'date': date})

    def startThread(self):
        self.Thread = threading.Thread(target=self.runThread)
        self.Thread.start()


    def arduinoConnect(self):
        # Iniciando conexión serial
        self.arduinoPort = serial.Serial('COM5', 9600)
        # Esperamos a que el arduino se reinicie correctamente
        time.sleep(2)

    def arduinoDisconnect(self):
        self.arduinoPort.close()

    def threadStop(self):
        if(self.Thread.is_alive()):
            self.stop = True

    def runThread(self):
        #Verificamos que el puerto este abierto
        while (self.arduinoPort.is_open and self.stop == False):
            self.getArduinoData()
            self.uploadDataMongoDb()

    def getArduinoData(self):
        # En el siguiente orden llega la información por el puerto
        # CO2
        self.CO2 = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
        self.CO2list.append(self.CO2)
        print('Value CO2: ' + str(round(self.CO2)))
        # TVOC
        self.TVOC = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
        self.TVOClist.append(self.TVOC)
        print('Valor TVOC: ' + str(self.TVOC))
        # humidity
        self.humidity = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
        print('Humidity Value: ' + str(round(self.humidity)))
        self.humiditylist.append(self.humidity)
        # temperature
        self.temperature = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
        print('Temperature Value: ' + str(self.temperature))
        self.temperaturelist.append(self.temperature)
        self.generateMatplot()
        time.sleep(1)


    def generateMatplot(self):
        width = 3
        height = 2
        dpi = 120
        #Generar la grafica de la humidity
        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        ax.plot(self.humiditylist)
        self.canvas1 = agg.FigureCanvasAgg(fig)
        self.canvas1.draw()
        renderer = self.canvas1.get_renderer()
        self.graphicHum = renderer.tostring_rgb()

        #Generar la grafica del CO2

        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        ax.plot(self.CO2list)
        self.canvas2 = agg.FigureCanvasAgg(fig)
        self.canvas2.draw()
        renderer = self.canvas2.get_renderer()
        self.graphicCO2 = renderer.tostring_rgb()

        # Generar la grafica de la temperature

        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        ax.plot(self.temperaturelist)
        self.canvas3 = agg.FigureCanvasAgg(fig)
        self.canvas3.draw()
        renderer = self.canvas3.get_renderer()
        self.graphicTemp = renderer.tostring_rgb()
        # Generar la grafica del TVOC

        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        ax.plot(self.TVOClist)
        self.canvas4 = agg.FigureCanvasAgg(fig)
        self.canvas4.draw()
        renderer = self.canvas4.get_renderer()
        self.graphicTVOC = renderer.tostring_rgb()

######################## PYGAME METHOD ########################
def Window():
    pygame.init()

    # Crear ventana
    window = pygame.display.set_mode((1000, 600))
    # Titulo de la ventana
    pygame.display.set_caption("Sensors")


    #Crear clase Interfaz
    sensor = Sensor()
    sensor.arduinoConnect()
    sensor.mongoConnect()
    sensor.startThread()


    myFont = pygame.font.Font(None, 30)

    dimensionx = 30
    dimensiony = 30
    distancex = 500
    distancey = 250
    while True:
        window.fill((255,255,255))
        humidity = myFont.render("humidity: "+str(sensor.humidity)+"%", 0,(0,0,0))
        CO2 = myFont.render("CO2: "+str(sensor.CO2)+" ppm", 0,(0,0,0))
        Temp = myFont.render("temperature: "+str(sensor.temperature)+"°C", 0,(0,0,0))
        TVOC = myFont.render("TVOC: "+str(sensor.TVOC)+" mg/m3", 0,(0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sensor.arduinoDisconnect()
                sensor.threadStop()
                sys.exit()
        if(sensor.graphicHum != None and
                sensor.canvas1 != None and
                sensor.graphicCO2 != None and
                sensor.canvas2 != None and
                sensor.graphicTVOC != None and
                sensor.canvas3 != None and
                sensor.graphicTemp!= None and
                sensor.canvas4 != None):

            surf = pygame.image.fromstring(sensor.graphicHum, sensor.canvas1.get_width_height(), "RGB")
            window.blit(surf,(dimensionx,dimensiony))
            surf = pygame.image.fromstring(sensor.graphicCO2, sensor.canvas2.get_width_height(), "RGB")
            window.blit(surf, (dimensionx, dimensiony+distancey))
            surf = pygame.image.fromstring(sensor.graphicTemp, sensor.canvas2.get_width_height(), "RGB")
            window.blit(surf, (dimensionx+distancex, dimensiony))
            surf = pygame.image.fromstring(sensor.graphicTVOC, sensor.canvas2.get_width_height(), "RGB")
            window.blit(surf, (dimensionx+distancex, dimensiony + distancey))

        window.blit(humidity,(dimensionx,dimensiony))
        window.blit(CO2, (dimensionx, dimensiony+distancey))
        window.blit(Temp, (dimensionx+distancex, dimensiony))
        window.blit(TVOC, (dimensionx+distancex, dimensiony+distancey))

        pygame.display.update()


if __name__ == '__main__':
    Window()