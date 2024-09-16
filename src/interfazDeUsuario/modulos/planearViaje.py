from clases.fieldFrame import FieldFrame
from modulos.excepciones import *

def planearViaje(ventana_usuario, opcion=0, opcionEscogidaAdmin=None):
        # Muestra la ventana para planear viaje
        ventana_usuario.destruirInterfazProcesos()
        ventana_usuario.interaccion_label.config(text="Planear tu viaje")
        ventana_usuario.interaccion_texto.config(text="Actualmente se encuentra en la ventana de planear tu viaje. Aqui podras planear tu proximo viaje\nsegún las mejores opciones que tenemos para ofrecerte según tus preferencias.\n\nPrimero ingrese la cantidad de personas para las cuales quiere planear el viaje:")
        ingresarNombre_frame = FieldFrame(ventana_usuario.procesosYConsultas_frame, tipo_formulario=3,on_accept=lambda seleccion:planearViaje(ventana_usuario,seleccion), tituloCriterios="Criterios", criterios=["Cantidad de personas"], tituloValores="Valores")
        ingresarNombre_frame.pack(padx=10, pady=5)