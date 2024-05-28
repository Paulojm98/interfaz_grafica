# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:44:04 2024

@author: paulo
"""

class ControladorPrediccion:
    def __init__(self, modelo_prediccion, vista_prediccion):
        self.modelo_prediccion = modelo_prediccion
        self.vista_prediccion = vista_prediccion

    def realizar_prediccion(self):
        self.modelo_prediccion.predecir()
        