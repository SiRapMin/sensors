import numpy as np
from PIL import Image
import easygui as eg
from keras.models import model_from_json

############## POSIBLES CLASES ##################

dic_clas = {0: 'AnnualCrop',
            1: 'Forest',
            2: 'Highway',
            3: 'Industrial',
            4: 'Mining',
            5: 'Pasture',
            6: 'Residential',
            7: 'River',
            8: 'SeaLake'}

dic_clas_spanish = {0: 'Cultivos o Sabanas',
            1: 'Bosque',
            2: 'Autopista',
            3: 'Industrial',
            4: 'Mineria',
            5: 'Pasto',
            6: 'Residencial',
            7: 'Rio',
            8: 'Mar'}

# cargar json y crear el modelo
json_file = open('tipodesuelos.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)


# Cargar pesos al nuevo modelo
loaded_model.load_weights("tipodesuelos.h5")

print("Cargado modelo desde disco.")

#Compilamos el modelo
loaded_model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])


#Elegimos una imagen
extension = ["*.jpg", "*.png"]
imagen_url = eg.fileopenbox(msg="Abrir archivo",
                         title="Control: fileopenbox",
                         default='',
                         filetypes=extension)

#Guardamos la imagen dentro de nuestro arreglo que sera la entrada de nuestra red neuronal
imagen = Image.open(str(imagen_url))
im_array = np.array(imagen)
datos_entrada = (np.array([im_array]))/255

#El modelo predice la entrada y genera un arreglo con la probabilidad de cada clase de imagen
prob_pred_test = loaded_model.predict(datos_entrada)

print(prob_pred_test)
#Escogemos la probabilidad mayor y la mostramos
predicciones_test = [dic_clas_spanish[np.argmax(prob)] for prob in prob_pred_test]
print(predicciones_test)

