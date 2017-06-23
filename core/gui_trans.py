import sys
import numpy as np
import math
from PyQt5 import QtCore, uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

from core import transformacion

trans_class = uic.loadUiType("core/t1.ui")[0]

class Trans(QMainWindow, trans_class):
    
    def __init__(self, parent=None):
        self.padre = parent
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        
        self.elementos = {
            "Traslacion": self.frmTraslacion,
            "Rotacion": self.frmRotacion,
            "Reflexion": self.frmReflexion,
            "Escalado": self.frmEscalado
        }
        
        self.frmRotacion.hide()
        self.frmEscalado.hide()
        self.frmTraslacion.hide()
        self.frmReflexion.hide()
        
        # Acciones
        
        self.optTraslacion.toggled.connect(lambda x: self.mostrar("Traslacion"))
        self.optRotacion.toggled.connect(lambda x: self.mostrar("Rotacion"))
        self.optReflexion.toggled.connect(lambda x: self.mostrar("Reflexion"))
        self.optEscalado.toggled.connect(lambda x: self.mostrar("Escalado"))

        self.btnAceptar.clicked.connect(self.comprobar)
        
        self.last = "Rotacion"
        self.mostrar(self.last)
    
    def mostrar(self, elemento):
        self.last = elemento
        self.setWindowTitle(elemento)
        
        for actual in self.elementos:
            if actual == elemento:
                self.layout.addWidget(self.elementos[actual])
                self.elementos[actual].show()
            else:
                self.elementos[actual].hide()
                
    def comprobar(self):
        ref_x = False
        ref_y = False
        if self.padre.imagen is None:
            self.mostrar_mensaje("Abra primero la imagen a transformar")
            return
        else:
            img = self.padre.imagen
            filas, columnas = img.shape[:2]
        
        
        # Rotacion
        if self.last == "Rotacion":
            texto = str(self.txtAngulo.toPlainText())
            if not texto.isdigit():
                self.mostrar_mensaje("En ángulo debe ser un número")
            else:
                angulo = float(texto)
                t1 = abs(int(columnas * math.sin(math.radians(angulo))) + 1)
                t2 = abs(int(filas * math.cos(math.radians(angulo))) + 1)
                nuevo_x = t1 + t2

                t11 = abs(int(columnas * math.cos(math.radians(angulo))) + 1)
                t22 = abs(int(filas * math.sin(math.radians(angulo))) + 1)

                nuevo_y = t11 + t22
                off_columnas = math.ceil(filas * math.sin(math.radians(angulo)))
                

                mat = transformacion.mat_rotacion_z(angulo)
                trans = transformacion.core(img, mat,
                                            nuevo_x, nuevo_y,
                                            off_columnas=off_columnas)

                self.padre.draw_nuevo(trans, "Rotacion: {0} grados".format(angulo))

        # Reflexion
        if self.last == "Reflexion":
            if self.chkX.isChecked():
                ref_x = True
            if self.chkY.isChecked():
                ref_y = True
            
            if not ref_y and not ref_x:
                self.mostrar_mensaje("Debe seleccionar una opción")
                return 
            
            mat = transformacion.mat_ref(ref_x, ref_y)
            trans = transformacion.core(img, mat)
            self.padre.draw_nuevo(trans, "Reflexion")
        
        # Escalado
        if self.last == "Escalado":
            texto = str(self.txtEscala.toPlainText())
            if texto.isdigit():
                factor = int(texto)
                mat = np.identity(3) * factor
                trans = transformacion.core(img, mat, filas*factor, columnas*factor)
                self.padre.draw_nuevo(trans, "Escalado por {0}".format(factor))
            else:
                self.mostrar_mensaje("La escala debe ser un número")
        
        # TRaslacion
        if self.last == "Traslacion":
            texto_x = str(self.txtX.toPlainText())
            texto_y = str(self.txtY.toPlainText())
            
            if texto_x.isdigit():
                tx = int(texto_x)
            
            if texto_y.isdigit():
                ty = int(texto_y)
            
            
    def mostrar_mensaje(self, mensaje):
        self.statusBar().showMessage(mensaje)
            
            
