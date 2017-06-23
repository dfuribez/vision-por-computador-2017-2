# -*- coding: utf-8 -*-

import numpy as np

def kernel_kirsch():
    r1 = np.array([[5, -3, -3],
                   [5, 0, -3],
                   [5, -3, -3]])
    
    r2 = np.array([[-3, -3, -3],
                   [5, 0, -3],
                   [5, 5, -3]])
    
    r3 = np.array([[-3, -3, -3],
                   [-3, 0, -3],
                   [5, 5, 5]])
    
    r4 = np.array([[-3, -3, -3],
                   [-3, 0, 5],
                   [-3, 5, 5]])
    
    r5 = np.array([[-3, -3, 5],
                   [-3, 0, 5],
                   [-3, -3, 5]])
    
    r6 = np.array([[-3, 5, 5],
                   [-3, 0, 5],
                   [-3, -3, -3]])
    
    r7 = np.array([[5, 5, 5],
                   [-3, 0, -3],
                   [-3, -3, -3]])
    
    r8 = np.array([[5, 5, -3],
                   [5, 0, -3],
                   [-3, -3, -3]])
    
    return (2, r1, r2, r3, r4, r5, r6, r7, r8)

def kernel_sobel():
    sx = np.array([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]])
    
    sy = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]])
    
    return (1, sx, sy)

def kernel_roberts():
    # Roberts
    rx = np.array([[0, 1],
                   [-1, 0]])
    
    #Riberts
    ry = np.array([[1, 0],
                   [0, -1]])

    return (1, rx, ry)

def kernel_robinson():
    r1 = np.array([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]])
    
    r2 = np.array([[0, -1, -2],
                   [1, 0, -1],
                   [2, 1, 0]])
    
    r3 = np.array([[-1, -2, -1],
                   [0, 0, 0],
                   [1, 2, 1]])
    
    r4 = np.array([[-2, -1, 0],
                   [-1, 0, 1],
                   [0, 1, 2]])
    
    r5 = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
    
    r6 = np.array([[0, 1, 2],
                   [-1, 0, 1],
                   [-2, -1, 0]])
    
    r7 = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]])
    
    r8 = np.array([[2, 1, 0],
                   [1, 0, -1],
                   [0, -1, -2]])
    
    return (2, r1, r2, r3, r4, r5, r6, r7, r8)

lista_kernels = {"roberts": kernel_roberts,
                 "sobel": kernel_sobel,
                 "kirsch": kernel_kirsch,
                 "robinson": kernel_robinson}

def core(img, tipo, umbral):
    """Función que calcula los bordes de una imagen por Roberts y Sobel.
    
    img: imagen para calcular los bordes.
    kernels: lista de kernels a aplicar.
    umbral: umbral a aplicar para decidir si se toma el borde o no.
    tipo: 1 ó 2, tipo1 bordes Roberts y sobel, tipo 2, bordes Kirshc, robinson"""
    
    kernels = None
    
    # Obtenemos el kernel dependiendo del tipo
    clase, *kernels = lista_kernels[tipo]()
    
    if kernels is None:
        print(f"Método {tipo} no soportado.")
        return
    
    
    filas_k, columnas_k = kernels[0].shape
    
    filas, columnas = img.shape[:2]
    
    bordes = np.zeros((filas, columnas))
    
    if not filas_k % 2:
        
        impar = False
        offset = 0
    else:
        # Siel kernel es impar, se calcula el centro
        impar = True
        offset = (filas_k - 1) // 2
    
    for fila in range(offset, filas - offset):
        for columna in range(offset, columnas - offset):
            if impar:
                #print("Impar")
                window = img[fila-offset:fila+offset+1,columna-offset:columna+offset+1]
            else:
                #print("Par")
                window = img[fila:fila+2, columna:columna+2]
        
            conv = []
            # Aplicamos la convolución para todos los filtros
            for kernel in kernels:
                conv.append(np.sum(window * kernel))
        
            # Calculamos la magnitud
            if clase == 1:
                # Calculamos la magnitud para Sobel Y Roberts
                magnitud = np.power(conv, 2)
                magnitud = np.sqrt(np.sum(magnitud))
            else:
                # Calculamos la máxima respuesta para Kirsch y robinson.
                magnitud = max(conv)
        
            if magnitud < umbral:
                bordes[fila, columna] = 0
            else:
                bordes[fila, columna] = 255
    
    return bordes
    

if __name__ == "__main__":
    import filtros
    import estadistica
    from scipy import ndimage
    from matplotlib import pyplot as plt
    imagen = "../img/Lena.jpg"
    img = ndimage.imread(imagen)
    img = estadistica.rgb2gray_dos(img)
    img = filtros.gauss(img)
    
    
    # Roberts
    #bordes = core(img, [rx, ry], 20)
    
    # Sobel
    bordes = core(img, "robinson", 20)
    
    #bordes = roberts(img, 20)
    
    plt.imshow(img, cmap="gray")
    plt.show()
    
    plt.imshow(bordes, cmap="gray")
    plt.show()
