# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 20:14:11 2024

@author: paulo
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import customtkinter as ctk
from keras.utils import np_utils
import pywt
from PIL import Image


class Util_creacion_dataset:
    
    damage_posicion = {
        'X1Y1': (0.03665, 0.03665),
        'X1Y2': (0.03665, 0.0733),
        'X1Y3': (0.03665, 0.10995),
        'X1Y4': (0.03665, 0.1466),
        'X1Y5': (0.03665, 0.18325),
        'X2Y1': (0.0733, 0.03665),
        'X2Y2': (0.0733, 0.0733),
        'X2Y3': (0.0733, 0.10995),
        'X2Y4': (0.0733, 0.1466),
        'X2Y5': (0.0733, 0.18325),
        'X3Y1': (0.10995, 0.03665),
        'X3Y2': (0.10995, 0.0733),
        'X3Y3': (0.10995, 0.10995),
        'X3Y4': (0.10995, 0.1466),
        'X3Y5': (0.10995, 0.18325),
        'X4Y1': (0.1466, 0.03665),
        'X4Y2': (0.1466, 0.0733),
        'X4Y3': (0.1466, 0.10995),
        'X4Y4': (0.1466, 0.1466),
        'X4Y5': (0.1466, 0.18325),
        'X5Y1': (0.18325, 0.03665),
        'X5Y2': (0.18325, 0.0733),
        'X5Y3': (0.18325, 0.10995),
        'X5Y4': (0.18325, 0.1466),
        'X5Y5': (0.18325, 0.18325)
        }
    
    sensores_posiciones = {
        0: (0.0, 0.0),
        1: (0.0733, 0.0),
        2: (0.1466, 0.0),
        3: (0.2199, 0.0),
        4: (0.2199, 0.0733),
        5: (0.2199, 0.1466),
        6: (0.2199, 0.2199),
        7: (0.1466, 0.2199),
        8: (0.0733, 0.2199),
        9: (0.0, 0.2199),
        10: (0.0, 0.1466),
        11: (0.0, 0.0733)}



    
    def __init__(self, df, destino, panel_derecho):
        self.df = df
        self.destino = destino
        self.panel = panel_derecho
        self.Fs = 12.5e6
        self.dt = 1.0 / self.Fs  # sec
        self.f_min = 100000  # Frecuencia mínima del rango de interés
        self.f_max = 600000  # Frecuencia máxima del rango de interés
        self.num_intervals = 50  # Número de intervalos (escalas)
        self.frequencies = np.linspace(self.f_max, self.f_min, self.num_intervals) / self.Fs
        self.scales = pywt.frequency2scale('morl', self.frequencies)
        self.control_panel()
        self.num_archivos_creados = 0
        self.crear()

    def normalize_signal(self, signal):
        normalized_signal = 2 * ((signal - np.min(signal)) / (np.max(signal) - np.min(signal))) - 1
        return normalized_signal
    
    
    def control_panel(self):
        numero_archivos = self.df.shape[0]
        self.label_numero_archivos = ctk.CTkLabel(self.panel, text=f"Se van a procesar {numero_archivos} archivos", font=("Roboto", 14))
        self.label_numero_archivos.grid(row=1, column=1, columnspan=3, pady=10, padx=10)
        self.label_archivo_creado = ctk.CTkLabel(self.panel, text="", font=("Roboto", 14))
        self.label_archivo_creado.grid(row=2, column=1, columnspan=3, pady=10, padx=10)
    
    def crear(self):
        for (label, classname, frecuencia, ciclos), group in self.df.groupby(['Label', 'ClassName', 'Frecuencia', 'Ciclos']):
            
            if len(group) == 2 and len(group['Amplitud'].unique()) == 2:  # Asegurar 2 filas con distinta 'Amplitud'
                # Cargar los archivos .mat para cada fila en el grupo
                self.num_archivos_creados = self.num_archivos_creados + 1
                resultados_procesados = []
                label = np_utils.to_categorical(label, 26)
                mats = [sio.loadmat(row['FileName']) for _, row in group.iterrows()]
                signals1 = mats[0]['data']
                signals2 = mats[1]['data']
                for transmitter in range(12):
                    for receiver in range(12):
                        if transmitter != receiver:
                            signal_norn1 = self.normalize_signal(signals1[:, transmitter, receiver])
                            signal_norn2 = self.normalize_signal(signals2[:, transmitter, receiver])
                            signal_resultante = signal_norn1 - signal_norn2
                            signal_resultante = signal_resultante[:2000]
                            
                            # Calcular el coeficiente de la transformada wavelet continua (CWT)
                            coeff, freq = pywt.cwt(signal_resultante, self.scales, 'morl', self.dt)
                            
                            # Convertir el coeficiente en una imagen
                            original_image = Image.fromarray(coeff.astype('uint8'))
                            
                            # Redimensionar la imagen a (50, 50)
                            resized_image = original_image.resize((50, 50))
                            
                            # Convertir la imagen de vuelta a un array
                            resized_array = np.array(resized_image)
                            
                            # Guardar el array redimensionado en la lista de resultados
                            resultados_procesados.append(resized_array)
    
                resultados_procesados = np.array(resultados_procesados)
                resultados_procesados = np.transpose(resultados_procesados, (1, 2, 0))
                # Guardar como archivos .npz
                np.savez(self.destino+str(classname)+'_'+str(frecuencia)+'_'+str(ciclos)+'.npz', resultados_procesados=resultados_procesados, label=label)
                archivo_creado = str(classname)+'_'+str(frecuencia)+'_'+str(ciclos)+'.npz'
                self.label_archivo_creado.configure(text=f"Archivo: {archivo_creado} creado")
                self.panel.update()
                
        ctk.CTkLabel(self.panel, text="Proceso terminado.", font=("Roboto", 20)).grid(row=3, column=1, columnspan=3, pady=10, padx=10)
        ctk.CTkLabel(self.panel, text=f"Se han creado {self.num_archivos_creados} archivos en la dirección {self.destino}.", font=("Roboto", 14)).grid(row=4, column=1, columnspan=3, pady=10, padx=10)
        

