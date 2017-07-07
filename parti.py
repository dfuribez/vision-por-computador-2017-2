import numpy as np


from core import estadistica  # RGB2Gray
from core import etiquetar  # Etiquetar elementos imagen binaria
from core import morfo  # Aplicar operaciones morfológicas
from core import common  # Operaciones comunes

from matplotlib import pyplot as plt
from scipy.misc import imsave

plt.axis("off")

IMAGEN = "img/partituras/burro_partitura1.jpg"
#IMAGEN = "img/partituras/tetris.jpg"
IMAGEN = "part.png"
IMAGEN = "part4.png"
THRESH = 100
KERNEL = np.array([[1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1]])

NOMBRES = [0, "FA", "RE", "SI", "SOL", "MI"]
NOMBRES_M = [0, "MI", "DO", "LA", "FA", "--"]

def mayor(et, eti, umbral):
    
    encontrados = []
    u_filas, u_columnas = umbral
    for etiqueta in eti:
        roi, _ = etiquetar.roi(et, etiqueta)
        filas, columnas = roi.shape
        if filas >= u_filas and columnas >= u_columnas:
            encontrados.append(roi)
    
    return encontrados
            
def find_lines(parte):
    filas, columnas = parte.shape
    new = np.zeros((filas, columnas))
    line = 1
    antes = False
    notas = {
        1: 0,  # FA
        2: 0,  # RE
        3: 0,  # SI
        4: 0,  # SOL
        5: 0,  # MI
    }

    for fila in range(filas):
        suma = 0
        for columna in range(columnas):
            if parte[fila, columna]:
                suma += 1
        
        if suma >= (columnas // 2):
            
            if not antes:
                notas[line] = fila
                line += 1
                
            
            new[fila,:] = line
            antes = True
        else:
            antes = False
    return new, notas
        
def get_note(lineas, coors, prom):
    fila_prom = (coors[0][0] + coors[0][1]) // 2
    nota = None
    for x in range(1, 5):
        if lineas[x] - prom <= fila_prom <= lineas[x] + prom:
            nota = NOMBRES[x]
        elif lineas[x+1] - prom < fila_prom < lineas[x+1] + prom:
            nota = NOMBRES[x+1]
        elif lineas[x] < fila_prom < lineas[x+1]:
            nota = NOMBRES_M[x]
        else:
            pass
            #print(None)
        if nota is not None:
            return fila_prom, nota
    return fila_prom, None

def dist_prom(notas):
    dist = 0
    for x in range(1, 5):
        dist += abs(notas[x] - notas[x+1])
    return dist // 5

imagen = common.abrir_imagen(IMAGEN)


if len(imagen.shape) == 3:
    print("Convirtiendo a escala de grises...")
#    imagen = estadistica.rgb2gray(imagen)
    imagen = imagen[:,:,0]

print("invirtiendo xcolores...")
imagen = np.amax(imagen) - imagen

plt.axis("off")
plt.imshow(imagen, cmap="gray")
plt.show()

print("Aplicando umbral...")


imagen[imagen<THRESH] = 0
imagen[imagen>=THRESH] = 1

plt.axis("off")
plt.imshow(imagen, cmap="binary")
plt.show()

et, eti = etiquetar.etiquetar(imagen)
imsave("etiquetada.png", et)
plt.imshow(et)
plt.show()


lineas = mayor(et, eti, (20, 200))
print(f"{len(lineas)} lineas encontradas")
for line in lineas:
    plt.axis("off")
    plt.imshow(line, cmap="binary")
    plt.show()
    linea_notas, coor_notas = find_lines(line)
    plt.axis("off")
    plt.imshow(linea_notas)
    plt.show()
    prom =  dist_prom(coor_notas) // 3
    notas = morfo.core(line, KERNEL, "ero")
    notas[notas<10] = 0
    notas[notas>=10] = 1
    notas, _ = etiquetar.etiquetar(notas)
    plt.axis("off")
    plt.imshow(notas)
    plt.show()
    filas, columnas = notas.shape
    recorridos = []
    b_notas = []
    for columna in range(columnas):
        for fila in range(filas):
            pixel = notas[fila, columna]
            if pixel:
                if not pixel in recorridos:
                    recorridos.append(pixel)
                    roi, coors = etiquetar.roi(notas, pixel)
                    cx, note = get_note(coor_notas, coors, prom)
                    if note is not None:
                        b_notas.append(note)
                    linea_notas[int(cx), columna] = 10
    print(", ".join(b_notas))
    plt.axis("off")
    plt.imshow(line, cmap="binary")
    plt.show()

