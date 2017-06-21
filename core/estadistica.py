# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 09:44:50 2017

@author: JUANCHO
"""

import numpy as np
from scipy import ndimage

def abrir_imagen(ruta):
    """Funcion que abre una imagen y devuelve su matriz"""
    imagen = ndimage.imread(ruta)
    return imagen


def rgb2gray1(imagen):
    """Funcion que convierte una imagen a color a blanco y negro"""
    
    filas, columnas = imagen.shape[:2]
    
    mascara = np.zeros((filas, columnas), np.uint8)
    
    for fila in range(filas):
        for columna in range(columnas):
            mascara[fila, columna] = np.uint8(np.average(imagen[fila, columna,:]))
    
    return mascara

def rgb2gray(img):
    return np.uint8(np.dot(img[...,:3], [0.299, 0.587, 0.114]))

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
    
    
    
    
    
