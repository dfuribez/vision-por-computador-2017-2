import sys
import numpy as np
import math
from PyQt5 import QtCore, uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

from core import transformacion
from core import common


trans_class = uic.loadUiType("gui/ui/transformacion.ui")[0]

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
        self.chkInter.hide()
        
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
        if elemento == "Escalado":
            self.chkInter.show()
        else:
            self.chkInter.hide()
                
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

                angulo %= 180
                if angulo == 0:
                    angulo = 180
                
                if angulo > 90:
                    off_filas = abs(math.ceil(columnas * math.cos(math.radians(angulo))))
                    off_columnas = 0
                else:
                    off_columnas = math.ceil(filas * math.sin(math.radians(angulo)))
                    off_filas = 0
                
                t1 = abs(int(columnas * math.sin(math.radians(angulo))) + 1)
                t2 = abs(int(filas * math.cos(math.radians(angulo))) + 1)
                nuevo_x = t1 + t2

                t11 = abs(int(columnas * math.cos(math.radians(angulo))) + 1)
                t22 = abs(int(filas * math.sin(math.radians(angulo))) + 1)

                nuevo_y = t11 + t22
                
                mat = transformacion.mat_rotacion_z(angulo)
                trans = transformacion.core(img, mat,
                                            nuevo_x, nuevo_y,
                                            off_columnas=off_columnas,
                                            off_filas=off_filas)

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
            escala = str(self.txtEscala.toPlainText())
            
            if escala:
                escala = common.is_num(escala)
            
            
            if escala:
                factor = escala
                mat = np.identity(3) * escala
#                print(factor, 20 * factor)
#                print(mat)
                new_filas = math.ceil(filas * factor)
                new_columnas = math.ceil(columnas * factor)
                
                trans = transformacion.core(img, mat, new_filas, new_columnas)
                if factor > 1 and self.chkInter.isChecked():
                    trans = transformacion.interpolar(trans, int(factor))
                self.padre.draw_nuevo(trans, "Escalado por {0}".format(factor))
            else:
                self.mostrar_mensaje("La escala debe ser un número")
        
        # TRaslacion
        if self.last == "Traslacion":
            texto_x = str(self.txtX.toPlainText())
            texto_y = str(self.txtY.toPlainText())
            
            tx, ty = None, None
    
            
            if texto_x.isdigit():
                tx = int(texto_x)
            
            if texto_y.isdigit():
                ty = int(texto_y)
            
            if any((tx, ty)):
                mat = np.identity(3)
                filas, columnas = img.shape[:2]
                n_columnas, n_filas = None, None
                if tx is not None:
                    mat[2, 1] = tx
                    n_columnas = int(columnas + tx)
                
                if ty is not None:
                    mat[2, 0] = ty
                    n_filas = int(filas + ty)
                
                new = transformacion.core(img, mat, n_filas, n_columnas)
                self.padre.draw_nuevo(new, f"TRaslación x: {tx}, y: {ty}")
            else:
                self.mostrar_mensaje("Falta número")
                
            
            
    def mostrar_mensaje(self, mensaje):
        self.statusBar().showMessage(mensaje)
            
            
