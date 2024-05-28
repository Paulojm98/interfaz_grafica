# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:39:17 2024

@author: paulo
"""
import random
import tensorflow as tf
import os
import numpy as np
from matplotlib.figure import Figure
from utilidades.util_ticket import TicketPurpose, Ticket
from utilidades.util_custom_callback import CustomCallback

class ModeloEntrenamiento:
    def __init__(self):
        # Inicialización de parámetros del modelo
        pass
        

    def entrenar(self, origen, destino, nombre_modelo, epochs, batch_size, validation_split, panel, queue_message, random_seed=None):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado el entrenamiento del modelo."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        # Obtener la lista de archivos .npz
        archivos_npz = [os.path.join(origen, archivo) for archivo in os.listdir(origen) if archivo.endswith('.npz')]
        # Mezclar el orden de los archivos con la semilla
        if random_seed is not None:    
            random.seed(random_seed)
        random.shuffle(archivos_npz)
        
        print(archivos_npz)
        # Calcular el índice para dividir entre entrenamiento y validación
        split_index = int(len(archivos_npz) * (1 - validation_split))
        # Dividir entre entrenamiento y validación
        archivos_entrenamiento = archivos_npz[:split_index]
        archivos_validacion = archivos_npz[split_index:]
        num_train_samples = len(archivos_entrenamiento)
        num_test_samples = len(archivos_validacion)
        # Crear conjuntos de datos para entrenamiento y validación
        train_generator = self.generador(archivos_entrenamiento, batch_size)
        validation_generator = self.generador(archivos_validacion, batch_size)
        
        self.crear_modelo()
        
        callbacks = [CustomCallback(panel, queue_message)]
        
        self.history=self.model.fit(
            train_generator,
            steps_per_epoch=num_train_samples // batch_size,
            epochs= epochs,
            validation_data=validation_generator,
            validation_steps=num_test_samples // batch_size,
            callbacks=callbacks)

        # Guardar el modelo entrenado
        ruta_modelo_guardar = os.path.join(destino, nombre_modelo+".h5")
        self.model.save(ruta_modelo_guardar)
        ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                        ticket_value=["Se ha terminado el proceso de entrenamientoArithmeticError",
                                      f"El modelo se ha guardado correctamente en {ruta_modelo_guardar}"])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        
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
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.3),
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
        
        return fig
    
         
        