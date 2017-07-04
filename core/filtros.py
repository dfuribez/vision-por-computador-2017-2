# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt

from core import common

def promedio(img, tamanio=3):
    if not tamanio % 2:
        tamanio += 1
        print(f"Se necesita core impar, trabajando con {tamanio}")
    
    core = np.ones((tamanio, tamanio))
    elem = tamanio ** 2
    
    offset = (tamanio - 1) // 2
    
    filas, columnas = img.shape[:2]
    
    new = np.zeros((filas, columnas))
    
    for fila in range(offset, filas - offset):
        for columna in range(offset, columnas - offset):
            
            im_part = img[fila-offset:fila+offset+1,columna-offset:columna+offset+1]
            
            im_sum = np.sum(im_part * core / elem)
            new[fila, columna] = im_sum
            
    return new

def mediana(img, tamanio):
    if not tamanio % 2:
        tamanio += 1
        print(f"Se necesita core impar, trabajando con {tamanio}")
    
    #core = np.ones((tamanio, tamanio))
    elem = tamanio ** 2
    
    offset = (tamanio - 1) // 2
    
    filas, columnas = img.shape[:2]
    
    new = np.zeros((filas, columnas))
    
    for fila in range(offset, filas - offset):
        for columna in range(offset, columnas - offset):
            
            im_part = img[fila-offset:fila+offset+1,columna-offset:columna+offset+1]
            im_part = im_part.ravel()
            mediana = np.sort(im_part)[elem // 2]
            
            new[fila, columna] = mediana
            
    return new

def moda(img, tamanio):
    if not tamanio % 2:
        tamanio += 1
        print(f"Se necesita core impar, trabajando con {tamanio}")
    
    moda_elementos = []
    moda_cantidad = []
    
    # core = np.ones((tamanio, tamanio))
    
    offset = (tamanio - 1) // 2
    
    filas, columnas = img.shape[:2]
    
    new = np.zeros((filas, columnas))
    
    for fila in range(offset, filas - offset):
        for columna in range(offset, columnas - offset):
            
            moda_elementos = []
            moda_cantidad = []
            
            im_part = img[fila-offset:fila+offset+1,columna-offset:columna+offset+1]
            im_part = im_part.ravel()
            
            counts = np.bincount(np.int64(im_part))
            moda = np.argmax(counts)

            new[fila, columna] = moda
            
    return new

def gauss(img):
    
    core = np.array([[1, 2, 1],
                     [2, 4, 2],
                     [1, 2, 1]]) / 16
    
    
    shape = len(img.shape)
    
    if shape == 2:
        filas, columnas, channels = img.shape + (None,)
        new = np.zeros((filas, columnas))
    else:
        filas, columnas, channels = img.shape
        new = np.zeros((filas, columnas, channels))
        
    offset = 1
    
    for fila in range(offset, filas -offset):
        for columna in range(offset, columnas - offset):
            if channels is None:
                im_part = img[fila-offset:fila+offset+1,columna-offset:columna+offset+1]
                nuevo = np.sum(im_part * core)
                new[fila, columna] = nuevo
            else:
                for channel in range(channels):
                    im_part = img[fila-offset:fila+offset+1,columna-offset:columna+offset+1,channel]
                    nuevo = np.sum(im_part * core)
                    new[fila, columna, channel] = int(nuevo)
    
    return new

def brillo_contraste(img, a, b):
    new = img.copy().astype(float)
    new = a * new + b
    new[new > 255] = 255
    new[new < 0] = 0
    return new


def umbralizar(img, umbral):    
    new = img.copy()
    
    if "-" in umbral:
        umbrales = umbral.split("-")
        
        if len(umbrales) == 2:
            u1, u2 = map(int, umbrales)
            if u1 > u2:
                buff_mayor = new <= u1
                buff_menor = new > u2
            else:
                buff_mayor = new <= u2
                buff_menor = new > u1
            
            mascara = np.logical_and(buff_mayor, buff_menor)
            new[mascara] = 255
            
            mascara = np.logical_not(mascara)
            new[mascara] = 0
            
            titulo = f"umbralizada entre {u1} y {u2}"
        else:
            # Pedir de nuevo el umbral
            return None
    else:
        
        umbral = common.is_int(umbral)
        
        if umbral is not None:
            new[new >= umbral] = 255
            new[new < umbral] = 0
            
            titulo = f"Umbralizada: {umbral}"
        else:
            # Pedir de nuevo el umbral
            return None
    
    return (new, titulo)

if __name__ == "__main__":
    imagen = "../img/gris.jpg"
    #imagen = "../img/gris.jpg"
    img = ndimage.imread(imagen)
    
    #img = np.zeros((100, 100))
    #img[50, 50] = 255

    plt.imshow(img, cmap="gray")
    plt.show()
    
    new = moda(img, 3)
    plt.imshow(new, cmap="gray")
    plt.show()
