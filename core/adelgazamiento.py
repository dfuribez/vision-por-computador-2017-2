# -*- coding: utf-8 -*-

import numpy as np


def conectividad(region):
    region = region.ravel()
    print(region)
    last = False
    con = 0
    for x in region:
        if x:
            if last != x:
                con += 1
            last = True
        else:
            last = False
    return con


def con2(img):
    coor = [img[0, 1], img[0, 2], img[1, 2],
            img[2, 2], img[2, 1], img[2, 0],
            img[1, 0], img[0, 0]]
    
    coor = "".join([str(x) for x in coor])
    
    return coor.find("01")


VEC = np.ones((3, 3))
VEC[1, 1] = 0

K1 = np.array([[0, 1, 0],
               [0, 0, 1],
               [0, 1, 0]])

K2 = np.array([[0, 0, 0],
               [1, 0, 1],
               [0, 1, 0]])

K3 = np.array([[0, 1, 0],
               [1, 0, 1],
               [0, 0, 0]])

K4 = np.array([[0, 1, 0],
               [1, 0, 0],
               [0, 1, 0]])

def condicion_uno(window):
    uno = np.sum(K1 * window)
    dos = np.sum(K2 * window)
    if (uno < 3) and (dos < 3):
        return True
    else:
        return False

def condicion_dos(window):
    uno = np.sum(K3 * window)
    dos = np.sum(K4 * window)
    if (uno < 3) and (dos < 3):
        return True
    else:
        return False

def  zhang(img, iteracion=1, n=1, anterior=None):
    print(iteracion)
    filas, columnas = img.shape
    #n = 1
    for fila in range(1, filas-1):
        for columna in range(1, columnas-1):
            if img[fila, columna]:
                #print(".")
                window = img[fila-1:fila+2, columna-1:columna+2]
                vecinos = np.sum(VEC * window)
                if 2 <= vecinos <= 6:
                    #print("vecinos")
                    #print(window)
                    #input()
                    if con2(window) == 1:
                        #print("ceros")
                        if iteracion == 1:
                            #print("iteracion")
                            if condicion_uno(window):
                                img[fila, columna] = 2
                                #print("Marcando:", fila, columna)
                            else:
                                next
                        if iteracion ==2:
                            if condicion_dos(window):
                                img[fila, columna] = 2
    n += 1
    
    if not n % 2:
        iteracion = 2
    else:
        iteracion = 1

    if np.sum(img == 2):
        img[img == 2] = 0
        img = zhang(img, iteracion, n, True)
    elif anterior is None:
        img = zhang(img, iteracion, n, False)
    elif not anterior:
        return img
    else:
        img = zhang(img, iteracion, n, False)
    
    return img
    


A = np.array([[0, 1, 0],
              [0, 0, 0],
              [1, 1, 1]]) 

B = np.array([[8, 1, 2],
              [7, 0, 3],
              [6, 5, 4]])

C = np.array([[0, 0, 0],
              [1, 0, 1],
              [0, 1, 0]])

D = np.array([[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

if __name__ == "__main__":
    from scipy import ndimage
    from matplotlib import pyplot as plt
    imagen = "../img/ske.jpg"
    img = ndimage.imread(imagen)
    img = img[:,:,0]
    img[img > 0] = 1
    
    new = zhang(img)
    print(new)
    plt.imshow(new, cmap="gray")
    plt.show()
