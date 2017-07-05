import numpy as np
import sys
from core import estadistica  # RGB2Gray
from core import etiquetar  # Etiquetar elementos imagen binaria
from core import morfo  # Aplicar operaciones morfológicas
from core import common  # Operaciones comunes

from matplotlib import pyplot as plt

IMAGEN = "img/partituras/burro_partitura1.jpg"
#IMAGEN = "img/partituras/tetris.jpg"
IMAGEN = "part2.png"
THRESH = 100
KERNEL = np.array([[1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1]])

#KERNEL = np.ones((3, 3))

#KERNEL = np.array([[1, 1, 1]])


def mayor(et, eti, umbral):
    
    encontrados = []
    u_filas, u_columnas = umbral
    for etiqueta in eti:
        roi = etiquetar.roi(et, etiqueta)
        filas, columnas = roi.shape
        if filas >= u_filas and columnas >= u_columnas:
            encontrados.append(roi)
    
    return encontrados
            
def find_lines(parte):
    filas, columnas = parte.shape
    new = np.zeros((filas, columnas))
    line = 1
    antes = False
    for fila in range(filas):
        suma = 0
        for columna in range(columnas):
            if parte[fila, columna]:
                suma += 1
        
        if suma >= (columnas // 2):
            
            if not antes:
                line += 1
            
            new[fila,:] = line
            antes = True
        else:
            antes = False
    return new
        
def eliminar_lineas():
    pass

imagen = common.abrir_imagen(IMAGEN)

#plt.imshow(imagen, cmap="binary")
#plt.show()

#sys.exit(0)
#input()

if len(imagen.shape) == 3:
    print("Convirtiendo a escala de grises...")
#    imagen = estadistica.rgb2gray(imagen)
    imagen = imagen[:,:,0]

print("invirtiendo xcolores...")
imagen = np.amax(imagen) - imagen

plt.imshow(imagen, cmap="gray")
plt.show()

print("Aplicando umbral...")


imagen[imagen<THRESH] = 0
imagen[imagen>=THRESH] = 1

plt.imshow(imagen, cmap="binary")
plt.show()

et, eti = etiquetar.etiquetar(imagen)

print(eti)
plt.imshow(et)
plt.show()


lineas = mayor(et, eti, (20, 200))
print(f"{len(lineas)} lineas encontradas")
for line in lineas:
    plt.imshow(line, cmap="binary")
    plt.show()
    lineas = find_lines(line)
    
    notas = morfo.core(line, KERNEL, "ero")
    notas = morfo.core(notas, KERNEL)
#
    plt.imshow(notas)
    plt.show()
    
    plt.imshow(lineas)
    plt.show()
    
    plt.imshow(lineas + notas)
    plt.show()