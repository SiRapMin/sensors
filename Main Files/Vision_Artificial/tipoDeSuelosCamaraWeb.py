import numpy as np
from PIL import Image
import easygui as eg
import math
import cv2
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
from keras.models import model_from_json
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import img_to_array
import threading
import sys
import tensorflow as tf

ALTITUDE_BASE = 16

def nothing(x):
    pass

############## POSIBLES CLASES ##################
from scipy.stats._multivariate import random_correlation_gen


class VisionArtificial():
    def __init__(self):
        self.ground_preserved = ['Bosque','Forest','Pasto','Pasture']
        self.ground_medium = ['HerbaceousVegetation','PermanentCrop','Vegetación herbácea','Cultivo permanente']
        self.ground_water = ['River','SeaLake','Rio','Mar']
        self.dic_clas = {0: 'AnnualCrop',
                    1: 'Forest',
                    2: 'HerbaceousVegetation',
                    3: 'Highway',
                    4: 'Industrial',
                    5: 'Pasture',
                    6: 'PermanentCrop',
                    7: 'Residential',
                    8: 'River',
                    9: 'SeaLake'}

        self.dic_clas_spanish = {0: 'Cultivos o Sabanas',
                            1: 'Bosque',
                            2: 'Vegetación herbácea',
                            3: 'Autopista',
                            4: 'Industrial',
                            5: 'Pasto',
                            6: 'Cultivo permanente',
                            7: 'Residencial',
                            8: 'Rio',
                            9: 'Mar'}
        '''
        self.dic_clas = {0: 'AnnualCrop',
                    1: 'Forest',
                    2: 'Highway',
                    3: 'Industrial',
                    4: 'Mining',
                    5: 'Pasture',
                    6: 'Residential',
                    7: 'River',
                    8: 'SeaLake'}

        self.dic_clas_spanish = {0: 'Cultivos o Sabanas',
                            1: 'Bosque',
                            2: 'Autopista',
                            3: 'Industrial',
                            4: 'Mineria',
                            5: 'Pasto',
                            6: 'Residencial',
                            7: 'Rio',
                            8: 'Mar'}
        '''
        self.loaded_model = None
        self.loadNeuralNetwork()
        self.WebCamWindow = None
        self.enEjecucion=True

    def loadNeuralNetwork(self):

        # cargar json y crear el modelo
        json_file = open('Vision_Artificial/tipodesuelos.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(loaded_model_json)

        #necesario
        global graph
        graph = tf.get_default_graph()
        global sess
        sess = tf.Session()
        set_session(sess)

        # Cargar pesos al nuevo modelo
        self.loaded_model.load_weights("Vision_Artificial/tipodesuelos.h5")

        #print("Cargado modelo desde disco.")

        #Compilamos el modelo
        self.loaded_model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])


