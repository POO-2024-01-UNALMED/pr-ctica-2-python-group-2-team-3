import tkinter as tk

from modulos.excepciones import *
from modulos.reservarActividades import *
from gestorAplicacion.tipoActividad import TipoActividad
from gestorAplicacion.idioma import Idioma
from gestorAplicacion.destino import Destino
from gestorAplicacion.hotel import Hotel
from gestorAplicacion.reserva import Reserva

ListaIdiomas=Idioma.listaNombres()
ListaTipoActividad=TipoActividad.listaNombres()
ListaDestinos=Destino.listaNombres()

reserva=None
def funreservarHospedaje(ventana_usuario):
        """
        Destruye la interfaz de procesos actual y modifica el título de la ventana para iniciar el proceso de planear un viaje.

        :param ventana_usuario: Objeto que representa la ventana del usuario.
        :type ventana_usuario: VentanaUsuario
        """
        ventana_usuario.destruirInterfazProcesos()
        ventana_usuario.modificarTitulo("Reservar hospedaje")
        reservarHospedaje(ventana_usuario)
    
def reservarHospedaje(ventana_usuario, opcion=0, seleccion=None):
        textoBase=["Actualmente se encuentra en la ventana de reservar hospedaje. Aqui podras,",
            "\nreservar tu hotel, elegir un buffet y hacer reservas en restaurantes si asi lo deseas.\n\n"]
    
        ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)

        if opcion == 0:  # Paso 0:Ingresar opcion de reserva
                opcionesReservarActividades=[
                        "Realizar una nueva reserva",
			"Buscar reserva existente para agregar las actividades"]
        
                ventana_usuario.modificarTexto("".join(textoBase)+"Empecemos eligiendo su tipo de reserva. Si ya tienes una reserva creada anteriormente y quieres añadirle un hospedaje\npuedes buscar tu reserva anterior con el codigo que te dieron, pero si no tienes ninguna reserva creada no te preocupes aca podras crear tu reserva desde cero 😊:")
                ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: reservarHospedaje(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?", valores=opcionesReservarActividades)
        if opcion == 1: # Paso 1: Realizar reserva
                if seleccion =="Buscar reserva existente para agregar las actividades":
                        excepcionesReservarActividades1 = [
                        ("Codigo", lambda seleccion: verificarCodigoNone(seleccion))]
                        
                        ventana_usuario.modificarTexto("".join(textoBase)+"Empecemos ingresando el codigo de tu reserva, recuerda que es el codigo que te dieron al realizar tu reserva:")
                        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: reservarHospedaje(ventana_usuario, 2, seleccion),criterios=["Codigo"], verificaciones=excepcionesReservarActividades1)
                else:
                        reserva = realizarReserva(ventana_usuario=ventana_usuario, textobase=textoBase[0])
                        reservarHospedaje(ventana_usuario, 2)
        if opcion==2:
                if seleccion:
                        reserva=Reserva.encontrarCodigo(seleccion)
        
                ventana_usuario.borrarFrame(ventana_usuario.resultados_frame)
                ventana_usuario.tituloResultados()
                criterios = [tupla[0] for tupla in reserva.resumenViaje()]
                valores = [tupla[1] for tupla in reserva.resumenViaje()]
                ventana_usuario.frameResultados(criterios,valores)
                
                reservarHotel(ventana_usuario=ventana_usuario,textoBase=textoBase)

def reservarHotel(ventana_usuario,opcion=0,seleccion=None,textoBase=None):
        print("Entro al metodo")
        ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
        ventana_usuario.texto_base = textoBase if textoBase is not None else "Actualmente se encuentra reservando un hotel.\n"
        
        hoteles_disponibles=Hotel.hotelesDisponibles("reserva")
        if opcion==0:
                ventana_usuario.modificarTexto("".join(textoBase)+"Ahora empezaremos a reservar tu hotel, en estos momentos se estan mostrando los hoteles con capacidad en el destino escogido, elige el que más \n"
                                               "te guste para mirar las posibles acomodaciones para tu reserva. 🤗¡No te preocupes puedes devolverte a elegir otro hotel cuando quieras!🤗")
                ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: reservarHotel(ventana_usuario, 1, seleccion), tituloValores="Elije el hotel", valores=hoteles_disponibles)
        if opcion==1:
                destino=ventana_usuario.reserva.getDestino() if ventana_usuario.reserva is not None else "Cartagena"
                clientes=len(ventana_usuario.reserva.get_clientes()) if ventana_usuario.reserva is not None else 8
                ventana_usuario.hotel=Hotel.buscarHotel(seleccion,destino)
                ventana_usuario.añadirResultado(criterios=["Hotel"],valores=[seleccion])
                
                acomodacion=ventana_usuario.hotel.mostrarAcomodacion(clientes)
                criterios = ["Opcion " + str(i) for i in range(len(acomodacion) + 1)]
                habilitado=[False for i in range(len(criterios) + 1)]
                criterios.append(ventana_usuario.hotel.getNombre())
                habilitado.append(True)
                acomodacion.append(("Seguir"))
                excepcionesHotel1=[
                        (ventana_usuario.hotel.getNombre(), lambda seleccion: verificarFormato(valor=seleccion,criterio=ventana_usuario.hotel.getNombre(),formato=0,palabras=["Seguir","Cambiar"]))]
                
                ventana_usuario.modificarTexto("".join(textoBase)+"Ahora te esta apareciendo las posibles acomodaciones de habitaciones para las personas de tu reserva, si te quires devolver \n"
                                               "a escoger otro hotel debes ingresar en la casilla al lado del nombre del hotel ¨Cambiar¨ de lo contrario puedes dejar el valor por defecto ¨Seguir¨y darle al boton de aceptar:")
                ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: reservarHotel(ventana_usuario, 2, seleccion), criterios=criterios, valores=acomodacion,habilitado=habilitado,verificaciones=excepcionesHotel1)
        
        if opcion==2:
                if seleccion == "Cambiar":
                        reservarHotel(ventana_usuario, 0, seleccion)
                else:
                        criterios=["Individual (capacidad 1)", "Doble (capacidad 2)", "Familiar (capacidad 4)", "Suite (capacidad 6)" ]
                        valores=  list(ventana_usuario.hotel.get_habitaciones().values())
                        excepcionesHotel2=[
                                ("Individual (capacidad 1)",lambda seleccion: verificarNumero(seleccion,True)),
                                ("Doble (capacidad 2)",lambda seleccion: verificarNumero(seleccion,True)),
                                ("Familiar (capacidad 4)",lambda seleccion: verificarNumero(seleccion,True)),
                                ("Suite (capacidad 6)",lambda seleccion: verificarNumero(seleccion,True)),
                        ("*", lambda seleccion: verificarHabitaciones(valor=seleccion,criterio=ventana_usuario.hotel.getNombre(),formato=0,palabras=["Seguir","Cambiar"]))]
                
                        ventana_usuario.modificarTexto("".join(textoBase)+"Procede a ingresar el numero de habitaciones que quieres reservar por cada tipo, el numero de habitaciones disponibles del hotel se encuentra al frente del criterio.\nTen en cuenta que cada tipo de habitacion\n"
                                               "tiene una capacidad y la suma de las capacidades de las habitaciones no puede ser menor a las personas en tu reserva y debe haber un mayor de edad por habitacion:")
                        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: reservarHotel(ventana_usuario, 3, seleccion), criterios=criterios, valores=valores,verificaciones=excepcionesHotel2)
        
        if opcion == 3:
                ventana_usuario.hotel.elegirHabitaciones(seleccion) 
                
                
    
