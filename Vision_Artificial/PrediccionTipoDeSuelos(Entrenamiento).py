import os
import numpy as np
from PIL import  Image
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
path_dataset = 'Dataset_Images/'

dic_clas  = {}
datos_entrada = []
clases_salida = []
i = 0

for element in os.listdir(path_dataset):

    if os.path.isdir(path_dataset + element):
        for file in os.listdir(path_dataset + element):
            im = Image.open(os.path.join(path_dataset, element, file))
            im_array = np.array(im)
            datos_entrada.append(im_array)
            clases_salida.append(i)
        dic_clas[i] = element
        i += 1
        print(element)


print('Datos Cargados')

clases_salida_oh = to_categorical(clases_salida)

datos_entrada = np.array(datos_entrada)
datos_entrada = datos_entrada/255

x_train,x_test,y_train,y_test = train_test_split(datos_entrada,clases_salida_oh,test_size=0.2,shuffle=True)

print('Generating Shapes')

in_shape = x_train[0,:,:,:].shape

model = Sequential()

print('Creating Model')

model.add(Conv2D(16,kernel_size=3,activation='relu',input_shape=in_shape))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(32,kernel_size=3,activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64,kernel_size=3,activation='relu'))
model.add(Flatten())
model.add(Dense(50))
model.add(Dense(len(dic_clas),activation='softmax'))

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

print('Training Model')

model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=10)

print('Prediciendo')

prob_pred_test = model.predict(x_test)

predicciones_test = [dic_clas[np.argmax(prob)] for prob in prob_pred_test]
clases_test = [dic_clas[np.argmax(clas)] for clas in y_test]


print('Clases Reales')
print(clases_test[:10])
print('Clases Predichas')
print(predicciones_test[:10])


print('Guardando modelo')
model_json = model.to_json()
with open("TrainModelAfterMining.json", "w") as json_file:
    json_file.write(model_json)
# serializar los pesos a HDF5
model.save_weights("TrainModelAfterMining.h5")

print("Model Saved!")