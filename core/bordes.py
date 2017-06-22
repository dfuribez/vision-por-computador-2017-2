# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt

def roberts(img, umbral):
    kx = np.array([[0, 1],
                   [-1, 0]])
    
    ky = np.array([[1, 0],
                   [0, -1]])
    
    filas, columnas = img.shape[:2]
    
    bordes = np.zeros((filas, columnas))
    
    for fila in range(1, filas - 1):
        for columna in range(1, columnas - 1):
            window = img[fila-1:fila+1, columna-1:columna+1]
            
            convolucion_x = np.sum(window * kx) 
            convolucion_y = np.sum(window * ky)
            
            gradiente = np.sqrt(convolucion_x * convolucion_x + convolucion_y * convolucion_y)
            
            if umbral is None:
                umbral = np.average(window)
                print(umbral)
            
            if gradiente < umbral:
                bordes[fila, columna] = 0
            else:
                bordes[fila, columna] = 255
    
    return bordes


if __name__ == "__main__":
    import filtros
    import estadistica
    imagen = "../img/Lena.jpg"
    img = ndimage.imread(imagen)
    img = estadistica.rgb2gray_dos(img)
    img = filtros.gauss(img)
    bordes = roberts(img, 20)
    
    plt.imshow(img, cmap="gray")
    plt.show()
    
    plt.imshow(bordes, cmap="gray")
    plt.show()