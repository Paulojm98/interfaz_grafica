# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:28:30 2024

@author: paulo
"""

import customtkinter as ctk
from tkinter import ttk
import pandas as pd
from utilidades.util_entrenamiento_red import Util_entrenamiento_red

class VistaPrediccionDesign(ctk.CTkFrame):
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
        
        # Carpeta origen
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación Modelo:").grid(row=1, column=1, pady=5)
        self.entrada_origen = ctk.CTkEntry(self.panel_izquierdo,)
        self.entrada_origen.grid(row=1, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación datos test:").grid(row=2, column=1, pady=5)
        self.entrada_destino = ctk.CTkEntry(self.panel_izquierdo)
        self.entrada_destino.grid(row=2, column=2, sticky="ew", pady=5)
        
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
    
        # Filtro por rango de Ciclos
        ctk.CTkLabel(self.panel_izquierdo, text="Porcentaje Validación:").grid(row=8, column=1, pady=5)
        self.entry_validation_split = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_validation_split.grid(row=8, column=2, sticky="ew", pady=5)
        
        # Variable para el estado del checkbox de ClassName
        self.check_filtro = ctk.IntVar()
        checkbutton_semilla = ctk.CTkCheckBox(self.panel_izquierdo, text="¿Quieres aplicar una semilla?", variable=self.check_filtro,
                                              command=self.toggle_fields)
        checkbutton_semilla.grid(row=9, column=1, columnspan=3, pady=5)
        
        # Semilla de reproducibilidad
        ctk.CTkLabel(self.panel_izquierdo, text="Valor de semilla:").grid(row=10, column=1, pady=5)
        self.entry_semilla = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_semilla.grid(row=10, column=2, sticky="ew", pady=5)
        self.entry_semilla.configure(state='disabled')
        
        #Botón para iniciar la creación del dataset
        self.button_entrenar = ctk.CTkButton(self.panel_izquierdo, text="Entrenar", command=self.entrenar_red)
        self.button_entrenar.grid(row=11, column=2, pady=10)
        
    def controles_panel_derecho(self):
        label_panel_dch = ctk.CTkLabel(self.panel_derecho, text="Información de la red creada",
                                text_color="black", font=("Roboto", 24, "bold"))

        # Empaqueta el label en el centro del panel del cuerpo principal
        label_panel_dch.pack(expand=True)

    
    def entrenar_red(self):
        self.limpiar_panel(self.panel_derecho)
        origen = self.entrada_origen.get()
        destino = self.entrada_destino.get()
        nombre_modelo = self.entry_nombre_modelo.get()
        tipo_caracteristicas = self.tipo_creacion.get()
        epocas = int(self.entry_epocas.get())
        batch_size = int(self.entry_batch_size.get())
        validation_split = float(self.entry_validation_split.get())
        semilla = None
        if self.check_filtro.get() == 1:
            try:
                semilla = int(self.entry_semilla.get())
                
            except ValueError:
                print("Por favor, asegúrate de que todos los campos son números válidos")
                return  # Salir de la función si la conversión falla
            
        Util_entrenamiento_red(origen, destino, nombre_modelo, epocas, batch_size, validation_split, self.panel_derecho, semilla)
        
        
    def toggle_fields(self):
        # ClassName
        if self.check_filtro.get() == 1:  # Si el Checkbutton está seleccionado
            self.entry_semilla.configure(state='normal')  # Activar
        else:
            self.entry_semilla.configure(state='disabled')  # Desactivar
        
            
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()