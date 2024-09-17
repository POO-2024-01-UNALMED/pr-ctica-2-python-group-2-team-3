import tkinter as tk
from tkinter import messagebox
from clases.fieldFrame import FieldFrame
from modulos.excepciones import *

from gestorAplicacion.tipoActividad import TipoActividad
from gestorAplicacion.idioma import Idioma
from gestorAplicacion.destino import Destino
from gestorAplicacion.reserva import Reserva
from gestorAplicacion.plan import Plan
from gestorAplicacion.hotel import Hotel


ListaIdiomas=Idioma.listaNombres()
ListaTipoActividad=TipoActividad.listaNombres()
ListaDestinos=Destino.listaNombres()
reserva=Reserva.encontrarCodigo(None)

def funModificarReserva(ventana_usuario):
        ventana_usuario.destruirInterfazProcesos()
        ventana_usuario.modificarTitulo("Modificar reserva")
        modificarReserva(ventana_usuario)
        
def modificarReserva(ventana_usuario, opcion=0, seleccion=None):
        textoBase=["Actualmente se encuentra en la ventana de modificar reserva. Aquí podrás modificar tu reserva anteriormente creada.\n"
        "Primero ingresa el codigo de la reserva.\n\n"]
        ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
        
        if opcion == 0:
                if seleccion:
                        reserva=Reserva.encontrarCodigo(seleccion)
                        modificarReserva(ventana_usuario, 1)
                else:
                        
                        excepcionesReservarActividades1 = [
                        ("Codigo", lambda seleccion: verificarCodigoNone(seleccion))]
                        
                        ventana_usuario.modificarTexto("".join(textoBase)+"Empecemos ingresando el codigo de tu reserva, recuerda que es el codigo que te dieron al realizar tu reserva:")
                        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: modificarReserva(ventana_usuario, 0, seleccion),criterios=["Codigo"], verificaciones=excepcionesReservarActividades1)
        if opcion == 1:
                if seleccion:
                        print(seleccion)
                        if "Modificar destino" in seleccion:
                                modificarReserva(ventana_usuario, 2)
                                
                        if "Modificar fechas" in seleccion:
                                modificarReserva(ventana_usuario, 3)
                        
                        if "Modificar idioma" in seleccion:
                                modificarReserva(ventana_usuario, 4)
                        if "Modificar cantidad de clientes" in  seleccion:
                                modificarReserva(ventana_usuario, 5)  
                        modificarReserva(ventana_usuario, 6) 
                        modificarReserva(ventana_usuario, 7)
                        modificarReserva(ventana_usuario, 8)    
                else:
                        opciones=["Modificar idioma","Modificar destino","Modificar fechas","Modificar cantidad de clientes"]
                        ventana_usuario.modificarTexto("".join(textoBase)+"Ingrese las opciones que desea modificar")
                        ventana_usuario.crearFormulario(tipo_formulario=1, on_accept=lambda seleccion: modificarReserva(ventana_usuario, 1, seleccion), tituloValores="Elige las opciones a modificar:", valores=opciones)
              
        if opcion == 2: 
                if seleccion:
                        reserva.set_destinoNombre(seleccion)  
                        ventana_usuario.tituloResultados()
                        ventana_usuario.frameResultados(criterios=["Destino:"], valores=[seleccion])
                else:
                        ventana_usuario.modificarTexto("".join(textoBase)+"Genial empezaremos ingresando el destino, selecciona la opcion del destino que prefieras:")
                        ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: modificarReserva(ventana_usuario, 2, seleccion), tituloValores="Elige el destino:", valores=ListaDestinos)
        
        if opcion == 3:
                if seleccion:
                        print(seleccion)
                        cantidad=int(seleccion["Cantidad de días"])
                        fecha=seleccion["Fecha de inicio"]
                        fechas=Reserva.mostrarDias(cantidad,fecha)
                        reserva.set_fechas(fechas)
                        ventana_usuario.añadirResultado("Fechas",fechas[0]+" - "+fechas[-1])
                else:
                        excepcionesPlanearFecha = [
                                ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
                                ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))]
                        
                        ventana_usuario.modificarTexto("".join(textoBase) + "Ahora ingrese el periodo de fechas en el que desea planear su viaje:")
                        ventana_usuario.crearFormulario( tipo_formulario=3,  on_accept=lambda seleccion: modificarReserva(ventana_usuario, 3, seleccion), criterios=["Cantidad de días", "Fecha de inicio"], verificaciones=excepcionesPlanearFecha)
        
     
        if opcion == 4:
                if seleccion:
                        reserva.set_idiomas(seleccion)
                        ventana_usuario.añadirResultado("Idioma",seleccion)
                else:
                        ventana_usuario.modificarTexto("".join(textoBase) + "Ingrese el idioma que desea que utilice el guia turistico en las diferentes actividades de su plan:")
                        ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: modificarReserva(ventana_usuario, 4, seleccion), tituloValores="Elige el idioma:", valores=ListaIdiomas)
        if opcion == 5:
                if seleccion:
                        reserva.set_cantidadClientes(int(seleccion["Cantidad de personas"]))
                        reserva.definirPrecio()
                        modificarReserva(ventana_usuario, 8)
                else:
                        excepcionesPlanearPresupuesto = [
                                ("Cantidad de personas", lambda seleccion: verificarNumero(seleccion))]
                        
                        ventana_usuario.modificarTexto("".join(textoBase) + "Ahora ingrese la nueva cantidad de personas que van a estar en tu reserva")
                        ventana_usuario.crearFormulario( tipo_formulario=3,  on_accept=lambda seleccion: modificarReserva(ventana_usuario, 5, seleccion), criterios=["Cantidad de personas"], verificaciones=excepcionesPlanearPresupuesto)
       
        if opcion == 6:
                if seleccion:
                        reserva.set_paquete_turistico(seleccion)
                        ventana_usuario.añadirResultado("Paquete turistico",seleccion)
                        modificarReserva(ventana_usuario, 8)
                else:
                        ventana_usuario.modificarTexto("".join(textoBase) + "Ahora elije el paquete turistico que mas te gusto:")
                        ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: modificarReserva(ventana_usuario, 6, seleccion), tituloValores="Elige el paquete turistico::", valores=Plan.generar_paquetes_turisticos())
        if opcion == 7:
                if seleccion:
                        reserva.set_hotel(seleccion)
                        ventana_usuario.añadirResultado("Hotel",seleccion)
                else:
                        ventana_usuario.modificarTexto("".join(textoBase) + "Elige el hotel que mas te llamo la atencion:")
                        ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: modificarReserva(ventana_usuario, 7, seleccion), tituloValores="Elige el paquete turistico::", valores=Hotel.mostrarHoteles())
        
        if opcion == 8:
                ventana_usuario.borrarResultados("___________ Resumen de la reserva modificada___________")
                ventana_usuario.modificarTexto( textoBase[0] + "🥳¡Felicidades! Haz moodificado tu reserva con exito🥳\nAquí podrás ver el resumen de tu nueva reserva, Esperamos haber sido de utilidad 😊")
                ventana_usuario.frameResumen(lista=reserva.resumenViaje(), metodoSalida=lambda: modificarReserva(ventana_usuario))
