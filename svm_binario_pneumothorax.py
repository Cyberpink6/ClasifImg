# -*- coding: utf-8 -*-
"""SVM Binario Pneumothorax.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dR-nFrnSjC9NPTcdWzZ-adJVKZhlkhO2

##Importando Librerias
"""

import numpy as np
from sklearn import svm
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import pandas as pd
from keras.utils import to_categorical
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    recall_score,
    log_loss,
    precision_score,
    f1_score
    )
import matplotlib.pyplot as plt

"""##Importando desde Drive"""

from google.colab import drive
drive.mount('/content/drive')

"""##Adaptando las imagenes al X y Y

"""

# Leer el archivo CSV
data = pd.read_csv('/content/drive/MyDrive/Binario Pneumothorax/dataset.csv')

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

"""##Entrenando"""

# Crear y entrenar el clasificador SVM para clasificación binaria
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = svm.predict(X_test)

"""##Accuracy y Loss"""

# Calcula la precisión y la pérdida en los datos de prueba
precision = accuracy_score(y_test, y_pred)
perdida = log_loss(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Imprime la precisión y la pérdida
print(f"Accuracy: {precision}")
print(f"Loss: {perdida}")
print(f"F1-score: {f1}")

# Graficar la precisión y la pérdida
nombres_metricas = ['Accuracy', 'Loss', 'F1-score']
valores_metricas = [precision, perdida, f1]

plt.bar(nombres_metricas, valores_metricas)
plt.xlabel('Métrica')
plt.ylabel('Valor')
plt.title('Métricas de Evaluación')
plt.show()
