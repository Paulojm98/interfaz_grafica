# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:34:01 2024

@author: paulo
"""
import pandas as pd
from utilidades.util_ticket import TicketPurpose, Ticket
import os


class ModeloBDatos:
    
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
    
    def __init__(self):
        pass
    

    def crear_bdatos(self, origen, destino, nombre_csv, panel, tipo, queue_message):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado la creación de la base de datos."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        
        try:
            data_dir_list = os.listdir(origen)
            self.df = pd.DataFrame(columns=['FileName', 'Label', 'ClassName'])
            

            for dataset in data_dir_list:
                mat_list = os.listdir(os.path.join(origen,dataset))
                if tipo is True:
                    label = self.labels_name.get(dataset, None)
                         
                num_files = len(mat_list)
                
                # read each file and if it is corrupted exclude it , if not include it in either train or test data frames
                for i in range(num_files):
                    mat_name = mat_list[i]
                    partes = mat_name.split("_")
                    mat_filename = os.path.join(origen,dataset,mat_name)
                    amplitud = partes[1]
                    frecuencia_m = partes[2]
                    ciclos = partes[3]
                    if tipo is True:
                        self.df = pd.concat([self.df,pd.DataFrame({'FileName': [mat_filename], 'Label': [label],'ClassName': [dataset],'Amplitud': [amplitud],'Frecuencia': [frecuencia_m],'Ciclos': [ciclos]})],ignore_index=True)
                    else:
                        self.df = pd.concat([self.df,pd.DataFrame({'FileName': [mat_filename], 'ClassName': [dataset],'Amplitud': [amplitud],'Frecuencia': [frecuencia_m],'Ciclos': [ciclos]})],ignore_index=True)
                    
            
            self.df.to_csv(os.path.join(destino, nombre_csv+".csv"))
            ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                            ticket_value=["Se ha finalizado la creación de la base de datos."])
            queue_message.put(ticket)
            panel.event_generate("<<Check_queue>>")
            
        except:
            ticket = Ticket(ticket_type=TicketPurpose.ERROR,
                            ticket_value=["Ha ocurrido un error al crear la base de datos."])
            queue_message.put(ticket)
            panel.event_generate("<<Check_queue>>")
            
        