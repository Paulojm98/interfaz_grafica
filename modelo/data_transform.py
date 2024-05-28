# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:36:11 2024

@author: paulo
"""
import numpy as np
import scipy.io as sio
from keras.utils import np_utils
import pywt
from PIL import Image
from utilidades.util_ticket import TicketPurpose, Ticket
import os

class ModeloDataset:
    
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
    
    
    def __init__(self):
        pass
    
    def normalize_signal(self, signal):
        normalized_signal = 2 * ((signal - np.min(signal)) / (np.max(signal) - np.min(signal))) - 1
        return normalized_signal

    def dataset_tf_wavelet(self, df, destino, panel, queue_message, train=True):
        Fs = 12.5e6
        dt = 1.0 / Fs  # sec
        f_min = 100000  # Frecuencia mínima del rango de interés
        f_max = 600000  # Frecuencia máxima del rango de interés
        num_intervals = 50  # Número de intervalos (escalas)
        frequencies = np.linspace(f_max, f_min, num_intervals) / Fs
        scales = pywt.frequency2scale('morl', frequencies)
        num_archivos_creados = 0
        num_archivos_totales = len(df)
        for (label, classname, frecuencia, ciclos), group in df.groupby(['Label', 'ClassName', 'Frecuencia', 'Ciclos']):
            
            if len(group) == 2 and len(group['Amplitud'].unique()) == 2:  # Asegurar 2 filas con distinta 'Amplitud'
                # Cargar los archivos .mat para cada fila en el grupo
                num_archivos_creados = num_archivos_creados + 1
                resultados_procesados = []
                label_one_hot = np_utils.to_categorical([label], num_classes=26)
                mats = [sio.loadmat(row['FileName']) for _, row in group.iterrows()]
                signals1 = mats[0]['data']
                signals2 = mats[1]['data']
                for transmitter in range(12):
                    for receiver in range(12):
                        if transmitter != receiver:
                            signal_norn1 = self.normalize_signal(signals1[:, transmitter, receiver])
                            signal_norn2 = self.normalize_signal(signals2[:, transmitter, receiver])
                            signal_resultante = signal_norn2 - signal_norn1
                            signal_resultante = signal_resultante[:2000]
                            
                            # Calcular el coeficiente de la transformada wavelet continua (CWT)
                            coeff, freq = pywt.cwt(signal_resultante, scales, 'morl', dt)
                            
                            # Convertir el coeficiente en una imagen
                            original_image = Image.fromarray(np.abs(coeff))
                            
                            # Redimensionar la imagen a (50, 50)
                            resized_image = original_image.resize((50, 50))
                            
                            # Convertir la imagen de vuelta a un array
                            resized_array = np.array(resized_image)
                            
                            # Guardar el array redimensionado en la lista de resultados
                            resultados_procesados.append(resized_array)
    
                resultados_procesados = np.array(resultados_procesados)
                resultados_procesados = np.transpose(resultados_procesados, (1, 2, 0))
                # Guardar como archivos .npz
                archivo_creado = str(classname)+'_'+str(frecuencia)+'_'+str(ciclos)+'.npz'
                np.savez(os.path.join(destino, archivo_creado), resultados_procesados=resultados_procesados, label=label_one_hot)
                
                ticket = Ticket(ticket_type=TicketPurpose.PROGRESO_TAREA,
                                ticket_value=[f"Archivo: {archivo_creado} creado", f"Progreso: {num_archivos_creados*2}/{num_archivos_totales}"])
                queue_message.put(ticket)
                panel.event_generate("<<Check_queue>>")
                
        ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                        ticket_value=["Proceso terminado", 
                                      f"Se han creado {num_archivos_creados} archivos en la dirección {destino}."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        
    def dataset_tf_fourier(self, df, destino, panel, queue_message):
        # En desarrollo
        pass
                
                
                
        