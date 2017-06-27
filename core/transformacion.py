# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from scipy import ndimage
import math


def mat_ref(x, y):
    mat = np.identity(3)
    if x:
        mat[1, 1] = -1
    if y:
        mat[0, 0] = -1

    return mat

def mat_rotacion_x(angulo):
    mat = np.identity(3)
    seno = math.sin(math.radians(angulo))
    coseno = math.cos(math.radians(angulo))
    
    mat[1, 1] = coseno
    mat[1, 2] = seno
    mat[2, 1] = -seno
    mat[2, 2] = coseno
    
    return mat

def mat_rotacion_y(angulo):
    mat = np.identity(3)
    seno = math.sin(math.radians(angulo))
    coseno = math.cos(math.radians(angulo))
    
    mat[0, 0] = coseno
    mat[2, 0] = seno
    mat[0, 2] = -seno
    mat[2, 2] = coseno
    
    return mat

def mat_rotacion_z(angulo):
    mat = np.identity(3)
    seno = math.sin(math.radians(angulo))
    coseno = math.cos(math.radians(angulo))
    
    mat[0, 0] = coseno
    mat[0, 1] = -seno
    mat[1, 0] = seno
    mat[1, 1] = coseno
    
    return mat

def core(img, matriz, n_filas=None, n_columnas=None,
         off_filas=0, off_columnas=0):
    
    shape = img.shape
    
    filas, columnas = shape[:2]
    
    if n_filas is None:
        n_filas = filas
    if n_columnas is None:
        n_columnas = columnas
    
    if len(shape) == 2:
        shape = (n_filas, n_columnas)
    else:
        shape = (n_filas, n_columnas, shape[-1])
        
    new = np.zeros(shape, np.uint8)
    
    for fila in range(filas):
        for columna in range(columnas):
            
            coor_x, coor_y, z = ([fila, columna, 1] @ matriz).astype(int)
            
            new[coor_x+off_filas, coor_y+off_columnas,...] = img[fila, columna,...]
                
    
    return new

def interpolar(img, factor):
    
    shape = img.shape
    filas, columnas = shape[:2]
    
    for fila in range(0, filas, factor):
        try:
            izq = img[fila,...]
            der = img[fila+factor,...]
            centro = int(np.ceil((factor - 1) / 2))
            for pixel in range(1, factor):
                #if pixel < centro:
                    #new_pixel = izq
                #elif pixel == centro:
                    #new_pixel = (izq + der) / 2
                #else:
                    #new_pixel = der
                #new_pixel = (izq +der) // 2
                new_pixel = izq
                img[fila+pixel,...] = new_pixel
        except:
            pass
    
    for columna in range(0, columnas, factor):
        try:
            izq = img[:,columna,...]
            der = img[:,columna,...]
            centro = int(np.ceil((factor - 1 ) / 2))
            for pixel in range(1, factor):
                #if pixel < centro:
                    #new_pixel = izq
                #elif pixel == centro:
                    #new_pixel = (izq + der) / 2
                #else:
                    #new_pixel = der
                #new_pixel = (izq + der) // 2
                new_pixel = izq
                img[:,columna+pixel,...] = new_pixel
        except:
            pass
    return img
    

if __name__ == "__main__":
    A = 2
    #img = np.arange(1, 16).reshape(3, 5)
    img = ndimage.imread("../img/gris.jpg")
    #img = img[:,:,0]
    mat = np.identity(3) * A
    
    print(img.shape)
    
    nfilas, ncolumnas = [x * A for x in img.shape[:2]]
    
    new = core(img, mat, nfilas, ncolumnas)
    
    print(new.shape)

    plt.imshow(new, cmap="gray")
    plt.show()
    
    new = interpolar(new, A)
    
    print(new.shape)
    plt.imshow(new, cmap="gray")
    plt.show()
    
    
