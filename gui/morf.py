import sys
import numpy as np
import math
from PyQt5 import QtCore, uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

from core import morfo
from core import common

morf_class = uic.loadUiType("gui/ui/morfologia.ui")[0]

CRUZ = np.array([[0, 1, 0],
                 [1, 1, 1],
                 [0, 1, 0]])

DIAGONAL = np.array([[1, 0, 1],
                     [0, 1, 0],
                     [1, 0, 1]])

CUADRADO = np.ones((3, 3))

class Morfo(QMainWindow, morf_class):
    
    def __init__(self, padre=None):
        self.padre = padre
        QMainWindow.__init__(self, padre)
        
        self.setupUi(self)
        
        self.OP = {"Erosion": self.erosion,
              "Dilatacion": self.dilatacion,
              "Apertura": self.apertura,
              "Cerradura": self.cierre,
            }
        
        self.cmdAceptar.clicked.connect(self.boton)
        self.cmdCuadrado.clicked.connect(lambda x: self.array2text(CUADRADO))
        self.cmdCruz.clicked.connect(lambda x: self.array2text(CRUZ))
        self.cmdDiagonal.clicked.connect(lambda x: self.array2text(DIAGONAL))
        
        
    def text2array(self):
        texto = str(self.txtElemento.toPlainText())
        texto = texto.split()
        filas = len(texto)
        
        len_columnas = list(map(len, texto))
        
        if not filas % 2 or not len_columnas[0] % 2:
            self.mostrar_mensaje("Se necesitas dimensiones impares")
            return None
        
        if not all(x.isdigit() for x in "".join(texto)):
            self.mostrar_mensaje("Los elementos deben ser numéricos")
            return None
        
        
        if texto:
            if  len_columnas == [len_columnas[0]] * filas:
                columnas = len(texto[0])
                estructurante = np.array([int(x) for x in "".join(texto)])
                estructurante = estructurante.reshape(filas, columnas)
                print(estructurante)
                return estructurante
            else:
                self.mostrar_mensaje("Las columnas no tienen la misma longitud")
        else:
            self.mostrar_mensaje("El elemento no puede estar vacío")
        
        return None
    
    def array2text(self, elemento):
        filas, columnas = elemento.shape
        buffer = ""
        for fila in range(filas):
            for columna in range(columnas):
                buffer += str(int(elemento[fila, columna]))
            buffer += "\r\n"
        self.txtElemento.clear()
        self.txtElemento.appendPlainText(buffer)
        print(buffer)

    def boton(self):
        kernel = self.text2array()
        if kernel is None:
            return
        
        if self.rdCierre.isChecked():
            opcion = "Cerradura"
        
        if self.rdDilatacion.isChecked():
            opcion = "Dilatacion"
        
        if self.rdErosion.isChecked():
            opcion = "Erosion"
        
        if self.rdApertura.isChecked():
            opcion = "Apertura"
        
        if self.padre.imagen is not None:
            self.seleccionado(opcion, kernel)
        else:
            self.mostrar_mensaje("Abra primero la imagen")
    
    def seleccionado(self, opcion, kernel):
        img = self.padre.imagen
        iteraciones = str(self.txtIter.toPlainText())
        if iteraciones.isdigit():
            iteraciones = int(iteraciones)
            new = self.OP[opcion](img, kernel)
            for _ in range(iteraciones - 1):
                new = self.OP[opcion](new, kernel)
            self.padre.draw_nuevo(new, "Morfologica")
        else:
            self.mostrar_mensaje("Número de iteraciones inválidas, asignando 1")
    
    def cierre(self, img, kernel):
        cerrado = morfo.core(img, kernel, "dil")
        cerrado = morfo.core(cerrado, kernel, "ero")
        return cerrado
    
    def apertura(self, img, kernel):
        abierto = morfo.core(img, kernel, "ero")
        abierto = morfo.core(abierto, kernel, "ero")
        return abierto
    
    def erosion(self, img, kernel):
        erosionado = morfo.core(img, kernel, "ero")
        return erosionado
    
    def dilatacion(self, img, kernel):
        dilatado = morfo.core(img, kernel, "dil")
        return  dilatado
    
    def mostrar_mensaje(self, mensaje):
        self.statusBar().showMessage(mensaje)
        
        
        
        
        
        
