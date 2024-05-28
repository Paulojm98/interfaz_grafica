# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:40:53 2024

@author: paulo
"""

from queue import Queue
import threading
from utilidades.util_ticket import TicketPurpose, Ticket
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Modificación del ControladorEntrenamiento para incluir el manejo de hilos y colas
class ControladorEntrenamiento:
    def __init__(self, modelo, vista):
        self.modelo = modelo.ModeloEntrenamiento
        self.vista = vista
        self.panel = self.vista.current_frame
        self.panel_derecho = self.panel.panel_derecho
        self.queue_message = Queue()
        self._bind()
        #self.cola_mensajes = queue.Queue()  # Cola para mensajes del hilo de entrenamiento
        
    def _bind(self):
        self.panel.checkbutton_semilla.configure(command=self.toggle_fields)
        self.panel.button_entrenar.configure(command=lambda: threading.Thread(target=self.entrenar_red).start())
        self.vista.root.bind("<<Check_queue>>", self.check_queue)

    def entrenar_red(self):
        try:
            origen = self.panel.entrada_origen.get()
            destino = self.panel.entrada_destino.get()
            nombre_modelo = self.panel.entry_nombre_modelo.get()
            tipo_caracteristicas = self.panel.tipo_creacion.get()
            epocas = int(self.panel.entry_epocas.get())
            batch_size = int(self.panel.entry_batch_size.get())
            validation_split = float(self.panel.entry_validation_split.get())
            semilla = None
            if self.panel.check_filtro.get() == 1:
                semilla = int(self.panel.entry_semilla.get())
                
            self.modelo.entrenar(origen, destino, nombre_modelo, epocas, batch_size, validation_split, self.panel, self.queue_message, semilla)
            
        except ValueError:
            ticket = Ticket(ticket_type=TicketPurpose.ERROR,
                            ticket_value=["Ha ocurrido un error en los valores númericos introducidos"])
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
            self.panel.textbox_logs_train.configure(state="normal")
            self.panel.textbox_logs_train.insert("end", msg.ticket_value[0] + "\n")
            self.panel.textbox_logs_train.configure(state='disabled')
            self.panel.textbox_logs_train.see("end")
            
        if msg.ticket_type == TicketPurpose.FIN_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            self.panel.label_panel_dch2.configure(text=msg.ticket_value[1])
            fig = self.modelo.pintar_graficas()
            canvas = FigureCanvasTkAgg(fig, self.panel_derecho)  # `self.panel` es el panel de CustomTkinter donde quieres mostrar el gráfico
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        
        
    def toggle_fields(self):
        # ClassName
        if self.panel.check_filtro.get() == 1:  # Si el Checkbutton está seleccionado
            self.panel.entry_semilla.configure(state='normal')  # Activar
        else:
            self.panel.entry_semilla.configure(state='disabled')  # Desactivar
            
    
        
            
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
            
            


