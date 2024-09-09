import tkinter as tk
from tkinter import messagebox
from clases.fieldFrame import FieldFrame
from modulos.excepciones import *

def reservarHospedaje(ventana_usuario, opcion=0, opcionEscogidaAdmin=None):
        # Muestra la ventana para reservar hospedaje
        ventana_usuario.destruirInterfazProcesos()
        
        ventana_usuario.interaccion_label.config(text="Reservar hospedaje")
        ventana_usuario.interaccion_texto.config(text="Actualmente se encuentra en la ventana de reservar hospedaje. Aqui podras reservar y elegir tu hotel\nsegún tus preferencias y ademas podras reservar los servicios extra con los que cuenta el hotel como buffets y restaurantes.\n\nPrimero ingrese el codigo que le dieron al realizar su reserva:")
        ingresarCodigo_frame = FieldFrame(ventana_usuario.procesosYConsultas_frame, tipo_formulario=3,on_accept=lambda seleccion:reservarHospedaje(ventana_usuario,seleccion), tituloCriterios="Criterios", criterios=["Codigo de la reserva"], tituloValores="Valores")
        ingresarCodigo_frame.pack(padx=10, pady=5)