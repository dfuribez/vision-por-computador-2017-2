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
from core import bordes

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
        self.actionContraste.triggered.connect(lambda x: self.contraste(True))
        self.actionBrillo.triggered.connect(lambda x: self.contraste(False))
        self.actionPsimple.triggered.connect(self.gray_simple)
        self.actionPUno.triggered.connect(self.gray_uno)
        self.actionPDos.triggered.connect(self.gray_dos)
        self.actionRoberts.triggered.connect(lambda x: self.calcular_bordes("roberts"))
        self.actionSobel.triggered.connect(lambda x: self.calcular_bordes("sobel"))
        self.actionKirsch.triggered.connect(lambda x: self.calcular_bordes("kirsch"))
        self.actionRobinson.triggered.connect(lambda x: self.calcular_bordes("robinson"))
        
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
    
    def gray_simple(self):
        self.gray = estadistica.rgb2gray(self.imagen)
        self.draw_nuevo(self.gray, "Escala de grises, promedio")
    
    def gray_uno(self):
        self.gray = estadistica.rgb2gray_uno(self.imagen)
        self.draw_nuevo(self.gray, "Escala de grises, ponderado uno")
    
    def gray_dos(self):
        self.gray = estadistica.rgb2gray_dos(self.imagen)
        self.draw_nuevo(self.gray, "Escala de grises, ponderado dos")
    
    
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
        if self.gray is not None:
            gray = self.gray
        else:
            gray = estadistica.rgb2gray(self.imagen)

        self.promedio = estadistica.media(gray)
        print("Media de la intensidad de los pixeles:", self.promedio)

        self.var = estadistica.varianza(gray, self.promedio)
        print("Varianza:", self.var)

        self.mediana = estadistica.mediana(gray)
        print("Mediana:", self.mediana)
        histo = estadistica.histograma(self.gray)
        self.moda = estadistica.moda(histo)
        print("Moda:", self.moda)
        
        text = "Promedio: {0}, Varianza: {1}, Mediana: {2}, Moda:{3}".format(self.promedio,
                                                                              self.var,
                                                                              self.mediana,
                                                                              self.moda)
        
        self.lblEstadistica.setText(text)
        
    def get(self, titulo):
        text, ok = QInputDialog.getText(self, "Input Dialog", titulo)
        if ok:
            return str(text)
        else:
            return None
    
    def filtro_promedio(self):
        core = self.get("Ingrese el tamaño del filtro:")
        if core is None:
            return
        
        core = common.is_int(core)
        
        if core is not None:
            new = filtros.promedio(self.imagen, core)
            self.draw_nuevo(new, "Filtro del promedio kernel: {0}".format(core))
        else:
            self.filtro_promedio()
            
    
    def filtro_moda(self):
        core = self.get("Ingrese el tamaño del filtro:")
        
        if core is None:
            return 
        
        core = common.is_int(core)
        
        if core is not None:
            new = filtros.moda(self.imagen, core)
            self.draw_nuevo(new, f"filtro de la moda kernel {core}x{core}")
        else:
            self.filtro_moda(new)
            
    
    def filtro_mediana(self):
        core = self.get("Ingrese el tamaño del filtro:")
        if core is None:
            return 
        
        core = common.is_int(core)
        
        if core is not None:
            new = filtros.mediana(self.imagen, core)
            self.draw_nuevo(new, "Filtro de la moda con kernel {0}x{0}".format(core))
        else:
            self.filtro_mediana()
            

    def filtro_gauss(self):
        new = filtros.gauss(self.imagen)
        self.draw_nuevo(new, "Filtro Gauss 3x3")
    
    def umbral(self):
        umbral = self.get("Elija  un umbral <inf>-<sup> o <limite>:")
        if umbral is None:
            return
        
        new = self.imagen.copy()
        
        if "-" in umbral:
            umbrales = umbral.split("-")
            
            if len(umbrales) == 2:
                u1, u2 = map(int, umbrales)
                if u1 > u2:
                    buff_mayor = new < u1
                    buff_menor = new > u2
                else:
                    buff_mayor = new < u2
                    buff_menor = new > u1
                
                mascara = np.logical_and(buff_mayor, buff_menor)
                new[mascara] = 255
                
                mascara = np.logical_not(mascara)
                new[mascara] = 0
                
                titulo = f"umbralizada entre {u1} y {u2}"
            else:
                self.umbral()
        else:
            
            umbral = common.is_int(umbral)
            
            if umbral is not None:
                new[new > umbral] = 255
                new[new < umbral] = 0
                
                titulo = f"Umbralizada: {umbral}"
            else:
                self.umbral()
        
        self.draw_nuevo(new, titulo)
    
    def contraste(self, contraste=True):
        
        if contraste:
            titulo = "contraste"
        else:
            titulo = "brillo"
            
        valor = self.get(f"Ingrese el {titulo}:")
        
        if valor is None:
            return 
        
        valor = common.is_num(valor)
        
        if valor is not None:
            if contraste:
                a, b = valor, 0
            else:
                a, b = 1, valor
            
            new = filtros.brillo_contraste(self.imagen, a, b)
                
            self.draw_nuevo(new, f"{titulo} modificado en {valor}")
        else:
            self.contraste()
    
    def calcular_bordes(self, tipo):
        umbral = self.get("Seleccione el umbral:")
        if umbral is None:
            return
        
        umbral = common.is_int(umbral)
        if umbral is not None:
            im_bordes = bordes.core(self.imagen, tipo, umbral)
            self.draw_nuevo(im_bordes, f"Bordes {tipo}, umbral: {umbral}")
        else:
            self.calcular_bordes(tipo)

app = QApplication(sys.argv)
corel = Corel(None)
corel.show()
app.exec_()
