# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:20:46 2024

@author: paulo
"""

import customtkinter as ctk
from tkinter import ttk
import pandas as pd
from utilidades.util_entrenamiento_red import Util_entrenamiento_red

class VistaEntrenamientoDesign(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paneles()
        self.controles_panel_izquierdo()
        self.controles_panel_derecho()
        
    def paneles(self):
        # Crear dos paneles (frames) dentro del panel principal
        self.panel_izquierdo = ctk.CTkFrame(self, width=250)
        self.panel_derecho = ctk.CTkFrame(self)
        
        self.panel_izquierdo.pack(side=ctk.LEFT, fill='y')
        self.panel_derecho.pack(side=ctk.RIGHT, fill='both', expand=True)
        
        
    def controles_panel_izquierdo(self):
        
        self.panel_izquierdo.grid_columnconfigure(2, weight=1)
        
        #Nombre del modelo para el guardado
        ctk.CTkLabel(self.panel_izquierdo, text="Nombre modelo:").grid(row=1, column=1, pady=5)
        self.entry_nombre_modelo = ctk.CTkEntry(self.panel_izquierdo,)
        self.entry_nombre_modelo.grid(row=1, column=2, sticky="ew", pady=5)
        
        # Carpeta origen
        ctk.CTkLabel(self.panel_izquierdo, text="Carpeta origen:").grid(row=2, column=1, pady=5)
        self.entrada_origen = ctk.CTkEntry(self.panel_izquierdo,)
        self.entrada_origen.grid(row=2, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Carpeta destino:").grid(row=3, column=1, pady=5)
        self.entrada_destino = ctk.CTkEntry(self.panel_izquierdo)
        self.entrada_destino.grid(row=3, column=2, sticky="ew", pady=5)
        
        # Tipo de creación de características
        ctk.CTkLabel(self.panel_izquierdo, text="Tipo de modelo:").grid(row=4, column=1, columnspan= 3, pady=5)
        self.tipo_creacion = ttk.Combobox(self.panel_izquierdo, 
                                          values=["CNN-TWavelet-Imagen", "CNN-TFourier-Imagen"],
                                          state="readonly", width=45)
        self.tipo_creacion.grid(row=5, column=1, columnspan=3,pady=5)
        
        
        # Filtro por rango de Frecuencia
        ctk.CTkLabel(self.panel_izquierdo, text="Épocas:").grid(row=6, column=1, pady=5)
        self.entry_epocas = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_epocas.grid(row=6, column=2, sticky="ew", pady=5)
    
        ctk.CTkLabel(self.panel_izquierdo, text="Tamaño lote:").grid(row=7, column=1, pady=5)
        self.entry_batch_size = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_batch_size.grid(row=7, column=2, sticky="ew", pady=5)
        
        ctk.CTkLabel(self.panel_izquierdo, text="Learning rate:").grid(row=8, column=1, pady=5)
        self.entry_learning_rate = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_learning_rate.grid(row=8, column=2, sticky="ew", pady=5)
    
        # Filtro por rango de Ciclos
        ctk.CTkLabel(self.panel_izquierdo, text="Porcentaje Validación:").grid(row=9, column=1, pady=5)
        self.entry_validation_split = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_validation_split.grid(row=9, column=2, sticky="ew", pady=5)
        
        # Variable para el estado del checkbox de ClassName
        self.check_filtro = ctk.IntVar()
        self.checkbutton_semilla = ctk.CTkCheckBox(self.panel_izquierdo, text="¿Quieres aplicar una semilla?", variable=self.check_filtro)
        self.checkbutton_semilla.grid(row=10, column=1, columnspan=3, pady=5)
        
        # Semilla de reproducibilidad
        ctk.CTkLabel(self.panel_izquierdo, text="Valor de semilla:").grid(row=11, column=1, pady=5)
        self.entry_semilla = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_semilla.grid(row=11, column=2, sticky="ew", pady=5)
        self.entry_semilla.configure(state='disabled')
        
        #Botón para iniciar la creación del dataset
        self.button_entrenar = ctk.CTkButton(self.panel_izquierdo, text="Entrenar")
        self.button_entrenar.grid(row=12, column=2, pady=10)
        
    def controles_panel_derecho(self):
        self.panel_derecho.grid_rowconfigure(2, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        self.label_panel_dch1 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
        # Segundo label justo debajo del primero en panel_derecho
        self.label_panel_dch2 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        
        self.textbox_logs_train = ctk.CTkTextbox(self.panel_derecho,wrap="word" )
        self.textbox_logs_train.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox_logs_train.configure(state="disabled")

    
    