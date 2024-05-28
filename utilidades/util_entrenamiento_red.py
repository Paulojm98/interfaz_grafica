# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 00:18:23 2024

@author: paulo
"""
import random
import tensorflow as tf
import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .util_custom_callback import CustomCallback
import customtkinter as ctk

class Util_entrenamiento_red:

    def __init__(self, origen, destino, nombre_modelo, epochs, batch_size, validation_split, panel_derecho, random_seed=None):
        self.panel = panel_derecho
        self.carpeta = origen
        self.destino = destino
        self.nombre_modelo = nombre_modelo
        self.validation_split = validation_split
        self.batch_size = batch_size
        self.epochs = epochs
        self.random_seed = random_seed
        self.control_panel()
        self.crear_modelo()
        self.entrenar()
    
    def control_panel(self):
        self.label_inicio = ctk.CTkLabel(self.panel, text="Se ha comenzado el entrenamiento", font=("Roboto", 14))
        self.label_inicio.grid(row=1, column=1, columnspan=3, pady=10, padx=10)
        self.label_info_entrenamiento = ctk.CTkLabel(self.panel, text="Información del entrenamiento aquí")
        self.label_info_entrenamiento.grid(row=2, column=1, columnspan=3, pady=10, padx=10)
        

    def entrenar(self):
        # Obtener la lista de archivos .npz
        archivos_npz = [os.path.join(self.carpeta, archivo) for archivo in os.listdir(self.carpeta) if archivo.endswith('.npz')]
        # Mezclar el orden de los archivos con la semilla
        if self.random_seed is not None:    
            random.seed(self.random_seed)
        random.shuffle(archivos_npz)
        # Calcular el índice para dividir entre entrenamiento y validación
        split_index = int(len(archivos_npz) * (1 - self.validation_split))
        # Dividir entre entrenamiento y validación
        archivos_entrenamiento = archivos_npz[:split_index]
        archivos_validacion = archivos_npz[split_index:]
        num_train_samples = len(archivos_entrenamiento)
        num_test_samples = len(archivos_validacion)
        # Crear conjuntos de datos para entrenamiento y validación
        train_generator = self.generador(archivos_entrenamiento, self.batch_size)
        validation_generator = self.generador(archivos_validacion, self.batch_size)
        
        callbacks = [CustomCallback(panel)]
        
        self.history=self.model.fit(
            train_generator,
            steps_per_epoch=num_train_samples // self.batch_size,
            epochs= self.epochs,
            validation_data=validation_generator,
            validation_steps=num_test_samples // self.batch_size,
            callbacks=callbacks)

        # Guardar el modelo entrenado
        ruta_modelo_guardar = os.path.join(self.destino, self.nombre_modelo+".h5")
        self.model.save(ruta_modelo_guardar)
        self.pintar_graficas()
        
    def cargar_y_procesar_archivo(self, archivo):
        data = np.load(archivo)
        # Convertir los datos a float32
        resultados_procesados = data['resultados_procesados'].astype(np.float32)
        etiquetas = data['label'].astype(np.float32)
        etiquetas
        return resultados_procesados, etiquetas

    def generador(self, data, batch_size):
        num_samples = len(data)
        while True:   
            for offset in range(0, num_samples, batch_size):
                # Get the samples you'll use in this batch
                batch_samples = data[offset:offset+batch_size]
                imagenes_batch = []
                etiquetas_batch = []
                # For each example
                for batch_sample in batch_samples:
                    archivo = batch_sample
                    imagen, etiqueta_one_hot = self.cargar_y_procesar_archivo(archivo)
                    imagenes_batch.append(imagen)
                    etiquetas_batch.append(etiqueta_one_hot)
                yield (np.array(imagenes_batch), np.array(etiquetas_batch))
    
    def crear_modelo(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(50, 50, 132)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(26, activation='softmax')
        ])

        # Compilar el modelo
        self.model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        # Resumen del modelo
        self.model.summary()
        
    def pintar_graficas(self):
        fig = Figure(figsize=(12, 6), dpi=100)
        plot1 = fig.add_subplot(121)
        plot2 = fig.add_subplot(122)
        
        plot1.plot(self.history.history['accuracy'], label='Precisión de Entrenamiento')
        plot1.plot(self.history.history['val_accuracy'], label='Precisión de Validación')
        plot1.set_title('Precisión a lo largo de las épocas')
        plot1.set_xlabel('Épocas')
        plot1.set_ylabel('Precisión')
        plot1.legend()
        
        plot2.plot(self.history.history['loss'], label='Pérdida de Entrenamiento')
        plot2.plot(self.history.history['val_loss'], label='Pérdida de Validación')
        plot2.set_title('Pérdida a lo largo de las épocas')
        plot2.set_xlabel('Épocas')
        plot2.set_ylabel('Pérdida')
        plot2.legend()
        
        # Mostrar el gráfico en el panel
        canvas = FigureCanvasTkAgg(fig, master=self.panel)  # `self.panel` es el panel de CustomTkinter donde quieres mostrar el gráfico
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=1, columnspan=3, pady=10, padx=10)
        

