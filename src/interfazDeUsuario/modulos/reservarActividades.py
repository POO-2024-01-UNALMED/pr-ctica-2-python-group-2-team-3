import tkinter as tk
from tkinter import messagebox
from excepciones import *

from gestorAplicacion.actividad import Actividad
from gestorAplicacion.tipoActividad import TipoActividad
from gestorAplicacion.idioma import Idioma
from gestorAplicacion.destino import Destino
from gestorAplicacion.guia import Guia
from gestorAplicacion.reserva import Reserva
from gestorAplicacion.cliente import Cliente
from gestorAplicacion.suscripcion import Suscripcion
from gestorAplicacion.grupo import Grupo


def reservarActividades(ventana_usuario, opcion=0, seleccion=None):
    """
    Gestiona el proceso de reserva de actividades turísticas.
    
    :param ventana_usuario: Objeto que representa la interfaz de usuario.
    :param opcion (int, optional): Indica el paso del proceso de reserva. Default es 0.
    :param seleccion (dict, optional): Datos seleccionados por el usuario en cada paso.
    """
    reserva = None
    textoBase = [
        "Actualmente se encuentra en la ventana de reservar actividades turísticas.",
        "Aquí podrás registrar tu reserva,\ncomprar una suscripción y elegir un plan personalizado de actividades o un paquete turístico ya planeado.\n\n"]
    
    ventana_usuario.destruirInterfazProcesos()  # Elimina los elementos de la interfaz de procesos      

    if opcion == 0:  # Paso 0: Ingresar opción de reserva
        opcionesReservarActividades = [
            "Realizar una nueva reserva",
            "Buscar reserva existente para agregar las actividades"]
        
        ventana_usuario.modificarTexto( "".join(textoBase) +"Empecemos eligiendo su tipo de reserva, si ya tienes una reserva creada anteriormente y quieres añadirle un plan de actividades\npuedes buscar tu reserva anterior con el código que te dieron, pero si no tienes ninguna reserva creada no te preocupes, acá podrás crear tu reserva desde cero 😊:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: reservarActividades(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?",valores=opcionesReservarActividades)

    if opcion == 1: # Paso 1: Buscar o crear la reserva
        if seleccion == "Buscar reserva existente para agregar las actividades":
            excepcionesReservarActividades1 = [
                ("Código", lambda seleccion: verificarCodigo(seleccion))]
            
            ventana_usuario.modificarTexto( "".join(textoBase) + "Empecemos ingresando el código de tu reserva, recuerda que es el código que te dieron al realizar tu reserva:")
            ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: reservarActividades(ventana_usuario, 2, seleccion),  criterios=["Código"], verificaciones=excepcionesReservarActividades1)
        
        elif seleccion == "Realizar una nueva reserva":
            reserva = realizarReserva(ventana_usuario=ventana_usuario, opcion=0, seleccion=None, textobase=textoBase[0])
            reservarActividades(ventana_usuario, 2, seleccion)
            return reserva
            

    if opcion == 2: # Paso 2: Elegir plan de actividades y terminar procesos
        if seleccion and "Código" in seleccion:
            reserva = Reserva.buscar_reserva(int(seleccion["Código"]))
        else:
            reserva = reserva_global
        
        elegirPlanTuristico(ventana_usuario)
        ventana_usuario.borrarResultados("___________ Resumen de la reserva realizada___________")
        ventana_usuario.modificarTexto( textoBase[0] + "\n🎉🎉Terminaste de realizar tu reserva🎉🎉\n\nAquí podrás ver el resumen de lo que elegiste. Esperamos haber sido de utilidad 😊"  )
        ventana_usuario.frameResumen(lista=reserva_global.toString(), metodoSalida=lambda: reservarActividades(ventana_usuario))

