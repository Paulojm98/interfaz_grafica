# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:51:18 2024

@author: paulo
"""

import customtkinter as ctk
from tkinter import ttk

class VistaBDatosDesign(ctk.CTkFrame):
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
        # Ubicación datos de entrenamiento
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación datos entrenamiento:").grid(row=1, column=1, pady=5)
        self.entry_data_train = ctk.CTkEntry(self.panel_izquierdo,)
        self.entry_data_train.grid(row=1, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación destino:").grid(row=2, column=1, pady=5)
        self.entry_destino_train = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_destino_train.grid(row=2, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Nombre csv entrenamiento:").grid(row=3, column=1, pady=5)
        self.entry_nombre_train = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_nombre_train.grid(row=3, column=2, sticky="ew", pady=5)
        
        #Botón para iniciar la creación del dataset
        self.button_crear_db_train = ctk.CTkButton(self.panel_izquierdo, text="Crear CSV Entrenamiento")
        self.button_crear_db_train.grid(row=4, column=2, pady=10)
        
        # Ubicación datos de test
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación datos test:").grid(row=5, column=1, pady=5)
        self.entry_data_test = ctk.CTkEntry(self.panel_izquierdo,)
        self.entry_data_test.grid(row=5, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación destino:").grid(row=6, column=1, pady=5)
        self.entry_destino_test = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_destino_test.grid(row=6, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Nombre csv test:").grid(row=7, column=1, pady=5)
        self.entry_nombre_test = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_nombre_test.grid(row=7, column=2, sticky="ew", pady=5)
        
        #Botón para iniciar la creación del dataset
        self.button_crear_db_test = ctk.CTkButton(self.panel_izquierdo, text="Crear CSV Test")
        self.button_crear_db_test.grid(row=8, column=2, pady=10)
        
        
        
    def controles_panel_derecho(self):
        # Configuración de grid en panel_derecho para que el Treeview se expanda
        
        self.label_panel_dch1 = ctk.CTkLabel(self.panel_derecho, text="", anchor="center")
        self.label_panel_dch1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
        # Segundo label justo debajo del primero en panel_derecho
        self.label_panel_dch2 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
        # Treeview que ocupa el espacio restante en panel_derecho
        self.tree = ttk.Treeview(self.panel_derecho)
        #self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.scrollbar = ttk.Scrollbar(self.panel_derecho, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.panel_derecho.grid_rowconfigure(2, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        

        
            