#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def is_num(text):
    buffer = text
        
    for char in ["-", ",", "."]:
        buffer = buffer.replace(char, "")
    
    if buffer.isdigit():
        return text
    else:
        return False

def is_int(text):
    if text.isdigit():
        return true
    else:
        return False

