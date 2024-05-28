# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 00:14:19 2024

@author: paulo
"""

import pandas as pd
import customtkinter as ctk
from tkinter import ttk
import os

class Util_creacion_bdatos:
    
    labels_name = {
        'Pristine': 0,
        'X1Y1': 1,
        'X1Y2': 2,
        'X1Y3': 3,
        'X1Y4': 4,
        'X1Y5': 5,
        'X2Y1': 6,
        'X2Y2': 7,
        'X2Y3': 8,
        'X2Y4': 9,
        'X2Y5': 10,
        'X3Y1': 11,
        'X3Y2': 12,
        'X3Y3': 13,
        'X3Y4': 14,
        'X3Y5': 15,
        'X4Y1': 16,
        'X4Y2': 17,
        'X4Y3': 18,
        'X4Y4': 19,
        'X4Y5': 20,
        'X5Y1': 21,
        'X5Y2': 22,
        'X5Y3': 23,
        'X5Y4': 24,
        'X5Y5': 25,
        
    }


    
    def __init__(self, origen, destino, nombre_csv, panel_derecho, tipo):
        self.origen = origen
        self.destino = destino
        self.nombre_csv = nombre_csv
        self.panel = panel_derecho
        self.tipo = tipo
        self.control_panel()
        self.crear_bdatos()
    
    
    def control_panel(self):
        self.label_inicio = ctk.CTkLabel(self.panel, text="Se ha iniciado el proceso de creación", font=("Roboto", 14))
        self.label_inicio.pack(side=ctk.TOP)
        self.panel.update()
    
    def crear_bdatos(self):
        data_dir_list = os.listdir(self.origen)
        if self.tipo is True:
            df = pd.DataFrame(columns=['FileName', 'Label', 'ClassName'])
        else:
            df = pd.DataFrame(columns=['FileName', 'ClassName'])
        

        for dataset in data_dir_list:
            mat_list = os.listdir(os.path.join(self.origen,dataset))
            if self.tipo is True:
                label = self.labels_name.get(dataset, None)
                     
            num_files = len(mat_list)
            
            # read each file and if it is corrupted exclude it , if not include it in either train or test data frames
            for i in range(num_files):
                mat_name = mat_list[i]
                partes = mat_name.split("_")
                mat_filename = os.path.join(self.origen,dataset,mat_name)
                amplitud = partes[1]
                frecuencia_m = partes[2]
                ciclos = partes[3]
                if self.tipo is True:
                    df = pd.concat([df,pd.DataFrame({'FileName': [mat_filename], 'Label': [label],'ClassName': [dataset],'Amplitud': [amplitud],'Frecuencia': [frecuencia_m],'Ciclos': [ciclos]})],ignore_index=True)
                else:
                    df = pd.concat([df,pd.DataFrame({'FileName': [mat_filename], 'ClassName': [dataset],'Amplitud': [amplitud],'Frecuencia': [frecuencia_m],'Ciclos': [ciclos]})],ignore_index=True)
                
        
        df.to_csv(os.path.join(self.destino, self.nombre_csv+".csv"))
        self.label_inicio.configure(text="Proceso terminado")
        # Crear el Treeview dentro del frame
        tree = ttk.Treeview(self.panel)
        
        # Definir las columnas
        tree['columns'] = list(df.columns)
        
        # Formatear nuestras columnas
        for col in tree['columns']:
            tree.column(col, anchor="center")
            tree.heading(col, text=col, anchor="center")
        
        # Añadir los datos del DataFrame al Treeview
        for i, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        
        tree.pack(pady=20, padx=20, fill= ctk.BOTH, expand=True)
        
        

