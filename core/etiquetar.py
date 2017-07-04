# -*- coding: utf-8 -*-

import numpy as np

def conectividad(img):
    """Función que calcula la conectividad de un pixel.
    
    img: ventana 3x3 centrada en el pixel a calcular la vecindad
    
    Devuelve la vecindad."""
    coor = [img[0, 1], img[0, 2], img[1, 2],
        img[2, 2], img[2, 1], img[2, 0],
        img[1, 0], img[0, 0]]
    
    con = 0
    for x in range(len(coor) - 1):
        if coor[x] != coor[x+1]:
            con += 1
    
    if coor[0] != coor[-1]:
        con += 1
    
    #print("\r",coor, "->", con - 1)
    return con - 1

def etiquetar(img):
    """Función que etiquea los elementos de una imagen.
    
    Los objetos deben ser de color blanco (intensidad uno (1))
    y el fondo negro (intensidad cero (0))
    
    img: imagen a etiquetar
    
    Devuelve una lista donde el primer elemento es la imagen etiquetada
    y el segundo, un conjunto con las etiquetas"""
    
    
    filas, columnas = img.shape
    
    etiquetas = set()
    etiqueta = 2
    encontrados = 0
    
    mascara = np.ones((3, 3), np.int_)
    
    new = img.copy()
    #new = np.zeros((filas, columnas))
    
    for fila in range(1, filas - 1):
        for columna in range(1, columnas - 1):
            # Si el píxel es distinto de cero, analiza los vecinos
            if new[fila, columna]:
                # Obtiene la vecindad de 3x3
                ventana = new[fila-1:fila+2, columna-1:columna+2]
    #            ventana = window * mascara
                elementos = set(ventana.ravel())
                
                maximo = max(elementos)
                if maximo == 1:

                    ventana[ventana > 0] = etiqueta
                    etiquetas.add(etiqueta)
                    etiqueta += 1
                    encontrados += 1
                elif maximo > 1:
                    elementos = elementos - {0, 1, maximo}
                    if len(elementos) >= 1:
                        
                        encontrados -= len(elementos)
                        for vieja in elementos:
                            if vieja in etiquetas:
                                etiquetas.remove(vieja)
                            new[new == vieja] = maximo
                    else:
                        ventana[ventana > 0] = maximo
                        new[fila-1:fila+2, columna-1:columna+2] = ventana
    print(etiquetas)
    return new, etiquetas

def roi(img, etiqueta):
    """Función que extrae un elemento de una imagen etiquetada.
    
    img: imagen etiqeutada
    etiqueta: etiqueta del elemento a extraer
    
    Devuelve el elemento extraido"""
    
    filas, columnas = img.shape
    x1, y1 = None, None
    x2, y2 = None, None
    x3, y3 = None, None
    x4, y4 = None, None
    
    for fila in range(filas):
        act = img[fila,:]
        #print(act)
        if etiqueta in act:
            if x1 is None:
                x1 = fila
                y1 = 0
        else:
            if (x1 is not None):
                x2 = fila
                y2 = 0
                break
    
    for columna in range(columnas):
        act = img[:, columna]
        if etiqueta in act:
            if x3 is None:
                x3 = columna
            y3 = 0
        else:
            if x3 is not None:
                x4 = columna
                y4 = 0
                break
    
    #print ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
    return img[x1:x2, x3:x4]

def perimetro(img):
    """Calcula el perimetro de un objeto.
    
    img: objeto a calcular.
    
    Devuelve el perimetro del elemento
    """
    img = img // np.amax(img)
    filas, columnas = img.shape
    new = np.zeros((filas + 2, columnas + 2))
    new[1:-1, 1:-1] = img
    #print(new)
    p = 0
    
    for fila in range(1, filas + 2):
        for columna in range(1, columnas + 2):
            if new[fila, columna]:
                window = new[fila-1:fila+2, columna-1:columna+2]
                if 0 < np.sum(window) - 1 < 8:
                    #print("(",fila, ",", columna, ")")
                    if conectividad(window) == 1:
                        p += 1
    return p

def area(img):
    """Calcula el área de un objeto."""
    
    return np.count_nonzero(img)

def circularidad(img):
    """Calcula la circularidad."""
    a = area(img)
    p = perimetro(img)
    
    if p == 0:
        return 0
    
    #c = (p ** 2) / (4 * 3.1416 * a)
    c = (4 * 3.1416 * a) / (p ** 2)
    return c

def centroide(img):
    """Calcula el centroide.
    
    Devuelve una lista con las coordenadas en x, y"""
    
    filas, columnas = img.shape
    a = area(img)
    if a == 0:
        return 0, 0
    
    cx, cy = 0, 0
    for fila in range(filas):
        for columna in range(columnas):
            if img[fila, columna]:
                cx += fila
                cy += columna
    
    return (cx/a, cy/a)
    

if __name__ == "__main__":
    from scipy import ndimage
    from matplotlib import pyplot as plt
    import estadistica
    import math
    imagen = "../img/et.jpg"
    #imagen = "p.jpg"
    img = ndimage.imread(imagen)
    img = estadistica.rgb2gray(img)
    #print(img.shape)
    img[img<=50] = 0
    img[img>50] = 1
    img = 1 - img


    #print(perimetro(np.ones((10, 10))))
    
    #plt.imshow(img)
    #plt.show()
    
    new, etiquetas = etiquetar(img)
    #plt.imshow(new)
    #plt.show()
    
    for item in etiquetas:
        print(item)
        new_roi = roi(new, item)
        #print(perimetro(new_roi))
        p = perimetro(new_roi)
        a = area(new_roi)
        cx, cy = map(int, centroide(new_roi))
        print("p ->", p)
        print("a ->", a)
        print("c ->", circularidad(new_roi))
        print(cx, cy)
        print(new_roi.shape)
        new_roi[cx, cy] = 1
        plt.imshow(new_roi, cmap="binary")
        plt.show()
    #print(new)
    #print(_)
