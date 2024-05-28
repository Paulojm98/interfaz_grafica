# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:43:16 2024

@author: paulo
"""
from queue import Queue
import threading
from utilidades.util_ticket import TicketPurpose, Ticket
import pandas as pd


class ControladorDataset:
    def __init__(self, modelo, vista):
        self.modelo = modelo.modeloDataset
        self.vista = vista
        self.panel = self.vista.current_frame
        self.panel_derecho = self.panel.panel_derecho
        self.queue_message = Queue()
        self._bind()

    def _bind(self):
        self.panel.checkbutton_filtro.configure(command=self.toggle_fields)
        self.panel.button_crear.configure(command=lambda: threading.Thread(target=self.crear_dataset).start())
        self.vista.root.bind("<<Check_queue>>", self.check_queue)
        
    def crear_dataset(self):
        try:
            origen = self.panel.entrada_origen.get()
            destino = self.panel.entrada_destino.get()
            tipo_caracteristicas = self.panel.tipo_creacion.get()
            self.df = pd.read_csv(origen)
            if self.panel.check_filtro.get() == 1:
                frec_min = float(self.panel.frecuencia_min_entry.get())
                frec_max = float(self.panel.frecuencia_max_entry.get())
                ciclos_min = float(self.panel.ciclos_min_entry.get())
                ciclos_max = float(self.panel.ciclos_max_entry.get())
                self.df = self.df[(self.df["Frecuencia"] >= frec_min) & (self.df["Frecuencia"] <= frec_max)]
                self.df = self.df[(self.df["Ciclos"] >= ciclos_min) & (self.df["Ciclos"] <= ciclos_max)]
                
            numero_archivos = self.df.shape[0]
            
            if tipo_caracteristicas == "Transformada de Wavelet":
                ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                                ticket_value=[f"Se van a procesar {numero_archivos} archivos"])
                self.queue_message.put(ticket)
                self.panel.event_generate("<<Check_queue>>")
                self.modelo.dataset_tf_wavelet(self.df, destino, self.panel, self.queue_message)
            
            if tipo_caracteristicas == "Transformada de Fourier":
                ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                                ticket_value=["Tipo de transformada de datos en desarrollo"])
                self.queue_message.put(ticket)
                self.panel.event_generate("<<Check_queue>>")
                
        except ValueError:
            ticket = Ticket(ticket_type=TicketPurpose.ERROR,
                            ticket_value=["Ha ocurrido un error con los campos del filtro."])
            self.queue_message.put(ticket)
            self.panel.event_generate("<<Check_queue>>")
            
        except FileNotFoundError:
            ticket = Ticket(ticket_type=TicketPurpose.ERROR,
                            ticket_value=["Ha ocurrido un error con los campos origen o destino"])
            self.queue_message.put(ticket)
            self.panel.event_generate("<<Check_queue>>")
        
        
        
    def check_queue(self, event):
        msg = self.queue_message.get()
        
        if msg.ticket_type == TicketPurpose.INICIO_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
        if msg.ticket_type == TicketPurpose.ERROR:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
        if msg.ticket_type == TicketPurpose.PROGRESO_TAREA:
            self.panel.label_panel_dch2.configure(text=msg.ticket_value[0])
            self.panel.label_panel_dch3.configure(text=msg.ticket_value[1])
            
        if msg.ticket_type == TicketPurpose.FIN_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            self.panel.label_panel_dch2.configure(text=msg.ticket_value[1])
            self.panel.label_panel_dch3.configure(text="")
            

            
            
    
    def toggle_fields(self):
        # ClassName
        if self.panel.check_filtro.get() == 1:  # Si el Checkbutton está seleccionado
            self.panel.frecuencia_min_entry.configure(state='normal')  # Activar
            self.panel.frecuencia_max_entry.configure(state='normal')  # Activar
            self.panel.ciclos_min_entry.configure(state='normal')  # Activar
            self.panel.ciclos_max_entry.configure(state='normal')  # Activar
        else:
            self.panel.frecuencia_min_entry.configure(state='disabled')  # Desactivar
            self.panel.frecuencia_max_entry.configure(state='disabled')
            self.panel.ciclos_min_entry.configure(state='disabled')
            self.panel.ciclos_max_entry.configure(state='disabled')
            
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

