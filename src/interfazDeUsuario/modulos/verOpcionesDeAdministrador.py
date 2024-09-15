import tkinter as tk
from modulos.excepciones import *

from gestorAplicacion.actividad import Actividad
from gestorAplicacion.tipoActividad import TipoActividad
from gestorAplicacion.idioma import Idioma
from gestorAplicacion.destino import Destino
from gestorAplicacion.guia import Guia
from gestorAplicacion.reserva import Reserva

ListaIdiomas=Idioma.listaNombres()
ListaTipoActividad=TipoActividad.listaNombres()
ListaDestinos=Destino.listaNombres()
    
def opcionesAdministrador(ventana_usuario, opcion=0, opcionEscogidaAdmin=None):
    """
    Muestra la ventana para las opciones del administrador y redirige según la opción seleccionada.
    
    :param ventana_usuario(Tk): Instancia de la ventana principal de usuario.
    :param opcion(int): Indica el paso en el proceso de selección de opciones del administrador.
    :param opcionEscogidaAdmin(str): Opción seleccionada por el usuario (e.g. "Ingresar guía", "Retirar guía").
    """
    Lista_opcionesAdministrador = ["Ingresar guia", "Retirar guia", "Ver disponibilidad guias", "Ingresar actividad", "Cancelar actividad"]

    # Preparar la interfaz para mostrar las opciones de administrador
    ventana_usuario.destruirInterfazProcesos()
    ventana_usuario.modificarTitulo("Ver opciones de administrador")
    ventana_usuario.modificarTexto(
        "Actualmente se encuentra en la ventana de opciones de administrador. Aquí podrá registrar,\n"
        "cancelar, modificar y supervisar los guías turísticos y las actividades recreativas de la empresa.\n\n"
        "Ingrese la opción que desea realizar para continuar con el proceso:" )
    
    ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: opcionesAdministrador(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?", valores=Lista_opcionesAdministrador)

    if opcion == 1:
        # Llamar a la función correspondiente según la opción seleccionada
        opciones = {
            "Ingresar guia": ingresarGuia,
            "Retirar guia": retirarGuia,
            "Ver disponibilidad guias": verDisponibilidadGuias,
            "Ingresar actividad": ingresarActividad,
            "Cancelar actividad": cancelarActividad
        }
        if opcionEscogidaAdmin in opciones:
            opciones[opcionEscogidaAdmin](ventana_usuario)


def ingresarGuia(ventana_usuario, opcion=0, seleccion=None):
    """
    Maneja el proceso paso a paso para ingresar un nuevo guía, incluyendo la entrada de datos y verificación.
    
    :param ventana_usuario(Tk): Instancia de la ventana principal de usuario.
    :param opcion(int): Fase del proceso para ingresar un guía (0 = entrada de datos básicos, 1 = idiomas, etc.).
    :param seleccion(dict): Datos seleccionados por el usuario (nombre, edad, idiomas, etc.).
    """
    textoBase=["Actualmente se encuentra en la ventana de ingresar guía.",
            " A continuación\n le vamos a guiar en el proceso para registrar un nuevo guía turístico.\n\n"]
    
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)

    if opcion == 0:  # Paso 0:Ingresar nombre y edad
        excepcionesIngresarGuia = [
            ("Nombre", lambda seleccion: verificarNombre(seleccion)),
            ("Edad", lambda seleccion: verificarNumero(seleccion)) ]
        
        ventana_usuario.modificarTexto("".join(textoBase)+"Empecemos ingresando el nombre y la edad del nuevo guía:")
        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: ingresarGuia(ventana_usuario, 1, seleccion),criterios=["Nombre", "Edad"], verificaciones=excepcionesIngresarGuia)

    elif opcion == 1:  # Paso 1: Ingresar idiomas
        ventana_usuario.guia=Guia(nombre=seleccion["Nombre"], edad=seleccion["Edad"])
        
        ventana_usuario.tituloResultados()
        ventana_usuario.frameResultados(criterios=["Nombre", "Edad"], valores=[seleccion["Nombre"], seleccion["Edad"]])
        
        ventana_usuario.modificarTexto("".join(textoBase)+"Proceda a seleccionar las habilidades y capacidades del guía:")
        ventana_usuario.crearFormulario(tipo_formulario=1, on_accept=lambda seleccion: ingresarGuia(ventana_usuario, 2, seleccion),tituloValores="Seleccione los Idiomas que domina", valores=ListaIdiomas)

    elif opcion == 2:  # Paso 2:Ingresar actividades
        ventana_usuario.guia.ingresarIdiomas(seleccion)
        
        ventana_usuario.añadirResultado("Idiomas", ", ".join(seleccion))
        ventana_usuario.crearFormulario(tipo_formulario=1, on_accept=lambda seleccion: ingresarGuia(ventana_usuario, 3, seleccion), tituloValores="Seleccione las actividades para las cuales está capacitado",  valores=ListaTipoActividad)

    elif opcion == 3:  # Paso 3: Seleccionar destino
        ventana_usuario.guia.ingresarTipoActividades(seleccion)
        destinosP = Destino.elegirDestinoGuia(ventana_usuario.guia)
        
        ventana_usuario.añadirResultado("Tipos de actividad", ", ".join(seleccion))
        if len(destinosP)>0:
            ventana_usuario.modificarTexto("".join(textoBase)+"Seleccione el destino donde trabajará el guía según sus preferencias:" )
            ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: ingresarGuia(ventana_usuario, 4, seleccion),tituloValores="Seleccione el destino", valores=destinosP)
        else:
            ingresarGuia(ventana_usuario, 4)

    elif opcion == 4:  # Paso 4: Finalizar proceso
        if seleccion:
            destino=Destino.buscarNombre(seleccion) if Destino.buscarNombre(seleccion) is not None else seleccion
            Destino.ingresarGuia(ventana_usuario.guia, destino)

        ventana_usuario.guia.ingresarGuia()
        ventana_usuario.guia.asignarParametros()
        
        ventana_usuario.borrarResultados("___________ Resumen de la información personal del guía___________")
        ventana_usuario.modificarTexto(textoBase[0]+ "\n🎉🎉Terminaste de ingresar el guía🎉🎉\n\nAquí podrás ver el resumen de tu ingreso. Esperamos haber sido de utilidad 😊")
        ventana_usuario.frameResumen( lista=ventana_usuario.guia.toString(), metodoSalida=lambda: opcionesAdministrador(ventana_usuario))

