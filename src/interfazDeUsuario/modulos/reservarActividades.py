import tkinter as tk
from excepciones import *
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
    
    textoBase = [
        "Actualmente se encuentra en la ventana de reservar actividades turísticas.",
        "Aquí podrás registrar tu reserva,\ncomprar una suscripción y elegir un plan personalizado de actividades o un paquete turístico ya planeado.\n\n"]
    
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)

    if opcion == 0:  # Paso 0: Ingresar opción de reserva
        opcionesReservarActividades = [
            "Realizar una nueva reserva",
            "Buscar reserva existente para agregar las actividades"]
        
        ventana_usuario.modificarTexto( "".join(textoBase) +"Empecemos eligiendo su tipo de reserva, si ya tienes una reserva creada anteriormente y quieres añadirle un plan de actividades puedes buscar tu reserva anterior con el código que te dieron, pero si no tienes ninguna reserva creada no te preocupes, acá podrás crear tu reserva desde cero 😊:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: reservarActividades(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?",valores=opcionesReservarActividades)

    if opcion == 1:# Paso 1: Buscar o crear la reserva
        if seleccion == "Buscar reserva existente para agregar las actividades":
            excepcionesReservarActividades1 = [
                ("Código", lambda seleccion: verificarCodigo(seleccion))]
            
            ventana_usuario.modificarTexto( "".join(textoBase) + "Empecemos ingresando el código de tu reserva, recuerda que es el código que te dieron al realizar tu reserva:")
            ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: reservarActividades(ventana_usuario, 2, seleccion),  criterios=["Código"], verificaciones=excepcionesReservarActividades1)
        else:
            ventana_usuario.reserva = realizarReserva(ventana_usuario=ventana_usuario, textobase=textoBase[0])
            reservarActividades(ventana_usuario, 2, seleccion)

    if opcion == 2: # Paso 2: Elegir plan de actividades y terminar procesos
        if seleccion:
            ventana_usuario.reserva = Reserva.buscar_reserva(seleccion["Código"])
        
        elegirPlanTuristico(ventana_usuario)
        ventana_usuario.borrarResultados("___________ Resumen de la reserva realizada___________")
        ventana_usuario.modificarTexto( textoBase[0] + "\n🎉🎉Terminaste de realizar tu reserva🎉🎉\n\nAquí podrás ver el resumen de lo que elegiste. Esperamos haber sido de utilidad 😊"  )
        ventana_usuario.frameResumen(lista=ventana_usuario.reserva.toString(), metodoSalida=lambda: reservarActividades(ventana_usuario))


