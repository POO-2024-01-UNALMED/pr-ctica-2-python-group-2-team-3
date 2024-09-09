import tkinter as tk
from tkinter import messagebox
from clases.fieldFrame import FieldFrame
from modulos.excepciones import *

def modificarReserva(ventana_usuario, opcion=0, opcionEscogidaAdmin=None):
        # Muestra la ventana para modificar reserva
        ventana_usuario.destruirInterfazProcesos()
        ventana_usuario.interaccion_label.config(text="Modificar reserva")
        ventana_usuario.interaccion_texto.config(text="Actualmente se encuentra en la ventana de modificar reserva.\nAqui podras modificar o cancelar una reserva que hayas creado previamente.\n\nPrimero ingrese el codigo que le dieron al realizar su reserva:")
        ingresarCodigo_frame = FieldFrame(ventana_usuario.procesosYConsultas_frame, tipo_formulario=3,on_accept=lambda seleccion:modificarReserva(ventana_usuario,seleccion), tituloCriterios="Criterios", criterios=["Codigo de la reserva"], tituloValores="Valores")
        ingresarCodigo_frame.pack(padx=10, pady=5)