def retirarGuia(ventana_usuario, opcion=0, seleccion=None):
    """
    Maneja el proceso de retirar un guía turístico, ya sea despidiéndolo definitivamente o dándolo de baja por un periodo de tiempo.
    
    :param ventana_usuario: La ventana actual de usuario donde se realizan las operaciones.
    :param opcion: Paso actual del proceso (0: seleccionar tipo de retiro, 1: ingresar guía, 2: retirar guía, 3: finalizar proceso).
    :param seleccion: Datos seleccionados o ingresados por el usuario en el formulario.
    """
    textoBase = [
        "Actualmente se encuentra en la ventana de retirar guía.",
        " A continuación\n le vamos a guiar en el proceso para", "despedir o dar de baja", 
        " a un guía turístico.\n\n"]
    
    texto_Despido = [textoBase[0] + textoBase[1] + "despedir definitivamente", textoBase[3]]
    texto_DarDeBja = [textoBase[0] + textoBase[1] + "dar de baja por un periodo de tiempo", textoBase[3]]
    
    opcionesRetirarGuia = [
        "Despedir definitivamente a un guía",
        "Dar de baja a un guía por un periodo de tiempo"]
    
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    
    if opcion == 0:  # Paso 0: Elegir la opción de tipo de retiro
        ventana_usuario.modificarTexto("".join(textoBase) + "Primero elija la opción que desea realizar:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: retirarGuia(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?",  valores=opcionesRetirarGuia)

    elif opcion == 1:  # Paso 1: Ingresar el guía
        ventana_usuario.tipo_retiro = seleccion
        textoBase = texto_Despido if ventana_usuario.tipo_retiro == "Despedir definitivamente a un guía" else texto_DarDeBja
        excepcionesRetirarGuia0 = [
            ("Nombre", lambda seleccion: verificarNombre(seleccion)),
            ("Edad", lambda seleccion: verificarNumero(seleccion)),
            ("Destino",lambda seleccion: verificarDestino(seleccion)),
            ("*", lambda seleccion: verificarGuia(seleccion))]
        
        ventana_usuario.modificarTexto("".join(textoBase) + "Ahora ingrese la información del guía que desea retirar (Asegúrese de ingresar un guía actualmente activo):")
        ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: retirarGuia(ventana_usuario, 2, seleccion), criterios=["Nombre", "Edad", "Destino"], verificaciones=excepcionesRetirarGuia0)

    elif opcion == 2:  # Paso 2: Retirar guía
        ventana_usuario.guia = Guia.buscarGuia(seleccion)
        if ventana_usuario.tipo_retiro == "Dar de baja a un guía por un periodo de tiempo":
            excepcionesRetirarGuia1 = [
                ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
                ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))]
            
            ventana_usuario.modificarTexto("".join(textoBase) + "Por último ingrese el periodo de tiempo en el que se va a retirar al guía:")
            ventana_usuario.crearFormulario( tipo_formulario=3,  on_accept=lambda seleccion: retirarGuia(ventana_usuario, 3, seleccion), criterios=["Cantidad de días", "Fecha de inicio"], verificaciones=excepcionesRetirarGuia1)
        else:
            retirarGuia(ventana_usuario, 3)
    
    elif opcion == 3:  # Paso 3: Finalizar proceso
        if ventana_usuario.tipo_retiro == "Despedir definitivamente a un guía":
            resumen=ventana_usuario.guia.retirarGuiaDespido()
            ventana_usuario.texto = "despedido el guía"
        elif ventana_usuario.tipo_retiro == "Dar de baja a un guía por un periodo de tiempo":
            periodo_tiempo = Reserva.mostrarDias(int(seleccion["Cantidad de días"]),seleccion["Fecha de inicio"])
            resumen=ventana_usuario.guia.retirarGuiaDespido(periodo_tiempo)
            ventana_usuario.texto = "retirado por un tiempo al guía"
        
        ventana_usuario.borrarResultados("___________ Resumen del proceso realizado___________")
        ventana_usuario.modificarTexto( textoBase[0] + "\n🥳¡Felicidades! Se ha " + ventana_usuario.texto + " con éxito🥳\n\nAquí podrás ver el resumen del retiro. Esperamos haber sido de utilidad 😊")
        ventana_usuario.frameResumen(lista=resumen, metodoSalida=lambda: opcionesAdministrador(ventana_usuario))
 
