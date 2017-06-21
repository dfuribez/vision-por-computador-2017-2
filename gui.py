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


from scipy import ndimage

from core import estadistica
from core import transformacion
from core import gui_trans
from core import filtros
from core import common

gui_class = uic.loadUiType("core/corel.ui")[0]

class Corel(QMainWindow, gui_class):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.imagen = None
        self.titulo = ""
        self.menu()
        
        # Figuras matplotlib
        self.foriginal = matplotlib.figure.Figure()
        self.fnuevo = matplotlib.figure.Figure()
        # FigureCanvas
        self.canvas_original = FigureCanvas(self.foriginal)
        self.canvas_nuevo = FigureCanvas(self.fnuevo)
        
        # Acciones
        self.actionAbrir.triggered.connect(self.abrir)
        self.actionRGB2Gray.triggered.connect(self.RGB2Gray)
        self.actionHistograma.triggered.connect(self.histograma)
        self.actionA.triggered.connect(self.a)
        self.actionB.triggered.connect(self.b)
        self.actionC.triggered.connect(self.c)
        self.actionD.triggered.connect(self.d)
        self.actionE.triggered.connect(self.e)
        self.actionEstadisticos.triggered.connect(self.estadisticos)
        self.btnPasar.clicked.connect(self.pasar)
        self.actionTransformar.triggered.connect(lambda x: self.window_trans.show())
        
        self.actionPromedio.triggered.connect(self.filtro_promedio)
        self.actionMediana.triggered.connect(self.filtro_mediana)
        self.actionModa.triggered.connect(self.filtro_moda)
        self.actionGauss.triggered.connect(self.filtro_gauss)
        self.actionUmbral.triggered.connect(self.umbral)
        self.actionContraste.triggered.connect(self.contraste)
        
        # Layouts
        self.imgOriginal.addWidget(self.canvas_original)
        self.imgNuevo.addWidget(self.canvas_nuevo)
        
        # transformaciones
        self.window_trans = gui_trans.Trans(self)
    
    def menu(self):
        menubar  = self.menuBar()
        
        # Acciones
        
        #actionPSimple= QAction(QIcon(None), "Promedio simple", self)
        #actionPSimple.setStatusTip("Promedio simple")
        #actionPSimple.triggered.connect(lambda x: print("Promedio simple"))
        
        #actionPPonderado = QAction(QIcon(None), "Promedio ponderado uno", self)
        #actionPPonderado.setStatusTip("Promedio ponderado uno")
        #actionPPonderado.triggered.connect(lambda x: print("Promedio ponderado uno"))
        
        # Agregar Memnus
        #transformaciones = menubar.addMenu("Transformaciones")
        #transformaciones.addAction(actionTransformar)
        
        #segmentacion = menubar.addMenu("Segmentar")
        #segmentacion.addAction(actionPSimple)
        #segmentacion.addAction(actionPPonderado)
    
    def pasar(self):
        self.imagen = self.nuevo
        self.draw_original(self.imagen, self.titulo)
        self.fnuevo.clf()
        self.canvas_nuevo.draw_idle()
    
    def dialogo(self):
        filename = QFileDialog.getOpenFileName(self, "Abrir archivo", ".")[0]
        print(filename)
        return filename
    
    def draw_original(self, img, titulo):
        self.foriginal.clf()
        plot = self.foriginal.add_subplot(111)
        plot.imshow(img, cmap="gray")
        plot.set_title(titulo)
        self.canvas_original.draw_idle()
    
    def draw_nuevo(self, img, titulo, mapa="gray"):
        self.nuevo = img
        self.titulo = titulo
        self.fnuevo.clf()
        plot = self.fnuevo.add_subplot(111)
        plot.imshow(img, cmap=mapa)
        plot.set_title(titulo)
        self.canvas_nuevo.draw_idle()

    def abrir(self):
        print("Abriendo lena...")
        # REseteo de variables
        self.mediana = 0
        self.moda = 0
        self.promedio = 0
        self.var = 0
        self.lblEstadistica.setText("")
        self.gray = None
        self.imagen = None
        
        #lena = "img/Lena.jpg"
        lena = self.dialogo()
        
        self.imagen =  ndimage.imread(lena)
        nombre = "{0}, ({1}, {2})".format(os.path.split(lena)[-1], *self.imagen.shape[:2])
        self.draw_original(self.imagen, nombre)
        mensaje = "Abierta: {0}, filas: {1}, columnas: {2}".format(nombre,
                                                                   *self.imagen.shape[:2])
        self.statusBar().showMessage(mensaje)
        
    
    def RGB2Gray(self):
        self.gray = estadistica.rgb2gray(self.imagen)
        self.draw_nuevo(self.gray, "Escala de grises")
    
    def histograma(self):
        histo = estadistica.histograma(self.imagen)
        self.fnuevo.clf()
        plot = self.fnuevo.add_subplot(111)
        plot.bar(np.arange(256), histo)
        plot.set_title("Histograma")
        self.canvas_nuevo.draw_idle()
        
    def a(self):
        mascara = self.gray >= 150
        nueva = self.gray.copy()
        nueva[mascara] = self.promedio
        self.draw_nuevo(nueva, "Mayores que 150 reciben promedio")
    
    def b(self):
        mascara = self.gray >= 150
        nueva = self.gray.copy()
        nueva[mascara] = self.mediana
        self.draw_nuevo(nueva, "Mayores que 150 reciben mediana")
    
    def c(self):
        mascara = self.gray >= 150
        nueva = self.gray.copy()
        nueva[mascara] = self.moda
        self.draw_nuevo(nueva, "Mayores que 150 reciben moda")

    def d(self):
        nueva = self.gray.copy()
        nueva[nueva >= self.promedio] = 255
        self.draw_nuevo(nueva, "Mayores que el promedio reciben blanco")
    
    def e(self):
        nueva = self.gray.copy()
        nueva[nueva >= self.promedio] = 255
        nueva[nueva <= self.promedio] = 0
        
        self.draw_nuevo(nueva, "Mayores que el promedio reciben blanco y menores negro")
    
    def estadisticos(self):
        gray = self.gray
        self.promedio = estadistica.media(gray)
        print("Media de la intensidad de los pixeles:", self.promedio)

        self.var = estadistica.varianza(gray, self.promedio)
        print("Varianza:", self.var)

        self.mediana = estadistica.mediana(gray)
        print("Mediana:", self.mediana)
        histo = estadistica.histograma(self.gray)
        self.moda = estadistica.moda(histo)
        print("Moda:", self.moda)
        
        text = "Promedio: {0}, Varianza: {1}, Mediana: {2}, Moda: {3}".format(self.promedio,
                                                                              self.var,
                                                                              self.mediana,
                                                                              self.moda)
        
        self.lblEstadistica.setText(text)
        
    def get(self, titulo):
        text, ok = QInputDialog.getText(self, "Input Dialog", titulo)
        if ok:
            text = str(text)
            if text.isdigit():
                return int(text)
            else:
                return False
        else:
            return None
    
    def filtro_promedio(self):
        texto = self.get("Ingrese el tamaño del filtro:")
        if texto is None:
            return
        
        if texto:
            new = filtros.promedio(self.imagen, texto)
            self.draw_nuevo(new, "Filtro del promedio kernel: {0}".format(texto))
        else:
            self.filtro_promedio()
            
    
    def filtro_moda(self):
        core = self.get("Ingrese el tamaño del filtro:")
        if core is None:
            return 
        
        if core:
            new = filtros.moda(self.imagen, core)
            self.draw_nuevo(new, f"filtro de la moda kernel {core}x{core}")
        else:
            self.filtro_moda(new, "")
            
    
    def filtro_mediana(self):
        core = self.get("Ingrese el tamaño del filtro:")
        if core is None:
            return 
        
        if core:
            new = filtros.mediana(self.imagen, core)
            self.draw_nuevo(new, "Filtro de la moda con kernel {0}x{0}".format(core))
        else:
            self.filtro_mediana()
            

    def filtro_gauss(self):
        new = filtros.gauss(self.imagen)
        self.draw_nuevo(new, "Filtro Gauss 3x3")
    
    def umbral(self):
        umbral = self.get("Elija  un umbral:")
        if umbral is None:
            return
        
        new = self.imagen.copy()
        
        if umbral:
            new[new > umbral] = 255
            new[new < umbral] = 0
            
            self.draw_nuevo(new, f"Umbralizada: {umbral}")
    
    def contraste(self):
        a = self.get("Ingrese el contraste")
        


app = QApplication(sys.argv)
corel = Corel(None)
corel.show()
app.exec_()
