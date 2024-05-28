# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 14:32:48 2024

@author: paulo
"""

import customtkinter as ctk
from tkinter import ttk
import pandas as pd
from utilidades.util_creacion_dataset import Util_creacion_dataset

class VistaDatasetDesign(ctk.CTkFrame):
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
        # Carpeta origen
        self.panel_izquierdo.grid_columnconfigure(2, weight=1)
        ctk.CTkLabel(self.panel_izquierdo, text="Carpeta origen:").grid(row=1, column=1, pady=5)
        self.entrada_origen = ctk.CTkEntry(self.panel_izquierdo,)
        self.entrada_origen.grid(row=1, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Carpeta destino:").grid(row=2, column=1, pady=5)
        self.entrada_destino = ctk.CTkEntry(self.panel_izquierdo)
        self.entrada_destino.grid(row=2, column=2, sticky="ew", pady=5)
        
        # Tipo de creación de características
        ctk.CTkLabel(self.panel_izquierdo, text="Tipo de creación de características:").grid(row=3, column=1, columnspan= 3, pady=5)
        self.tipo_creacion = ttk.Combobox(self.panel_izquierdo, 
                                          values=["Transformada de Wavelet", "Transformada de Fourier"],
                                          state="readonly", width=45)
        self.tipo_creacion.grid(row=4, column=1, columnspan=3,pady=5)
        
        # Variable para el estado del checkbox de ClassName
        self.check_filtro = ctk.IntVar()
        self.checkbutton_filtro = ctk.CTkCheckBox(self.panel_izquierdo, text="¿Quieres aplicar filtros?", variable=self.check_filtro)
        self.checkbutton_filtro.grid(row=5, column=1, columnspan=3, pady=5)
        
        # Filtro por rango de Frecuencia
        ctk.CTkLabel(self.panel_izquierdo, text="Frecuencia mínima:").grid(row=6, column=1, pady=5)
        self.frecuencia_min_entry = ctk.CTkEntry(self.panel_izquierdo)
        self.frecuencia_min_entry.grid(row=6, column=2, sticky="ew", pady=5)
        self.frecuencia_min_entry.configure(state='disabled')
    
        ctk.CTkLabel(self.panel_izquierdo, text="Frecuencia máxima:").grid(row=7, column=1, pady=5)
        self.frecuencia_max_entry = ctk.CTkEntry(self.panel_izquierdo)
        self.frecuencia_max_entry.grid(row=7, column=2, sticky="ew", pady=5)
        self.frecuencia_max_entry.configure(state='disabled')
    
        # Filtro por rango de Ciclos
        ctk.CTkLabel(self.panel_izquierdo, text="Ciclos mínimo:").grid(row=8, column=1, pady=5)
        self.ciclos_min_entry = ctk.CTkEntry(self.panel_izquierdo)
        self.ciclos_min_entry.grid(row=8, column=2, sticky="ew", pady=5)
        self.ciclos_min_entry.configure(state='disabled')
        
    
        ctk.CTkLabel(self.panel_izquierdo, text="Ciclos máximo:").grid(row=9, column=1, pady=5)
        self.ciclos_max_entry = ctk.CTkEntry(self.panel_izquierdo)
        self.ciclos_max_entry.grid(row=9, column=2, sticky="ew", pady=5)
        self.ciclos_max_entry.configure(state='disabled')
        
        #Botón para iniciar la creación del dataset
        self.button_crear = ctk.CTkButton(self.panel_izquierdo, text="Crear Dataset")
        self.button_crear.grid(row=10, column=2, pady=10)
        
    def controles_panel_derecho(self):
        self.label_panel_dch1 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
        # Segundo label justo debajo del primero en panel_derecho
        self.label_panel_dch2 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.label_panel_dch3 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch3.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    
        
        
    
            