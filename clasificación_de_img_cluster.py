# -*- coding: utf-8 -*-
"""Clasificación de Img Cluster.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Et_OKMldzVei6BOCg6Ju_vdx6EaEIpVA

##Importaciones
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import image
from tensorflow.keras import regularizers
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Flatten,
    Conv2D,
    MaxPooling2D
    )
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    recall_score,
    precision_score,
    f1_score
    )
from tensorflow.keras.optimizers import Adam
from tensorflow.image import rgb_to_grayscale
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import plot_model
import tensorflow as tf
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np
import os
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import cv2
from tensorflow.keras.optimizers import SGD
from sklearn.model_selection import StratifiedKFold
import numpy as np

"""##Montar Google Drive"""

from google.colab import drive
drive.mount('/content/drive')

"""##Crear el csv"""

# Directorio base que contiene las subcarpetas de train y test
base_dir = '/content/drive/MyDrive/Dataset Desbalanceado'

# Crear una lista vacía para almacenar los datos del dataset
dataset = []

for enfermedad in os.listdir(base_dir):
    enfermedad_dir = os.path.join(base_dir, enfermedad)

    # Verificar si el elemento es un directorio
    if os.path.isdir(enfermedad_dir):
        # Recorrer las imágenes dentro de cada clase
        for imagen in os.listdir(enfermedad_dir):
            imagen_path = os.path.join(enfermedad_dir, imagen)

            # Obtener el nombre de la enfermedad
            label = None
            if enfermedad == 'Pneumonia':
                label = 1
            elif enfermedad == 'Pneumothorax':
                label = 2
            elif enfermedad == 'Nodule':
                label = 3
            else:
                label = 0

            # Agregar la información de la imagen y sus atributos al dataset
            dataset.append((imagen_path, label))

# Crear el DataFrame a partir de los datos del dataset
df = pd.DataFrame(dataset, columns=['Imagen', 'Label'])

# Escribir el DataFrame en un archivo CSV
df.to_csv('/content/drive/MyDrive/Dataset Desbalanceado/dataset.csv', index=False)

"""##Leer los datos de las imágenes"""

# Leer el archivo CSV
data = pd.read_csv('/content/drive/MyDrive/Dataset Desbalanceado/dataset.csv')

# Obtener las columnas 'imagen' y 'label'
X_paths = data.iloc[:, 0]  # Características
y = data.iloc[:, 1]  # Etiquetas

# Cargar las imágenes y convertirlas en matrices de píxeles
X = []
for path in X_paths:
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir de BGR a RGB
    X.append(image)

X = np.array(X)

"""##Crear el modelo"""

inp_shape = (224,224,1)
act = ('relu')
drop = .5
kernal_reg = regularizers.l1(.001)
dil_rate = 2
epochs_without_improvement = 0
batch_size = 32
epochs = 50

model = Sequential()
model.add(Conv2D(64, kernel_size=(3,3),activation=act, input_shape = inp_shape,
               kernel_regularizer = kernal_reg,
               kernel_initializer = 'he_uniform',  padding = 'same', name = 'Input_Layer'))
model.add(MaxPooling2D(pool_size=(2, 2),  strides = (2,2)))
model.add(Flatten())
model.add(Dense(32, activation=act))
model.add(Dropout(drop))
model.add(Dense(4, activation='softmax', name = 'Output_Layer'))
# compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Callback para guardar el modelo con la mejor precisión
early_stopping = EarlyStopping(monitor='val_accuracy', verbose = 1, patience=3, min_delta = 0.005, mode='max')
checkpoint = ModelCheckpoint("modelo_prueba.keras", verbose=1, save_best_only=True)

"""##Valicacion cruzada (Editar)"""

# Leer archivos CSV
train_files = ['/content/drive/MyDrive/Dataset Desbalanceado/0train.csv',
               '/content/drive/MyDrive/Dataset Desbalanceado/1train.csv',
               '/content/drive/MyDrive/Dataset Desbalanceado/2train.csv',
               '/content/drive/MyDrive/Dataset Desbalanceado/3train.csv',
               '/content/drive/MyDrive/Dataset Desbalanceado/4train.csv']  # Provide the full path to your training files
test_files = ['/content/drive/MyDrive/Dataset Desbalanceado/0test.csv',
              '/content/drive/MyDrive/Dataset Desbalanceado/1test.csv',
              '/content/drive/MyDrive/Dataset Desbalanceado/2test.csv',
              '/content/drive/MyDrive/Dataset Desbalanceado/3test.csv',
              '/content/drive/MyDrive/Dataset Desbalanceado/4test.csv']   # Provide the full path to your testing files

# Lista para almacenar resultado

# Lista para almacenar resultados
results = []

# Iterar sobre cada par de archivos de entrenamiento y prueba
for train_file, test_file in zip(train_files, test_files):
    # Leer el archivo CSV
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(train_file)

    # Cargar imágenes y etiquetas
    X_train = np.array([X(img) for img in train_data['Imagen']])
    y_train = train_data['Label'].values
    X_test = np.array([X(img) for img in test_data['Imagen']])
    y_test = test_data['Label'].values

    # Crear y entrenar el modelo
    model = model(num_classes=len(np.unique(y_train)))  # Ajusta num_classes a tu caso
    model.fit(X_train.reshape(X_train.shape[0], -1), y_train, epochs=10, batch_size=32)  # Ajusta epochs y batch_size

"""##Entrenar el modelo"""

# Entrenamiento del modelo

model_checkpoint = ModelCheckpoint('modelo_prueba.h5', verbose = 1, save_best_only=True,
                                  monitor = 'val_accuracy', min_delta = .002)
lr_plat = ReduceLROnPlateau(patience = 3, mode = 'min')
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                    callbacks=[early_stopping,model_checkpoint, lr_plat],
                    validation_data=(X_test, y_test), verbose=1)
print("Epoch {}/{}".format(epochs, epochs))
loss, accuracy = model.evaluate(X_test, y_test, verbose=1)

"""##Guardar el modelo"""

model.save('modelo_prueba.h5')