# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:41:56 2024

@author: paulo
"""



from queue import Queue
import threading
from utilidades.util_ticket import TicketPurpose

class ControladorBDatos:
    def __init__(self, modelo, vista):
        self.modelo = modelo.modeloBDatos
        self.vista = vista
        self.panel = self.vista.current_frame
        self.panel_derecho = self.panel.panel_derecho
        self.queue_message = Queue()
        self._bind()

    def _bind(self):
        self.panel.button_crear_db_train.configure(command=lambda: threading.Thread(target=self.crear_bd_train).start())
        self.panel.button_crear_db_test.configure(command= lambda: threading.Thread(target=self.crear_bd_test()).start())
        self.vista.root.bind("<<Check_queue>>", self.check_queue)
        

    def crear_bd_train(self):
        origen = self.panel.entry_data_train.get()
        destino = self.panel.entry_destino_train.get()
        nombre_csv = self.panel.entry_nombre_train.get()
        self.modelo.crear_bdatos(origen, destino, nombre_csv, self.panel, True, self.queue_message)
        
    def crear_bd_test(self):
        origen = self.panel.entry_data_test.get()
        destino = self.panel.entry_destino_test.get()
        nombre_csv = self.panel.entry_nombre_test.get()
        self.modelo.crear_bdatos(origen, destino, nombre_csv, self.panel, False, self.queue_message)
        
    def check_queue(self, event):
        msg = self.queue_message.get()
        
        if msg.ticket_type == TicketPurpose.INICIO_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
        if msg.ticket_type == TicketPurpose.ERROR:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
        if msg.ticket_type == TicketPurpose.FIN_TAREA:
            num_archivos = len(self.modelo.df)
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            self.panel.label_panel_dch2.configure(text=f"La base de datos tiene {num_archivos} archivos.")
            self.panel.tree['columns'] = list(self.modelo.df.columns)

            # Configura la columna del árbol para que no muestre encabezado y ajusta su ancho si no se va a usar
            self.panel.tree.column("#0", width=0, stretch=False)
            self.panel.tree.heading("#0", text="")
            
            # Formatear nuestras columnas
            for col in self.panel.tree['columns']:
                self.panel.tree.column(col, anchor="center")
                self.panel.tree.heading(col, text=col, anchor="center")
            
            # Añadir los datos del DataFrame al Treeview
            for i, row in self.modelo.df.iterrows():
                self.panel.tree.insert("", "end", values=list(row))
            
            self.panel.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            self.panel.scrollbar.grid(row=2, column=1, sticky='ns')
            
    
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()