######################## IMPORTS ########################
from pygame.locals import *
from tkinter import *
from datetime import date
from datetime import datetime
#import datetime
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
        today = datetime.now()
        day = str(format(today.day))
        month = str(format(today.month))
        year = str(format(today.year))
        hour = str(format(today.hour))
        minute = str(format(today.minute))
        second = str(format(today.second))

        dateNow = year +'-'+ month +'-'+ day +'T'+ hour +':'+ minute +':'+ second
        print('AQUI'+dateNow)
        d = datetime.strptime(dateNow, "%Y-%m-%dT%H:%M:%S") 
        print('TAMBIEN AQUI'+str(d))
        self.db.CO2.insert_one({'valor': self.CO2, 'fecha': d})
        self.db.TVOC.insert_one({'valor': self.TVOC, 'fecha': d})
        self.db.humidity.insert_one({'valor': self.humidity, 'fecha': d})
        self.db.temperature.insert_one({'valor': self.temperature, 'fecha': d})

    def startThread(self):
        self.Thread = threading.Thread(target=self.runThread)
        self.Thread.start()


    def arduinoConnect(self):
        # Iniciando conexión serial
        self.arduinoPort = serial.Serial('COM3', 9600)
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

def button(msg,x,y,w,h,ic,ac, gameDisplay, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        #pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        AAfilledRoundedRect(gameDisplay, (x,y,w,h), ac, 0.25)


        if click[0] == 1 and action != None:
            action()         
    else:
        #pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
        AAfilledRoundedRect(gameDisplay, (x,y,w,h), ic, 0.25)

    smallText = pygame.font.SysFont("comicsansms",round(w*0.15))
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

def WindowPygame():
    pygame.init()

    # Crear ventana
    window = pygame.display.set_mode((1000, 600))
    # Titulo de la ventana
    pygame.display.set_caption("Sensors")


    #Crear clase Interfaz
    sensor = Sensor()
    #sensor.arduinoConnect()
    sensor.mongoConnect()
    #sensor.startThread()


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
                #sensor.arduinoDisconnect()
                #sensor.threadStop()
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

        blue = (7, 88, 230)
        light_blue = (47, 128, 255)

        button("Conectar", 800, 100, 120, 40, blue, light_blue, window, sensor.arduinoConnect)
        button("Desconectar", 800, 300, 120, 40, blue, light_blue, window, sensor.arduinoDisconnect)

        #AAfilledRoundedRect(window,(50,50,200,50),(200,20,20),0.5)

        pygame.display.update()


if __name__ == '__main__':
    Window()
