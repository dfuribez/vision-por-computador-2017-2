#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy import ndimage

def abrir_imagen(ruta):
    """Funcion que abre una imagen y devuelve su matriz"""
    imagen = ndimage.imread(ruta)
    return imagen

def is_num(text):
    buffer = text
        
    for char in ["-", ",", "."]:
        buffer = buffer.replace(char, "")
    
    if buffer.isdigit():
        return float(text)
    else:
        return None

def is_int(text):
    if text.isdigit():
        return int(text)
    else:
        return None

