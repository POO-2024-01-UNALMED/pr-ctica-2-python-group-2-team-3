import tkinter as tk
from tkinter import messagebox
from clases.fieldFrame import FieldFrame
from modulos.excepciones import *

def reservarActividades(ventana_usuario, opcion=0, opcionEscogidaAdmin=None):
        # Muestra la ventana para reservar actividades
        ventana_usuario.destruirInterfazProcesos()
        ventana_usuario.interaccion_label.config(text="Reservar actividades turísticas")
        ventana_usuario.interaccion_texto.config(text="Actualmente se encuentra en la ventana de reservar actividades.\nAqui podras reservar y elegir tu plan de actividades turisticas.\n\nPrimero ingresa los datos del titular de la reserva:")
        ingresarNombre_frame = FieldFrame(ventana_usuario.procesosYConsultas_frame, tipo_formulario=3,on_accept=lambda seleccion:reservarActividades(ventana_usuario,seleccion),  tituloCriterios="Criterios", criterios=["Nombre","Edad"], tituloValores="Valores")
        ingresarNombre_frame.pack(padx=10, pady=5)