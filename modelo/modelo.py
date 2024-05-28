# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:55:47 2024

@author: paulo
"""

from .data_transform import ModeloDataset
from .database_manager import ModeloBDatos
from .train_model import ModeloEntrenamiento
from .prediction import ModeloPrediccion


class Modelo:
    def __init__(self):
        self.modeloBDatos = ModeloBDatos()
        self.modeloDataset = ModeloDataset()
        self.ModeloEntrenamiento = ModeloEntrenamiento()
        self.modeloPrediccion = ModeloPrediccion()