def realizarReserva(ventana_usuario, opcion=0, seleccion=None, textobase=None):
    """
    Crea una nueva reserva de actividades turísticas.

    :param ventana_usuario: Objeto que representa la interfaz de usuario.
    :param opcion (int, optional): Indica el paso del proceso de creación de la reserva. Default es 0.
    :param seleccion (dict, optional): Datos seleccionados por el usuario en cada paso.
    :param textobase (str, optional): Mensaje base para mostrar en la interfaz.
    """
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    ventana_usuario.texto_base = textobase if textobase is not None else "Actualmente se encuentra creando una nueva reserva.\n"
    
    if opcion == 0: # Paso 0: Ingreso de detalles iniciales de la reserva
        excepcionesReservarActividades0 = [
            ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
            ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))]
        
        ventana_usuario.modificarTexto("".join(ventana_usuario.texto_base) +  "Empezaremos a crear su reserva desde 0, primero ingrese el periodo de tiempo en el que planea reservar:")
        ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 1, seleccion), criterios=["Cantidad de días", "Fecha de inicio"],  verificaciones=excepcionesReservarActividades0)

    if opcion == 1: #Paso 1: Ingreso de información del titular de la reserva.
        ventana_usuario.fecha = seleccion
        ventana_usuario.tituloResultados()
        ventana_usuario.frameResultados(criterios=["Cantidad de días", "Fecha de inicio"], valores=[seleccion["Cantidad de días"], seleccion["Fecha de inicio"]] )
        
        excepcionesReservarActividades1 = [ 
                        ("Nombre", lambda seleccion: verificarNombre(seleccion)), ("Edad", lambda seleccion: verificarTitular(seleccion))]
        
        ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Ahora ingrese la información de la persona que va a ser el titular de la reserva:")
        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 2, seleccion), criterios=["Nombre", "Edad"], verificaciones=excepcionesReservarActividades1)

    if opcion == 2: #Paso 2: Verificación de suscripción y creación del titular.
        ventana_usuario.titular = SuscripcionverificarSuscripcion(seleccion)
        ventana_usuario.añadirResultado( criterios=["Nombre del titular:", "Edad del titular:"], valores=[seleccion["Nombre"], seleccion["Edad"]])
        
        if ventana_usuario.titular is None:
            ventana_usuario.titular = newCliente(seleccion)
            ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Actualmente no cuenta con una suscripción con nosotros, elija cómo quiere proceder con su reserva:" )
            
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 3, seleccion), tituloValores="¿Desea comprar una suscripción para recibir descuentos impresionantes para su reserva?",  valores=["Sí, quiero comprar", "No, gracias"])
        else:
            realizarReserva(ventana_usuario, 3)

    if opcion == 3: #Paso 3: Elección de suscripción o confirmación sin suscripción.
        if seleccion == "Sí, quiero comprar":
            ventana_usuario.suscripcion = comprarSuscripcion(ventana_usuario)
        else:
            ventana_usuario.suscripcion = "No se aplicará una suscripción a la reserva"
        
        ventana_usuario.frameResultados(criterios=["Suscripción:"], valores=[ventana_usuario.suscripcion])
        
        excepcionesReservarActividades2 = [
            ("Cantidad de clientes", lambda seleccion: verificarNumero(seleccion))]
        
        ventana_usuario.reserva = newReserva()
        ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Ingrese la cantidad de clientes que van a reservar, sin contar al titular:")
        ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 4, seleccion), criterios=["Cantidad de clientes"], verificaciones=excepcionesReservarActividades2 )

    if opcion == 4: #Paso 4: Ingreso de cantidad de clientes.
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
            ventana_usuario.reserva = asignarClasificacion(ventana_usuario.reserva)
            ventana_usuario.reserva = aplicarSuscripcion(ventana_usuario.reserva)
        else:
            excepcionesReservarActividades3 = [
                ("Nombre", lambda seleccion: verificarNombre(seleccion)),
                ("Edad", lambda seleccion: verificarTitular(seleccion))]
            
            ventana_usuario.modificarTexto("".join(ventana_usuario.texto_base) +  "Ahora ingrese la información del cliente " + str(ventana_usuario.contador) + ":")
            ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 5, seleccion), criterios=["Nombre", "Edad"], verificaciones=excepcionesReservarActividades3)

    return ventana_usuario.reserva


def comprarSuscripcion(ventana_usuario, opcion=0, seleccion=None):
    """
    Gestiona el proceso de compra de suscripciones.

    :param ventana_usuario: Objeto que representa la interfaz de usuario.
    :param opcion (int, optional): Paso del proceso de compra de suscripción. Default es 0.
    :param seleccion (str, optional): Elección del tipo de suscripción.
    :return: Objeto nuevaSuscripcion.
    """
    suscripcionesDisponibles = SuscripcionmostrarPosiblesSuscripciones()
    
    if opcion == 0: # Preguntar si se quiere comprar una suscripción
        ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Actualmente no cuenta con una suscripción con nosotros, elija cómo quiere proceder con su reserva:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: comprarSuscripcion(ventana_usuario, 1, seleccion),  tituloValores="¿Desea comprar una suscripción para recibir descuentos impresionantes para su reserva?", valores=["Sí, quiero comprar", "No, gracias"])
    
    if opcion == 1: #Escoger la suscripción o salir de la compra
            if seleccion == "No, gracias":
                    return None
            else:
                ventana_usuario.modificarTexto( "".join(ventana_usuario.texto_base) +  "Genial, puedes escoger entre estas opciones de suscripciones:")
                ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: comprarSuscripcion(ventana_usuario, 1, seleccion),  tituloValores="¿Desea comprar una suscripción para recibir descuentos impresionantes para su reserva?", valores=suscripcionesDisponibles)
        
    if opcion == 2: # Crear objeto suscripcion
        if seleccion == "Básica":
            nuevaSuscripcion = newSuscripcion(ventana_usuario.titular)
        elif seleccion == "General":
            nuevaSuscripcion = newSuscripcion(ventana_usuario.titular)
        elif seleccion == "Premium":
            nuevaSuscripcion = newSuscripcion(ventana_usuario.titular)
        elif seleccion == "VIP":
            nuevaSuscripcion = newSuscripcion(ventana_usuario.titular)
    
    return nuevaSuscripcion


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

