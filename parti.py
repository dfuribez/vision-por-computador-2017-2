import numpy as np

from core import estadistica  # RGB2Gray
from core import etiquetar  # Etiquetar elementos imagen binaria
from core import morfo  # Aplicar operaciones morfológicas
from core import common  # Operaciones comunes

from matplotlib import pyplot as plt

IMAGEN = "part.png"
THRESH = 1
KERNEL = np.array([[1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1]])

#KERNEL = np.ones((3, 3))

#KERNEL = np.array([[1, 1, 1]])
imagen = common.abrir_imagen(IMAGEN)

if len(imagen.shape) == 3:
    print("Convirtiendo a escala de grises...")
    imagen = estadistica.rgb2gray(imagen)

print("invirtiendo xcolores...")
imagen = np.amax(imagen) - imagen

plt.imshow(imagen, cmap="gray")
plt.show()

print("Aplicando umbral...")

imagen[imagen>=THRESH] = 1
imagen[imagen<THRESH] = 0

plt.imshow(imagen, cmap="gray")
plt.show()

print("Erosionando...")

#erosionado = imagen.copy()
notas = morfo.core(imagen, KERNEL, "ero")
notas = morfo.core(notas, KERNEL, "dil")

plt.imshow(notas, cmap="gray")
plt.show()


t_max = np.amax(notas)
t_min = np.amin(notas)

print(t_max)
print(t_min)

notas[notas==t_max] = 1
notas[notas==t_min] = 0

print(np.amax(notas))
print(np.amin(notas))

plt.subplot(121)
plt.imshow(imagen)
plt.subplot(122)
plt.imshow(notas)
plt.show()


print("Calculando líneas...")
lineas = imagen - notas

plt.imshow(lineas, cmap="gray")
plt.show()

print("Dilatando...")

