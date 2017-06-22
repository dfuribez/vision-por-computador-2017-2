# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 14:52:49 2017

@author: Estudiante
"""

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

def core(img, matriz, n_filas=None, n_columnas=None, off_filas=0, off_columnas=0):
    
    shape = img.shape
    
    filas, columnas = shape[:2]
    
    if n_filas is None:
        n_filas = filas
    if n_columnas is None:
        n_columnas = columnas
    
    if len(shape) == 2:
        prof = None
        new = np.ones((n_filas, n_columnas), np.uint8) * 255
    else:
        prof = shape[-1]
        new = np.ones((n_filas, n_columnas, prof), np.uint8) * 255
    
    
    for fila in range(filas):
        for columna in range(columnas):
            coor_x, coor_y, z = ([fila, columna, 1] @ matriz).astype(int)
            if prof is None:
                new[coor_x+off_filas, coor_y+off_columnas] = img[fila, columna]
            else:
                new[coor_x+off_filas, coor_y+off_columnas,:] = img[fila, columna,:]
                
    
    return new

if __name__ == "__main__":
    import estadistica
    img = ndimage.imread("../img/trans.jpg")
    
    #plt.imshow(img)
    #plt.show()
    # TRasladar
    print(img.shape)
    mat = np.identity(3)
    #print(mat)
    im = core(img, mat)
    plt.imshow(im)
    plt.show()