#Elegimos una imagen

    def predictImage(self,altitude):
        extension = ["*.jpg", "*.png"]
        imagen_url = eg.fileopenbox(msg="Abrir archivo",
                                 title="Control: fileopenbox",
                                 default='',
                                 filetypes=extension)

        if imagen_url:
            prediction = self.predict_image_url(imagen_url)
            self.image = threading.Thread(target=self.preview_image_cv, args=(imagen_url,))
            self.image.start()
            return prediction
        return 'None'

    def preview_image_cv(self,imagen_url):
        # Visualizar imagen
        try:
            #print(imagen_url)
            img = cv2.imread(imagen_url,0)
            cv2.imshow("Preview analysis of image", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            print('Imagen de formato no soportado')


    def predict_image_url(self,imagen_url):
        # Guardamos la imagen dentro de nuestro arreglo que sera la entrada de nuestra red neuronal
        image = Image.open(str(imagen_url))
        image_resize = image.resize((64,64))
        im_array = np.array(image_resize, dtype='float32')
        datos_entrada = (np.array([im_array])) / 255
        #print(str(datos_entrada))
        # El modelo predice la entrada y genera un arreglo con la probabilidad de cada clase de imagen
        prob_pred_test = self.loaded_model.predict(datos_entrada)
        #DEPRICATED ->>>prob_pred_test = self.loaded_model._make_predict_function(datos_entrada)
        #print(prob_pred_test)
        # Escogemos la probabilidad mayor y la mostramos
        predicciones_test = [self.dic_clas_spanish[np.argmax(prob)] for prob in prob_pred_test]



        return predicciones_test

    def predictWebCam(self,puertoCamara=None,url_video=None):
        self.video_threading = threading.Thread(target=self.video, args=(puertoCamara,url_video,))
        self.video_threading.start()

    def create_matrix(self,n):
        matrix = []
        for i in range(n):
            matrix.append([])
            for j in range(n):
                matrix[i].append(0)
        #print(matrix)
        return matrix


    def crop_image(self,frame,factor):
        size_image_to_net = 64
        height, width = frame.shape[:2]

        #Recalculate factor
        #print(height,width)
        #print("Factor_before: " + str(factor))
        if factor > height/size_image_to_net:
            factor = math.floor(height/size_image_to_net)
        if factor > width/size_image_to_net:
            factor = math.floor(width/size_image_to_net)
        #print("Factor_after: " + str(factor))

        #Size each image
        height = math.floor(height/factor)
        width = math.floor(width/factor)

        images = self.create_matrix(factor)
        #Getting crop images
        for i in range(factor):
            for j in range(factor):
                #print(str(i*height)+"-"+str((i+1)*height)+"_"+str(j*width)+"-"+str((j+1)*width))
                images[i][j] = frame[i*height:(i+1)*height,j*width:(j+1)*width]
                #cv2.imshow('Crop_image ' + str(i) + '_'+ str(j), frame[i*height:(i+1)*height,j*width:(j+1)*width])
        return images

    def prediction_from_frame(self,frame):
        img_resize = self.resizeImage(frame)
        cv2.imwrite('frame-resize.jpg', img_resize)

        with graph.as_default():
            set_session(sess)
            return self.predict_image_url('frame-resize.jpg')[0]

    def video(self,puertoCamara,url_video):
        if puertoCamara:
            self.WebCamWindow = cv2.VideoCapture(int(puertoCamara))
        elif url_video:
            self.WebCamWindow = cv2.VideoCapture(url_video)
        else:
            return False

        cv2.namedWindow('Video_Prediction')
        cv2.createTrackbar('Altitude','Video_Prediction', 0, 600, nothing)
        while (self.WebCamWindow.isOpened()):
            ret,frame = self.WebCamWindow.read()
            #analysis of image, based on altitude and resolution
            if frame is None:
                break
            cv2.imshow('Test',frame)
            altitude = cv2.getTrackbarPos('Altitude', 'Video_Prediction')
            factor_image = math.floor(altitude/ALTITUDE_BASE)
            if factor_image > 1:
                #crop of frame for video prediction based on factor_image
                images_cropped = self.crop_image(frame=frame,factor=factor_image)
                #print("Images cropped: "+str(len(images_cropped)))
                degrade = 180
                for row in range(len(images_cropped)):
                    for col in range(len(images_cropped)):
                        predictionItem = self.prediction_from_frame(images_cropped[row][col])
                        if predictionItem in self.ground_preserved:
                            images_cropped[row][col][:,:,1] = degrade
                        elif predictionItem in self.ground_medium:
                            images_cropped[row][col][:,:,1] = degrade-30
                            images_cropped[row][col][:,:,2] = degrade
                        elif predictionItem in self.ground_water:
                            images_cropped[row][col][:,:,0] = degrade
                        else:
                            #This is case present danger or mining
                            images_cropped[row][col][:,:,2] = degrade
            else:
                #print(prediccion)
                prediction_general = self.prediction_from_frame(frame)
                mensaje = "Zone Prediction -->   " + str(prediction_general)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, mensaje, (10, 40), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            #cv2.putText(frame,"altitude: " +str(altitude),(10, 200), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Se muestra en la ventana
            cv2.imshow('Video_Prediction', frame)

            k = cv2.waitKey(20) & 0xff
            if k == 27:
                break
        self.WebCamWindow.release()
        cv2.destroyAllWindows()


    def resizeImage(self,image):
        #print(image.shape)
        newImage = cv2.resize(image,(64,64))
        #print(newImage.shape)
        #cv2.imshow('Video_Redimension',newImage)
        return newImage

