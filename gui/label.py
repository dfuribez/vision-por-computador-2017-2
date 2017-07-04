import os
import sys
import numpy as np

from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon

import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from core import etiquetar

gui_label = uic.loadUiType("gui/ui/label.ui")[0]

class Label(QMainWindow, gui_label):
    
    def __init__(self, parent=None, etiquetada=None, elementos=[]):
        self.padre = parent
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.felemento = matplotlib.figure.Figure()
        self.canvas_elemento = FigureCanvas(self.felemento)
        
        self.etiquetada = etiquetada
        self.elementos = elementos
        
        
        self.cmbElemento.activated.connect(self.seleccionado)
        
        self.layout.addWidget(self.canvas_elemento)
        #self.lblPropiedades.setText("assad\r\nasdasda\r\nadasda\r\nasdasdasd")
        
        self.combo()
    
    def draw_elemento(self, elemento, titulo="Elemento"):
        self.elemento = elemento
        self.felemento.clf()
        plot = self.felemento.add_subplot(111)
        plot.imshow(elemento, cmap="binary")
        plot.set_title(titulo)
        self.canvas_elemento.draw_idle()
    
    def seleccionado(self):
        etiqueta = self.cmbElemento.currentText()
        
        elemento = etiquetar.roi(self.etiquetada, int(etiqueta))
        self.draw_elemento(elemento)
        p = self.propiedades(elemento)
        self.lblPropiedades.setText(p)
    
    def combo(self):
        self.cmbElemento.clear()
        self.cmbElemento.addItems(map(str, self.elementos))
        self.setWindowTitle(f"{len(self.elementos)} elementos.")
    
    def propiedades(self, img):
        
        area = etiquetar.area(img)
        perimetro = etiquetar.perimetro(img)
        cx, cy = etiquetar.centroide(img)
        if perimetro == 0:
            circu = 0
        else:
            circu = (4 * 3.1416 * area) / (perimetro ** 2)
        filas, columnas = img.shape
        rec = area / (filas * columnas)
        return f"Área: {area}\r\nPerimetro: {perimetro}\r\nCentroide: ({cx:.2f}, {cy:.2f})\r\nCircularidad: {circu:.4f}\r\nDimensiones: ({filas}, {columnas})\r\nRectangularidad: {rec:.2f}"
        
        