def verDisponibilidadGuias(ventana_usuario,opcion=0,seleccion=None):
    textoBase=["Actualmente se encuentra en la ventana de ver la disponibilidad de los guias.\n",
            " Aqui podras ver y filtrar la informacion de todos los guias registrados en la empresa.\n\n"]
    
    opcionesInicioVerDisponibilidadGuias = [
        "Ver la disponibilidad de todos los guías según la fecha",
		"Ver la disponibilidad de todos los guías según el destino",
		"Ver la disponibilidad de todos los guías según el idioma",
		"Ver el itinerario de un guía en específico"]
    
    opcionesCambioVerDisponibilidadGuias=[
        "Cambiar el tipo de tabla","Cambiar el filtro de fecha de la tabla","Volver al inicio"]
    
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    
    if opcion == 0:  # Paso 0: Elegir la opción de la tabla
        ventana_usuario.modificarTexto("".join(textoBase) + "Elija la opción de tabla que desea buscar:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: verDisponibilidadGuias(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?",  valores=opcionesInicioVerDisponibilidadGuias)
        
    if opcion == 1: # Paso 1: Elegir tabla
        ventana_usuario.opcion=seleccion
        ventana_usuario.modificarTexto("".join(textoBase) + "Elija el filtro de fecha con el cual quiere filtrar la información:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: verDisponibilidadGuias(ventana_usuario, 2, seleccion), tituloValores="¿Como desea buscar?",  valores=["Buscar según el mes","Buscar según el mes y el dia"])

    if opcion == 2: # Paso 2: Ingresar fecha
        ventana_usuario.opcionFecha=seleccion
        formato=1 if ventana_usuario.opcionFecha=="Buscar según el mes y el dia" else 2
        excepcionesVerDisponibilidadGuia1 = [
                ("Fecha", lambda seleccion: verificarFormato(seleccion, "Fecha", formato))]
            
        ventana_usuario.modificarTexto("".join(textoBase) + "Ingrese la fecha por la que va buscar:")
        ventana_usuario.crearFormulario( tipo_formulario=3,  on_accept=lambda seleccion:  verDisponibilidadGuias(ventana_usuario, 3, seleccion), criterios=["Fecha"], verificaciones=excepcionesVerDisponibilidadGuia1)
        
    if opcion == 3: # Paso 3: Ingresar guia, destino o idioma(si es necesario)
        ventana_usuario.fecha=seleccion
        if ventana_usuario.opcion=="Ver el itinerario de un guía en específico":
            excepcionesVerDisponibilidadGuia0 = [
            ("Nombre", lambda seleccion: verificarNombre(seleccion)),
            ("Edad", lambda seleccion: verificarNumero(seleccion)),
            ("Destino",lambda seleccion: verificarDestino(seleccion)),
            ("*", lambda seleccion: verificarGuia(seleccion))]
        
            ventana_usuario.modificarTexto("".join(textoBase) + "Proceda a ingresar la información del guía que desea buscar:")
            ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: verDisponibilidadGuias(ventana_usuario, 4, seleccion), criterios=["Nombre", "Edad", "Destino"], verificaciones=excepcionesVerDisponibilidadGuia0)

        elif ventana_usuario.opcion=="Ver la disponibilidad de todos los guías según el destino":
            ventana_usuario.modificarTexto("".join(textoBase)+"Proceda a elegir el destino que desea buscar:")
            ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: verDisponibilidadGuias(ventana_usuario, 4, seleccion),tituloValores="Seleccione el destino", valores=ListaDestinos)

        elif ventana_usuario.opcion=="Ver la disponibilidad de todos los guías según el idioma":
            ventana_usuario.modificarTexto("".join(textoBase)+"Proceda a elegir el idioma que desea buscar:")
            ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: verDisponibilidadGuias(ventana_usuario, 4, seleccion),tituloValores="Seleccione el idioma", valores=ListaIdiomas)
            
        else:
           verDisponibilidadGuias(ventana_usuario, 4, seleccion)
    
    if opcion == 4: # Paso 4: mostrar tabla
        if seleccion:
            if ventana_usuario.opcion=="Ver el itinerario de un guía en específico":
                ventana_usuario.guia=GuiabuscarGuia(seleccion)
            elif ventana_usuario.opcion=="Ver la disponibilidad de todos los guías según el destino":
                ventana_usuario.destino=GuiabuscarGuia(seleccion)
            elif ventana_usuario.opcion=="Ver la disponibilidad de todos los guías según el idioma":
                ventana_usuario.idioma=GuiabuscarGuia(seleccion)
        filtros=[]
        ventana_usuario.modificarTexto("".join(textoBase) + "Actualmente estas viendo la tabla de disponibilidad de los guias registrados, aqui podras filtrar la tabla con\n"
                                       "el menu de filtros que se encuentra en la esquina izquierda, ten en cuenta que los filtros se acomulan y si quieres borrarlos solo debes\n"
                                       "oprimir el boton de borrar filtros, si deseas salir o ver otro tipo de tabla debes oprimir el boton de salir")
        mostrarTabla(ventana_usuario,filtros)
    
    if opcion == 5: # Paso 5 :cambiar tabla
        ventana_usuario.modificarTexto("".join(textoBase) + "Ahora puedes elegir entre ver otro tipo de tabla o salir:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: verDisponibilidadGuias(ventana_usuario, 6, seleccion), tituloValores="¿Qué desea hacer?",  valores=opcionesCambioVerDisponibilidadGuias)
    
    if opcion ==6: # Paso 6 : terminar procesos o cambiar tabla
        if seleccion =="Volver al inicio":
            ventana_usuario.frameImagen()
            ventana_usuario.frameSalida(metodoSalida=lambda: opcionesAdministrador(ventana_usuario))
        elif seleccion=="Cambiar el tipo de tabla":
              verDisponibilidadGuias(ventana_usuario, 0, seleccion)
        else:
             verDisponibilidadGuias(ventana_usuario, 1, seleccion)
        
           
def ingresarActividad(ventana_usuario,opcion=0,seleccion=None):
    """
    Maneja el proceso paso a paso para ingresar una nueva actividad turística, incluyendo la entrada de datos y verificación.
    
    :param ventana_usuario(Tk): Instancia de la ventana principal de usuario.
    :param opcion(int): Fase del proceso para ingresar un guía (0 = entrada de datos básicos, 1 = idiomas, etc.).
    :param seleccion(dict): Datos seleccionados por el usuario (nombre, destino, etc.).
    """
    textoBase=["Actualmente se encuentra en la ventana de ingresar actividad.",
            " A continuación\n le vamos a guiar en el proceso para registrar un nueva actividad turística.\n\n"]
    
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)

    if opcion == 0:  # Paso 0:Ingresar nombre 
        excepcionesIngresarActividad = [
            ("Nombre", lambda seleccion: verificarNombre(seleccion))]
        
        ventana_usuario.modificarTexto("".join(textoBase)+"Empecemos ingresando el nombre que le va asignar a la actividad:")
        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: ingresarActividad(ventana_usuario, 1, seleccion),criterios=["Nombre"], verificaciones=excepcionesIngresarActividad)

    elif opcion == 1:  # Paso 1: Ingresar destino
        ventana_usuario.nombre=(seleccion["Nombre"])
        
        ventana_usuario.tituloResultados()
        ventana_usuario.frameResultados(criterios=["Nombre"], valores=[seleccion["Nombre"]])
        
        ventana_usuario.modificarTexto("".join(textoBase)+"Proceda a seleccionar el destino donde va a estar ubicada la actividad:")
        ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: ingresarActividad(ventana_usuario, 2, seleccion),tituloValores="Seleccione el destino", valores=ListaDestinos)

    elif opcion == 2:  # Paso 2:Ingresar tipos
        ventana_usuario.actividad=Actividad(ventana_usuario.nombre,seleccion)
        
        ventana_usuario.añadirResultado("Destino", seleccion)
        ventana_usuario.modificarTexto("".join(textoBase)+"Ahora ingrese los tipos de actividad que mejor representen a la actividad, elija máximo 2 opciones:")
        ventana_usuario.crearFormulario(tipo_formulario=2, on_accept=lambda seleccion: ingresarActividad(ventana_usuario, 3, seleccion), tituloValores="Seleccione los tipos de actividad",  valores=ListaTipoActividad)

    elif opcion == 3:  # Paso 3: Seleccionar destino
        ventana_usuario.actividad = actividadingresarTipoActividades(ventana_usuario.actividad, seleccion)
        ventana_usuario.actividad=actividadIngresarGuia(ventana_usuario.actividad)
        ventana_usuario.actividad = actividadasignarParametros(ventana_usuario.actividad)
        
        ventana_usuario.borrarResultados("___________ Resumen de la información de la actividad___________")
        ventana_usuario.modificarTexto(textoBase[0]+ "\n🎉🎉Terminaste de ingresar la actividad🎉🎉\n\nAquí podrás ver el resumen de tu ingreso. Esperamos haber sido de utilidad 😊")
        ventana_usuario.frameResumen( lista=ventana_usuario.actividad, metodoSalida=lambda: opcionesAdministrador(ventana_usuario))