def realizarReserva(ventana_usuario, opcion=0, seleccion=None, textobase=None):
    """
    Crea una nueva reserva de actividades turísticas.

    :param ventana_usuario: Objeto que representa la interfaz de usuario.
    :param opcion (int, optional): Indica el paso del proceso de creación de la reserva. Default es 0.
    :param seleccion (dict, optional): Datos seleccionados por el usuario en cada paso.
    :param textobase (str, optional): Mensaje base para mostrar en la interfaz.
    :return: Objeto reserva creado.
    """
    titular= None
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    ventana_usuario.texto_base = textobase if textobase is not None else "Actualmente se encuentra creando una nueva reserva.\n"
    
    if opcion == 0: # Paso 0: Ingreso de detalles iniciales de la reserva
        excepcionesReservarActividades0 = [
            ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
            ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))]
        
        ventana_usuario.modificarTexto("".join(ventana_usuario.texto_base) +  "Empezaremos a crear su reserva desde 0, primero ingrese el periodo de tiempo en el que planea reservar:")
        ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 1, seleccion), criterios=["Cantidad de días", "Fecha de inicio"],  verificaciones=excepcionesReservarActividades0)

    if opcion == 1: #Paso 1: Ingreso de información del titular de la reserva.
        fecha = seleccion
        ventana_usuario.fechas = Reserva.mostrarDias(seleccion["Cantidad de días"], seleccion["Fecha de inicio"])
        ventana_usuario.tituloResultados()
        ventana_usuario.frameResultados(criterios=["Cantidad de días", "Fecha de inicio"], valores=[seleccion["Cantidad de días"], seleccion["Fecha de inicio"]] )
        
        excepcionesReservarActividades1 = [ 
            ("Nombre", lambda seleccion: verificarNombre(seleccion)), 
            ("Edad", lambda seleccion: verificarTitular(seleccion))]
        
        ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Ahora ingrese la información de la persona que va a ser el titular de la reserva:")
        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 2, seleccion), criterios=["Nombre", "Edad"], verificaciones=excepcionesReservarActividades1)
        #return fechas #Posible fallo, estar pendiende de esto
        
    if opcion == 2: #Paso 2: Verificación de suscripción y creación del titular.
        titular = Suscripcion.verificar_suscripcion(nombre=seleccion["Nombre"], edad=seleccion["Edad"], lista_fechas=ventana_usuario.fechas)
        #ventana_usuario.titular = titular #Se guarda el titular en la ventana para poder acceder a él en otros métodos
        
        ventana_usuario.añadirResultado(criterio="Nombre del titular", valor=seleccion["Nombre"])
        ventana_usuario.añadirResultado(criterio="Edad del titular", valor=seleccion["Edad"])
        
        if titular is None:
            titular = Cliente(nombre=seleccion["Nombre"], edad=seleccion["Edad"])
            ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Actualmente no cuenta con una suscripción con nosotros, elija cómo quiere proceder con su reserva:" )
            
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 3, seleccion), tituloValores="¿Desea comprar una suscripción para recibir descuentos impresionantes para su reserva?",  valores=["Sí, quiero comprar", "No, gracias"])
            return titular
        else:
            realizarReserva(ventana_usuario, 3)
            return titular

    if opcion == 3: #Paso 3: Elección de suscripción o confirmación sin suscripción.
        
        if seleccion: #Caso en el que el cliente no tiene una suscripción, ya sea que la compre o no
            suscripcion  = comprarSuscripcion(ventana_usuario, seleccion=seleccion, titular= titular)
            titular.setSuscripcion(suscripcion)
    
        ventana_usuario.borrarResultados("")
        ventana_usuario.tituloResultados()
        ventana_usuario.frameResultados(criterios=["Suscripción"], valores=[titular.getSuscripcion().get_tipo() if titular.getSuscripcion() is not None else "No hay suscripción"])
        realizarReserva(ventana_usuario, 3)
        
        
    if opcion == 4: #Paso 4: Ingreso de cantidad de clientes.
        excepcionesReservarActividades2 = [
            ("Cantidad de clientes", lambda seleccion: verificarNumero(seleccion))]
        reserva = Reserva()
        ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Ingrese la cantidad de clientes que van a reservar, sin contar al titular:")
        ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 4, seleccion), criterios=["Cantidad de clientes"], verificaciones=excepcionesReservarActividades2 )
        ventana_usuario.cantidadClientes = int(seleccion)
        realizarReserva(ventana_usuario, 5)

    if opcion == 5: #Paso 5: Registro de clientes adicionales.
        if seleccion is None:
            ventana_usuario.contador = 0
            ventana_usuario.clientes = []
        else:
            ventana_usuario.contador += 1
            cliente = ingresarCliente(seleccion)
            ventana_usuario.reserva.append(cliente)
            ventana_usuario.clientes.append(cliente)
        
        seleccionx = "None" if ventana_usuario.contador == ventana_usuario.cantidadClientes else None
        realizarReserva(ventana_usuario, 6, seleccionx)

    if opcion == 6: #Paso 6: Finalización del proceso de reserva, asignación de clasificación y suscripción.
        if seleccion == "None":
            ventana_usuario.frameResultados(criterios=["Clientes:"], valores=ventana_usuario.clientes)
            reserva = asignarClasificacion(ventana_usuario.reserva)
            reserva = aplicarSuscripcion(ventana_usuario.reserva)
        else:
            excepcionesReservarActividades3 = [
                ("Nombre", lambda seleccion: verificarNombre(seleccion)),
                ("Edad", lambda seleccion: verificarTitular(seleccion))]
            
            ventana_usuario.modificarTexto("".join(ventana_usuario.texto_base) +  "Ahora ingrese la información del cliente " + str(ventana_usuario.contador) + ":")
            ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 5, seleccion), criterios=["Nombre", "Edad"], verificaciones=excepcionesReservarActividades3)

    return reserva


