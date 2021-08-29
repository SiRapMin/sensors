######################## IMPORTS ########################
import threading
import time
from datetime import datetime
import json
import matplotlib
import matplotlib.backends.backend_agg as agg
import pygame
import pylab
import serial
from pygame.locals import *
# import datetime
from pymongo import MongoClient

matplotlib.use("Agg")

######################## CLASS ########################

screen_width = 0
screen_height = 0

class Sensor():
    def __init__(self,puertoSerial):

        #Se inicializan las variables que guardan los datos de los sensores
        self.puertoSerial = puertoSerial
        self.humiditylist = []
        self.humidityAvgList=[]
        self.humidity = 0
        self.ultravioletlist = []
        self.ultravioletAvgList = []
        self.ultraviolet = 0
        self.temperaturelist = []
        self.temperatureAvgList = []
        self.temperature = 0
        self.CO2list = []
        self.CO2AvgList = []
        self.CO2 = 0
        self.TVOClist = []
        self.TVOCAvgList = []
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
        self.graphicUltraViolet = None
        self.canvas5 = None
        self.db = None

######################## METHODS ########################
    def mongoConnect(self):
        try:
            f = open('../mongoCredentials.json')
            data = json.load(f)
        except:
            print("---------------MONGO CREDENTIALS FILE MISSING---------------")

        try:
            client = MongoClient(data["mongoKey"])
            self.db = client.get_database(data["DB_name"])
        except:
            print("---------------------- MONGO DATABASE CONNECTION FAILED -----------------")

    def uploadDataMongoDb(self):
        today = datetime.now()
        day = str(format(today.day))
        month = str(format(today.month))
        year = str(format(today.year))
        hour = str(format(today.hour))
        minute = str(format(today.minute))
        second = str(format(today.second))

        dateNow = year +'-'+ month +'-'+ day +'T'+ hour +':'+ minute +':'+ second
        #print('AQUI'+dateNow)
        d = datetime.strptime(dateNow, "%Y-%m-%dT%H:%M:%S") 
        #print('TAMBIEN AQUI'+str(d))
        self.db.CO2.insert_one({'value': self.CO2, 'date': d})
        self.db.TVOC.insert_one({'value': self.TVOC, 'date': d})
        self.db.humidity.insert_one({'value': self.humidity, 'date': d})
        self.db.temperature.insert_one({'value': self.temperature, 'date': d})
        self.db.ultraviolet.insert_one({'value': self.ultraviolet, 'date': d})

    def startThread(self):
        self.Thread = threading.Thread(target=self.runThread)
        self.Thread.start()


    def arduinoConnect(self):
        # Iniciando conexión serial
        self.arduinoPort = serial.Serial(self.puertoSerial, 9600)
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
        #Based on json
        data = self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict')
        print('json: '+data)
        json_sensors = json.loads(data)
        self.CO2 = float(json_sensors['CO2'])
        self.TVOC = float(json_sensors['TVOC'])
        self.humidity = float(json_sensors['HUM'])
        self.temperature = float(json_sensors['TEMP'])
        self.ultraviolet = float(json_sensors['UV'])
        self.CO2list.append(self.CO2)
        self.TVOClist.append(self.TVOC)
        self.humiditylist.append(self.humidity)
        self.temperaturelist.append(self.temperature)
        self.ultravioletlist.append(self.ultraviolet)
        #Based on sequence
        '''
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
        # temperature
        self.ultraviolet = float(self.arduinoPort.readline().decode(encoding='UTF-8', errors='strict'))
        print('Ultraviolet Value: ' + str(self.ultraviolet))
        self.ultravioletlist.append(self.ultraviolet)
        '''
        self.generateMatplot()
        time.sleep(1)

    def generateMatplot(self):
        global screen_height
        global screen_width
        width = 3.1
        height = (screen_height * 0.00261)
        dpi = 120
        word_graph_size = screen_width*0.004
        #Generar la grafica de la humidity
        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(word_graph_size)
        ax.plot(self.humiditylist)
        self.humidityAvgList.append(self.getAverageFromList(self.humiditylist))
        ax.plot(self.humidityAvgList)
        self.canvas1 = agg.FigureCanvasAgg(fig)
        self.canvas1.draw()
        renderer = self.canvas1.get_renderer()
        self.graphicHum = renderer.tostring_rgb()

        #Generar la grafica del CO2

        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(word_graph_size)
        ax.plot(self.CO2list)

        self.CO2AvgList.append(self.getAverageFromList(self.CO2list))
        ax.plot(self.CO2AvgList)
        self.canvas2 = agg.FigureCanvasAgg(fig)
        self.canvas2.draw()
        renderer = self.canvas2.get_renderer()
        self.graphicCO2 = renderer.tostring_rgb()

        # Generar la grafica de la temperature

        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(word_graph_size)
        ax.plot(self.temperaturelist)
        self.temperatureAvgList.append(self.getAverageFromList(self.temperaturelist))
        ax.plot(self.temperatureAvgList)
        self.canvas3 = agg.FigureCanvasAgg(fig)
        self.canvas3.draw()
        renderer = self.canvas3.get_renderer()
        self.graphicTemp = renderer.tostring_rgb()

        # Generar la grafica del TVOC

        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(word_graph_size)
        ax.plot(self.TVOClist)
        self.TVOCAvgList.append(self.getAverageFromList(self.TVOClist))
        ax.plot(self.TVOCAvgList)
        self.canvas4 = agg.FigureCanvasAgg(fig)
        self.canvas4.draw()
        renderer = self.canvas4.get_renderer()
        self.graphicTVOC = renderer.tostring_rgb()

        # Generar la grafica del ULTRAVIOLET

        fig = pylab.figure(figsize=[width, height],  # Inches
                           dpi=dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(word_graph_size)
        ax.plot(self.ultravioletlist)
        self.ultravioletAvgList.append(self.getAverageFromList(self.ultravioletlist))
        ax.plot(self.ultravioletAvgList)
        self.canvas5 = agg.FigureCanvasAgg(fig)
        self.canvas5.draw()
        renderer = self.canvas5.get_renderer()
        self.graphicUltraViolet = renderer.tostring_rgb()

    def getAverageFromList(self,arrayList):
        acc = 0
        for i in arrayList:
            acc = i + acc
        avg = acc/len(arrayList)
        return avg
        

    def recollectData(sensor):
        print("Conectando")
        sensor.arduinoConnect()
        print("Contectado")
        sensor.mongoConnect()
        sensor.startThread()

    def stopCollectingData(sensor):
        sensor.arduinoDisconnect()
             


def button(msg,x,y,w,h,ic,ac, gameDisplay, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        AAfilledRoundedRect(gameDisplay, (x,y,w,h), ac, 0.25)


        if click[0] == 1 and action != None:
            action()         
    else:
        AAfilledRoundedRect(gameDisplay, (x,y,w,h), ic, 0.25)

    smallText = pygame.font.SysFont("timesnewroman",round(w*0.15))
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


def WindowPygame(puertoSerial):

    if puertoSerial is '':
        return

    pygame.init()
    print(puertoSerial)
    # Crear ventana
    window = pygame.display.set_mode((0, 0))
    global screen_height
    screen_height = pygame.display.Info().current_h
    global screen_width 
    screen_width = pygame.display.Info().current_w
    # Titulo de la ventana
    pygame.display.set_caption("Sensors")


    #Crear clase Interfaz
    sensor = Sensor(puertoSerial)
    #sensor.mongoConnect()
    #sensor.startThread()


    myFont = pygame.font.SysFont("timesnewroman", round(screen_width * 0.02))

    dimensionx = screen_width * 0.02
    dimensiony = screen_height * 0.02
    distancex = screen_width * 0.35
    distancey = screen_height * 0.45
    flag = True
    while flag == True:
        window.fill((255,255,255))
        humidity = myFont.render("Humidity: "+str(sensor.humidity)+"%", 0,(0,0,0))
        CO2 = myFont.render("CO2: "+str(sensor.CO2)+" ppm", 0,(0,0,0))
        Temp = myFont.render("Temperature: "+str(sensor.temperature)+"°C", 0,(0,0,0))
        TVOC = myFont.render("TVOC: "+str(sensor.TVOC)+" mg/m3", 0,(0,0,0))
        ultraViolet = myFont.render("Ultraviolet: " + str(sensor.ultraviolet) + " ???", 0, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                sensor.stop = True
                pygame.quit()
                #sys.exit()
                flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sensor.stop = True
                    pygame.quit()
                    flag = False
            
                
        if(sensor.graphicHum != None and
                sensor.canvas1 != None and
                sensor.graphicCO2 != None and
                sensor.canvas2 != None and
                sensor.graphicTVOC != None and
                sensor.canvas3 != None and
                sensor.graphicTemp!= None and
                sensor.canvas4 != None  and
                sensor.graphicUltraViolet != None and
                sensor.canvas5 != None and
                sensor.stop == False):

            surf = pygame.image.fromstring(sensor.graphicHum, sensor.canvas1.get_width_height(), "RGB")
            window.blit(surf,(dimensionx,dimensiony + 10))
            surf = pygame.image.fromstring(sensor.graphicCO2, sensor.canvas2.get_width_height(), "RGB")
            window.blit(surf, (dimensionx, dimensiony+distancey + 10))
            surf = pygame.image.fromstring(sensor.graphicTemp, sensor.canvas3.get_width_height(), "RGB")
            window.blit(surf, (dimensionx+distancex, dimensiony + 10))
            surf = pygame.image.fromstring(sensor.graphicTVOC, sensor.canvas4.get_width_height(), "RGB")
            window.blit(surf, (dimensionx+distancex, dimensiony + distancey + 10))
            surf = pygame.image.fromstring(sensor.graphicUltraViolet, sensor.canvas5.get_width_height(), "RGB")
            window.blit(surf, (2*distancex, dimensiony + 10))

        if (flag == False):
            continue
        window.blit(humidity,(dimensionx,dimensiony))
        window.blit(CO2, (dimensionx, dimensiony+distancey))
        window.blit(Temp, (dimensionx+distancex, dimensiony))
        window.blit(TVOC, (dimensionx+distancex, dimensiony+distancey))
        window.blit(ultraViolet, (dimensionx + 2*distancex, dimensiony))

        blue = (7, 88, 230)
        light_blue = (47, 128, 255)

        #Arduino Configuration

        window.blit(myFont.render("Configuration ", 0,(0,0,0)), ((screen_width * 0.84), (screen_height * 0.82)))

        button("Conectar", (screen_width * 0.898), (screen_height * 0.8699), (screen_width * 0.08789), (screen_height * 0.052083), blue, light_blue, window, sensor.recollectData)
        button("Desconectar", (screen_width * 0.898), (screen_height * 0.936), (screen_width * 0.08789), (screen_height * 0.052083), blue, light_blue, window, sensor.stopCollectingData)
        


        #AAfilledRoundedRect(window,(50,50,200,50),(200,20,20),0.5)
        pygame.display.update()


if __name__ == '__main__':
    WindowPygame("COM3")
    # client = MongoClient("mongodb+srv://test:test@sensorsdata.lp3o2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.get_database('sensors_DB')
    # records = db.CO2
    # print(records.count_documents({}))
    # today = datetime.now()
    # day = str(format(today.day))
    # month = str(format(today.month))
    # year = str(format(today.year))
    # hour = str(format(today.hour))
    # minute = str(format(today.minute))
    # second = str(format(today.second))
    # dateNow = year +'-'+ month +'-'+ day +'T'+ hour +':'+ minute +':'+ second
    # d = datetime.strptime(dateNow, "%Y-%m-%dT%H:%M:%S") 

    # new_CO2 = {
    #     'value': 5,
    #     'date' : d
    # }

    # records.insert_one(new_CO2)
    # print(records.count_documents({}))
