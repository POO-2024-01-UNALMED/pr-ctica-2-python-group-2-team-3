import tkinter as tk
from tkinter import messagebox
from clases.fieldFrame import FieldFrame
from modulos.excepciones import *

def opcionesAdministrador(ventana_usuario, opcion=0, opcionEscogidaAdmin=None):
    # Muestra la ventana para opciones de administrador
    ventana_usuario.destruirInterfazProcesos()
    ventana_usuario.interaccion_label.config(text="Ver opciones de administrador")
    ventana_usuario.interaccion_texto.config(text="Actualmente se encuentra en la ventana de opciones de administrador. Aqui podras registrar,\ncancelar,modificar y supervisar, los guias turisticos y las actividades recreativas de la empresa.\n\nIngrese la opcion que desea realizar para continuar con el proceso:")

    lista_opcionesAdministrador = ["Ingresar guia", "Retirar guia", "Ver disponibilidad guias", "Ingresar actividad", "Retirar actividad"]
    
    opcionesAdministrador_frame = FieldFrame(ventana_usuario.procesosYConsultas_frame, tipo_formulario=0, on_accept=lambda seleccion: opcionesAdministrador(ventana_usuario,1,seleccion), tituloValores="¿Qué desea hacer?", valores=lista_opcionesAdministrador)
    opcionesAdministrador_frame.pack(padx=10, pady=5)

    if opcion == 1:
        if opcionEscogidaAdmin == "Ingresar guia":
            ingresarGuia(ventana_usuario, 0)
        elif opcionEscogidaAdmin == "Retirar guia":
            retirarGuia(ventana_usuario)
        elif opcionEscogidaAdmin == "Ver disponibilidad guias":
            verDisponibilidadGuias(ventana_usuario)
        elif opcionEscogidaAdmin == "Ingresar actividad":
            ingresarActividad(ventana_usuario)
        elif opcionEscogidaAdmin == "Retirar actividad":
            retirarActividad(ventana_usuario)

def ingresarGuia(ventana_usuario, opcion=0, seleccion=None):
   pass
        
def retirarGuia(ventana_usuario,seleccion=None,opcion=0):
    pass
        
def verDisponibilidadGuias(ventana_usuario):
    pass

def ingresarActividad(ventana_usuario):
    pass

def retirarActividad(ventana_usuario):
    pass