def comprarSuscripcion(ventana_usuario, opcion=0, seleccion=None, titular=None):
    """
    Gestiona el proceso de compra de suscripciones.

    :param ventana_usuario: Objeto que representa la interfaz de usuario.
    :param opcion (int, optional): Paso del proceso de compra de suscripción. Default es 0.
    :param seleccion (str, optional): Elección del tipo de suscripción.
    :return: Objeto nuevaSuscripcion.
    """
    
    suscripcionesDisponibles = Suscripcion.get_lista_tipos()
    nuevaSuscripcion1 = None  # Initialize the variable

    if opcion == 0:  # Escoger la suscripción o salir de la compra
        if seleccion == "No, gracias":
            return None
        else:
            ventana_usuario.modificarTexto("".join(ventana_usuario.texto_base) + "Genial, puedes escoger entre estas opciones de suscripciones:")
            ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: comprarSuscripcion(ventana_usuario, 1, seleccion), tituloValores="¿Qué tipo de suscripción desea comprar?", valores=suscripcionesDisponibles)

    elif opcion == 1:  # Crear objeto suscripcion
        if seleccion == "Básica":
            nuevaSuscripcion1 = Suscripcion(tipo=seleccion, titular=titular, fechas=ventana_usuario.fechas)
            print("Se ha creado una suscripcion basica")
        elif seleccion == "General":
            nuevaSuscripcion1 = Suscripcion(tipo=seleccion, titular=titular, fechas=ventana_usuario.fechas)
            print("Se ha creado una suscripcion general")
        elif seleccion == "Premium":
            nuevaSuscripcion1 = Suscripcion(tipo=seleccion, titular=titular, fechas=ventana_usuario.fechas)
            print("Se ha creado una suscripcion premium")
        elif seleccion == "VIP":
            nuevaSuscripcion1 = Suscripcion(tipo=seleccion, titular=titular, fechas=ventana_usuario.fechas)
            print("Se ha creado una suscripcion VIP")
        else:
            print("No se ha seleccionado una suscripción válida")
            return None

    return nuevaSuscripcion1
        
def reservaExistente(ventana_usuario, textoBase):
    
    excepcionesReservarActividades1 = [
                ("Código", lambda seleccion: verificarCodigo(seleccion))]
            
    ventana_usuario.modificarTexto( "".join(textoBase) + "Empecemos ingresando el código de tu reserva, recuerda que es el código que te dieron al realizar tu reserva:")
    ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: reservarActividades(ventana_usuario, 2, seleccion),  criterios=["Código"], verificaciones=excepcionesReservarActividades1)
    
def crearYAsignarReserva(ventana_usuario, textoBase):
    global reserva_global
    reserva_global = realizarReserva(ventana_usuario=ventana_usuario, opcion=0, seleccion=None, textobase=textoBase[0])
    reservarActividades(ventana_usuario, 2, None)

def elegirPlanTuristico(ventana_usuario, opcion=0, seleccion=None):
    """
    Permite al usuario elegir un plan turístico.
    
    :param ventana_usuario: Objeto que representa la interfaz de usuario.
    :param opcion (int, optional): Paso del proceso de selección del plan. Default es 0.
    :param seleccion (str, optional): Selección del usuario.
    """
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    planesPosibles = [
        "Plan personalizado (Se escogen las actividades desde 0 de manera manual)",
        "Paquete turístico (Se escoge un plan turístico predefinido, con actividades generales ya establecidas)"
    ]
    
    if opcion == 0:
        ventana_usuario.modificarTexto(
            "".join(ventana_usuario.texto_base) + 
            "Ahora te guiaremos para que elijas tu plan o paquete turístico, primero elige la opción que deseas realizar:"
        )
        ventana_usuario.crearFormulario(
            tipo_formulario=0,
            on_accept=lambda seleccion: comprarSuscripcion(ventana_usuario, 1, seleccion),
            tituloValores="¿Qué desea hacer?",
            valores=planesPosibles
        )
    
    if opcion == 1:
        pass

