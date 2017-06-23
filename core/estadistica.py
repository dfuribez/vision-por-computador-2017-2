# -*- coding: utf-8 -*-

import numpy as np


def rgb2gray(img):
    return np.dot(img[...,:3], [1, 1, 1])

def rgb2gray_uno(img):
    return np.dot(img[...,:3], [0.2125, 0.7154, 0.0721])

def rgb2gray_dos(img):
    return np.dot(img[...,:3], [0.5, 0.419, 0.081])

def histograma(img):
    array = []
    for x in range(256):
        array.append(np.sum(img == x))
    return array

def media(img):
    """Funcion que calcula el proimedio de la intensidad de pixeles"""
    filas, columnas = img.shape[:2]
    prom = 0
    for fila in range(filas):
        for columna in range(columnas):
            prom += img[fila, columna]
    
    return (prom / (filas * columnas))

def varianza(img, media):
    """Funcion que calcula la varianza"""
    filas, columnas = img.shape[:2]
    var = 0
    for fila in range(filas):
        for columna in range(columnas):
            var += ((img[fila, columna] - media) ** 2)
    
    t = filas * columnas
    var = (var / t)
    
    return var
            
def mediana(img):
    pixels = img.ravel()
    pixels = np.sort(pixels)
    
    longitud = len(pixels)    
    
    if longitud % 2:
        index = int((longitud - 1) / 2)
    else:
        index = int(longitud / 2)
    
    return pixels[index]
    
    
def moda(histograma):
    v_max = max(histograma)
    #print(v_max)
    moda = histograma.index(v_max)
    return moda
    
    
    
    
    
