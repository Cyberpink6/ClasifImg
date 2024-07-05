# -*- coding: utf-8 -*-
"""SVM 224x224 Multiclase.iynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1q85ILgKqT6rVW9TdBFnITr5kEl_-04tr

##Importando Librerias
"""

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from keras.utils import to_categorical
import cv2
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    recall_score,
    precision_score,
    f1_score
    )
import matplotlib.pyplot as plt

"""##Importando desde Drive"""

from google.colab import drive
drive.mount('/content/drive')

"""##Adaptando las imagenes al X y Y y entrenando

"""

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

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = X_train.reshape(-1, 224*224)
X_test = X_test.reshape(-1, 224*224)

# Crear y entrenar el clasificador SVM
svm = SVC(kernel='linear')  # Puedes ajustar el tipo de kernel según tus necesidades (lineal, polinomial, RBF, etc.)
svm.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = svm.predict(X_test)

# Calcular las métricas de rendimiento
accuracy = accuracy_score(y_test, y_pred)
confusion_mat = confusion_matrix(y_test, y_pred)
# Resto de las métricas que desees calcular

# Imprimir los resultados
print("Exactitud:", accuracy)
print("Matriz de confusión:")
print(confusion_mat)
# Imprimir el resto de las métricas
print("Exactitud: {:.2f}".format(accuracy))

# Graficar la exactitud y F1-score
labels = ['Exactitud']
scores = [accuracy]

plt.bar(labels, scores)
plt.ylim(0, 1)
plt.title('Exactitud y F1-score del modelo SVM')

plt.show()