def cancelarActividad(ventana_usuario,opcion=0,seleccion=None):
    """
    Maneja el proceso de retirar una actividad turística, ya sea eliminandola definitivamente o sespendiendola por un periodo de tiempo.
    
    :param ventana_usuario: La ventana actual de usuario donde se realizan las operaciones.
    :param opcion: Paso actual del proceso (0: seleccionar tipo de retiro, 1: ingresar guía, 2: retirar guía, 3: finalizar proceso).
    :param seleccion: Datos seleccionados o ingresados por el usuario en el formulario.
    """
    textoBase = [
        "Actualmente se encuentra en la ventana de cancelar actividad.",
        " A continuación\n le vamos a guiar en el proceso para ", "eliminar o suspender", 
        " una actividad turística.\n\n"]
    
    texto_Eliminar = [textoBase[0] + textoBase[1] + "cancelar definitivamente", textoBase[3]]
    texto_suspender = [textoBase[0] + textoBase[1] + "suspender un periodo de tiempo", textoBase[3]]
    
    opcionesCancelarActividad = [
        "Cancelar definitivamente una actividad",
        "Suspender una actividad por un periodo de tiempo"]
    
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    
    if opcion == 0:  # Paso 0: Elegir la opción de tipo de retiro
        ventana_usuario.modificarTexto("".join(textoBase) + "Primero elija la opción que desea realizar:")
        ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: cancelarActividad(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?",  valores=opcionesCancelarActividad)

    elif opcion == 1:  # Paso 1: Ingresar la actividad
        ventana_usuario.tipo_retiro = seleccion
        textoBase = texto_Eliminar if ventana_usuario.tipo_retiro == "Cancelar definitivamente una actividad" else texto_suspender
        excepcionesCancelarActividad0 = [
            ("Nombre", lambda seleccion: verificarNombre(seleccion)),
            ("Destino",lambda seleccion: verificarDestino(seleccion)),
            ("*", lambda seleccion: verificarActividad(seleccion))]
        
        ventana_usuario.modificarTexto("".join(textoBase) + "Ahora ingrese la información de la actividad que desea cancelar (Asegúrese de ingresar una actividad actualmente activa):")
        ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: cancelarActividad(ventana_usuario, 2, seleccion), criterios=["Nombre", "Destino"], verificaciones=excepcionesCancelarActividad0)

    elif opcion == 2:  # Paso 2: Ingresar periodo de tiempo
        ventana_usuario.actividad = ActividadbuscarActividad(seleccion)
        if ventana_usuario.tipo_retiro == "Suspender una actividad por un periodo de tiempo":
            excepcionesCancelarActividad1 = [
                ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
                ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))]
            
            ventana_usuario.modificarTexto("".join(textoBase) + "Por último ingrese el periodo de tiempo en el que se va a suspender la actividad:")
            ventana_usuario.crearFormulario( tipo_formulario=3,  on_accept=lambda seleccion: cancelarActividad(ventana_usuario, 3, seleccion), criterios=["Cantidad de días", "Fecha de inicio"], verificaciones=excepcionesCancelarActividad1)
        else:
            cancelarActividad(ventana_usuario, 3)
    
    elif opcion == 3:  # Paso 3: Cancelar actividad
        if ventana_usuario.tipo_retiro == "Cancelar definitivamente una actividad":
            ventana_usuario.resumen = actividadCancelar()
            ventana_usuario.texto = "eliminado la actividad"
        elif ventana_usuario.tipo_retiro == "Suspender una actividad por un periodo de tiempo":
            periodo_tiempo = mostrarDias(seleccion)
            ventana_usuario.resumen = actividadSuspender(periodo_tiempo)
            ventana_usuario.texto = "suspendido la actividad"
        
        ventana_usuario.borrarResultados("___________ Resumen del proceso realizado___________")
        ventana_usuario.modificarTexto( textoBase[0] + "\n🥳¡Felicidades! Se ha " + ventana_usuario.texto + " con éxito🥳\n\nAquí podrás ver el resumen de la cancelación. Esperamos haber sido de utilidad 😊")
        ventana_usuario.frameResumen(lista=ventana_usuario.resumen, metodoSalida=lambda: opcionesAdministrador(ventana_usuario))

