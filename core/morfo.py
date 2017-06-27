# -*- coding: utf-8 -*-
import numpy as np


def core(img, kernel, op="dil"):
    filas, columnas= img.shape
    filas_k, columnas_k = kernel.shape
    
    offset_x = (filas_k - 1) // 2
    offset_y = (columnas_k - 1) // 2
    
    new = np.zeros((filas, columnas))
    
    for fila in range(offset_x, filas - offset_x):
        for columna in range(offset_y, columnas - offset_y):
            
            suma = []
            value = 0
            for x in range(filas_k):
                for y in range(columnas_k):
                    suma.append(img[fila-offset_x+x, columna-offset_y+y] + kernel[x, y])
            
            if op == "dil":
                value = max(suma)
            else:
                value = min(suma)
            
            for x in range(filas_k):
                for y in range(columnas_k):
                    if kernel[x, y]:
                        new[fila-offset_x+x, columna-offset_y+y] = value
    
    return new

if __name__ == "__main__":
    from scipy import ndimage
    from matplotlib import pyplot as plt
    imagen = "../img/test.png"
    img = ndimage.imread(imagen)
    img = np.amax(img) - img[:,:,0]
    
    #img = np.zeros((100, 100))
    #img[50, 50] = 255
    
    kernel = np.ones((5, 5))
    #kernel[0, 0] = 1
    #kernel[-1, -1] = 1
    print(kernel)
    plt.imshow(img, cmap="gray")
    plt.show()
    
    dil = core(img, kernel, "ero")
    plt.imshow(dil, cmap="gray")
    plt.show()
    dil = core(dil, kernel, "dil")
    
    #new = core(img, kernel, "a")
    plt.imshow(dil, cmap="gray")
    plt.show()