#-----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# -------------------------------------------METODOS EXTRA--------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def mostrarTabla(ventana_usuario,filtros):
    filtrosVerDisponibilidadGuias = [
        "Disponibilidad de todos los guías",
        "Solo los guías disponibles",
        "Solo los guías ocupados"]
    
    tabla=GuiamostrarDisponibilidadGuias(ventana_usuario.fecha,filtros)
    opcion=0 if ventana_usuario=="Ver la disponibilidad de todos los guías según la fecha" else 1 if ventana_usuario=="Ver la disponibilidad de todos los guías según el destino" else 2 if ventana_usuario=="Ver la disponibilidad de todos los guías según el idioma" else 3
    if ventana_usuario.opcionFecha=="Buscar según el mes y el dia":
        encabezados = [
            [ ["Tabla fecha"],["Mes:"]],
            [["Destino:"],["Cantidad de guias:","Cantidad de actividades"],["Mes:"]],
            [["Idioma:"],["Cantidad de guias:","Cantidad de personas"],["Mes:"]],
            [["Guia:","Destino:"],["Mes"]]]
        tituloColumnas=[
            ["Dia","Guias disponibles:","Guias ocupados:","Actividades con guia:","Destino mas usado:","Idioma mas usado:"],
            ["Dia","Guias disponibles:","Guias ocupados:","Actividades con guia:","Actividades sin guia:","Cantidad de personas:"],
            ["Dia","Guias disponibles:","Guias ocupados:","Actividades reservadas:","Grupos:","Destino común:"],
            ["Dia:","Estado","Actividad","Idioma","Cantidad Clientes"]]
        cuerpo=[
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5], tabla[6]],
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5], tabla[6]],
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5], tabla[6]],
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5]]]
            
    else:
        encabezados=[
            [["Tabla fecha"],["Mes:","Dia:"],["Guias disponibles:","Guias ocupados:","Actividades con guia:","Destino mas usado:","Idioma mas usado:"]],                  
            [["Destino:"],["Cantidad de guias:","Cantidad de actividades"],["Mes:","Dia"],["Guias disponibles:","Guias ocupados:","Actividades con guia:","Actividades sin guia:","Idioma mas usado:"]],
            [["Idioma:"],["Cantidad de guias:","Cantidad de personas"],["Mes:","Dia"],["Guias disponibles:","Guias ocupados:","Actividades reservadas:","Grupos:","Destino común:"]],
            [["Guia:","Destino:"],["Mes"]]]
        tituloColumnas=[
            ["Guia","Estado","Actividad","Destino","Idioma"],
            ["Guia","Estado","Actividad","Idioma","Cantidad Clientes"],
            ["Guia","Estado","Actividad","Destino","Cantidad Clientes"],
            ["Dia:","Estado","Actividad","Idioma","Cantidad Clientes"]]
        cuerpo=[
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5]],
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5]],
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5]],
            [tabla[1], tabla[2], tabla[3], tabla[4], tabla[5]]]
        
    ventana_usuario.crearTabla(encabezado=encabezados[opcion], titulo_columnas=tituloColumnas[opcion], filtros=filtrosVerDisponibilidadGuias, on_filtro=lambda filtros:filtrarTabla(ventana_usuario,filtros), eleccion="Salir", on_eleccion=lambda: verDisponibilidadGuias(ventana_usuario, 5))
    

def filtrarTabla(ventana_usuario,filtros):
    ventana_usuario.borrarFilas()