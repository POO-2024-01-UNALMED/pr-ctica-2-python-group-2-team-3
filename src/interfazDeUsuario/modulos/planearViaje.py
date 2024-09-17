import tkinter as tk
from tkinter import messagebox
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

reserva=Reserva()
textoBase = [
        "Actualmente se encuentra en la ventana de planear viaje. Aquí podrás planear todos los elementos de tu próximo viaje.\n"
        "Si ya tienes algo definido puedes ingresarlo y nosotros nos ocuparemos de mostrarte las mejores opciones para tu elección o "
        "puedes planear todo desde cero.\n\n"]

def funPlanearViaje(ventana_usuario):
    """
    Destruye la interfaz de procesos actual y modifica el título de la ventana para iniciar el proceso de planear un viaje.

    :param ventana_usuario: Objeto que representa la ventana del usuario.
    :type ventana_usuario: VentanaUsuario
    """
    ventana_usuario.destruirInterfazProcesos()
    ventana_usuario.modificarTitulo("Planear viaje")
    planearViaje(ventana_usuario)

def planearViaje(ventana_usuario, opcion=0, seleccion=None):
    """
    Función que guía al usuario en el proceso de planear un viaje paso a paso, permitiéndole seleccionar
    destinos, fechas, idiomas, paquetes turísticos, hoteles, entre otros.

    :param ventana_usuario: Objeto que representa la ventana del usuario.
    :type ventana_usuario: VentanaUsuario
    :param opcion: Indica el paso actual en el proceso de planificación del viaje.
    :type opcion: int
    :param seleccion: Selección del usuario en cada paso del proceso.
    :type seleccion: str or dict
    """
    
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    
    if opcion == 0: #Paso 0: elegir opcion destino y crear tabla si es necesario
        if seleccion:
            if seleccion == "Buscar las mejores opciones de destinos":
                mostrarTabla(ventana_usuario, "Destino", lambda: planearViaje(ventana_usuario, 1))
            else:
                planearViaje(ventana_usuario, 1)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) +"Primero empezaremos definiendo el destino. Puedes elegir entre ingresar el destino "
                                           "que ya tenías planeado o buscar entre nuestros destinos la opción que mejor se acomode a tus gustos:")
            ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 0, seleccion), tituloValores="¿Qué desea hacer?", valores=["Ingresar destino", "Buscar las mejores opciones de destinos"])
    
    if opcion == 1: #Paso 1: Ingresar destino
        if seleccion:
            reserva.set_destinoNombre(seleccion)
            ventana_usuario.tituloResultados()
            ventana_usuario.frameResultados(criterios=["Destino:"], valores=[seleccion])
            planearViaje(ventana_usuario, 2)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) +  "Genial, empezaremos ingresando el destino. Selecciona la opción del destino que "
                                           "prefieras:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 1, seleccion), tituloValores="Elige el destino:", valores=ListaDestinos )
    
    if opcion == 2: #Paso 2: elegir opcion fecha y crear tabla si es necesario
        if seleccion:
            if seleccion == "Buscar las mejores opciones de fechas":
                mostrarTabla(ventana_usuario, "Fecha", lambda: planearViaje(ventana_usuario, 3))
            else:
                planearViaje(ventana_usuario, 3)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) + "Ahora definiremos la fecha. Puedes elegir entre ingresar las fechas que ya "
                                           "tenías pensadas o buscar cuáles son las mejores fechas para visitar el destino escogido:")
            ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 2, seleccion), tituloValores="¿Qué desea hacer?", valores=["Ingresar fecha", "Buscar las mejores opciones de fechas"])
    
    if opcion == 3: #Paso 3: Ingresar periodo de fechas
        if seleccion:
            cantidad = int(seleccion["Cantidad de días"])
            fecha = seleccion["Fecha de inicio"]
            fechas = Reserva.mostrarDias(cantidad, fecha)
            reserva._fechas=fechas
            ventana_usuario.añadirResultado("Fechas", fechas[0] + " - " + fechas[-1])
            planearViaje(ventana_usuario, 4)
        else:
            excepcionesPlanearFecha = [
                ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
                ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))
            ]
            ventana_usuario.modificarTexto("".join(textoBase) + "Ahora ingrese el periodo de fechas en el que desea planear su viaje:")
            ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: planearViaje(ventana_usuario, 3, seleccion), criterios=["Cantidad de días", "Fecha de inicio"],verificaciones=excepcionesPlanearFecha)
    
    if opcion == 4: #Paso 4: elegir opcion idioma y crear tabla si es necesario
        if seleccion:
            if seleccion == "Buscar las mejores opciones de idiomas":
                mostrarTabla(ventana_usuario, "Idioma", lambda: planearViaje(ventana_usuario, 5))
            else:
                planearViaje(ventana_usuario, 5)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) +"Seguimos eligiendo el idioma. Puedes elegir entre ingresar el idioma que va "
                                           "a necesitar el guía turístico o buscar los idiomas con mayor disponibilidad:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 4, seleccion), tituloValores="¿Qué desea hacer?", valores=["Ingresar Idioma", "Buscar las mejores opciones de idiomas"])
    
    if opcion == 5: #Paso 5: Ingresar idioma
        if seleccion:
            reserva.set_idiomas(seleccion)
            ventana_usuario.añadirResultado("Idioma", seleccion)
            planearViaje(ventana_usuario, 6)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) + "Ingrese el idioma que desea que utilice el guía turístico en las diferentes actividades de su plan:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 5, seleccion), tituloValores="Elige el idioma:",valores=ListaIdiomas)
    
    if opcion == 6: #Paso 6: elegir opcion paquete turistico y crear tabla si es necesario
        if seleccion:
            if seleccion == "Buscar las mejores opciones de paquetes turísticos":
                mostrarTabla(ventana_usuario, "Plan", lambda: planearViaje(ventana_usuario, 7))
            else:
                planearViaje(ventana_usuario, 7)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) +"Llegó el momento de elegir tu plan turístico. Ten en cuenta que por la versatilidad "
            "de los planes personalizados aquí\nsolo podrás ingresar un paquete turístico o ver las opciones de paquetes turísticos que más se adapten a tus gustos:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 6, seleccion),  tituloValores="¿Qué desea hacer?", valores=["Ingresar paquete turístico", "Buscar las mejores opciones de paquetes turísticos"])
    
    if opcion == 7: #Paso 7: Ingresar paquete turistico
        if seleccion:
            reserva.set_paquete_turistico(seleccion)
            ventana_usuario.añadirResultado("Paquete turístico", seleccion)
            planearViaje(ventana_usuario, 8)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) +"Ahora elige el paquete turístico que más te gustó:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 7, seleccion), tituloValores="Elige el paquete turístico:", valores=Plan.generar_paquetes_turisticos())
    
    if opcion == 8: #Paso 8: elegir opcion hotel y crear tabla si es necesario
        if seleccion:
            if seleccion == "Buscar las mejores opciones de hoteles":
                mostrarTabla(ventana_usuario, "Hotel", lambda: planearViaje(ventana_usuario, 9))
            else:
                planearViaje(ventana_usuario, 9)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) +"Por último vamos a planear tu hospedaje. Ten en cuenta que no podemos garantizar la "
            "disponibilidad de las habitaciones en el momento en que realices la reserva\npor lo tanto solo podrás hacer una predicción del hospedaje "
            "de una sola habitación. Ahora elige entre seleccionar un hotel o ver las opciones de hoteles que más se adapten a tus gustos:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 8, seleccion), tituloValores="¿Qué desea hacer?",  valores=["Ingresar un hotel", "Buscar las mejores opciones de hoteles"])
    
    if opcion == 9: #Paso 9: Ingresar hotel
        if seleccion:
            reserva.set_hotel(seleccion)
            ventana_usuario.añadirResultado("Hotel", seleccion)
            planearViaje(ventana_usuario, 10)
        else:
            ventana_usuario.modificarTexto("".join(textoBase) +"Elige el hotel que más te llamó la atención:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: planearViaje(ventana_usuario, 9, seleccion), tituloValores="Elige el hotel:",valores=Hotel.mostrarHoteles())
    
    if opcion == 10: #Paso 10: Ingresar cantidad de personas para realizar el presupuesto
        if seleccion:
            reserva.set_cantidadClientes(int(seleccion["Cantidad de personas"]))
            reserva.definirPrecio()
            planearViaje(ventana_usuario, 11)
        else:
            excepcionesPlanearPresupuesto = [
                ("Cantidad de personas", lambda seleccion: verificarNumero(seleccion))
            ]
            ventana_usuario.modificarTexto("".join(textoBase) +"Ahora ingrese la cantidad de personas para las cuales quiere hacer su presupuesto:")
            ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: planearViaje(ventana_usuario, 10, seleccion), criterios=["Cantidad de personas"], verificaciones=excepcionesPlanearPresupuesto)
    
    if opcion == 11: #Paso 11: Mostrar resumen
        ventana_usuario.borrarResultados("___________ Resumen del viaje planeado___________")
        ventana_usuario.modificarTexto(
            "🥳 ¡Felicidades! Haz planeado tu viaje con éxito 🥳\n"
            "Aquí podrás ver el resumen del plan y la predicción del presupuesto final. Ten en cuenta que no podemos asegurar la disponibilidad y el precio de ninguno de nuestros servicios.\n"
            "Para utilizar los datos planeados guarda muy bien el código de la reserva. Esperamos haber sido de utilidad 😊"
        )
        ventana_usuario.frameResumen( lista=reserva.resumenViaje(), metodoSalida=lambda: planearViaje(ventana_usuario))

def mostrarTabla(ventana_usuario, tipo, metodoSalida):
    """
    Muestra una tabla con las mejores opciones disponibles según el tipo de selección (Destino, Fecha, Idioma, etc.).
    
    :param ventana_usuario: Objeto que representa la ventana del usuario.
    :type ventana_usuario: VentanaUsuario
    :param tipo: Tipo de datos que se mostrarán en la tabla (Destino, Fecha, Idioma, etc.).
    :type tipo: str
    :param metodoSalida: Función a ejecutar cuando el usuario decide salir de la tabla.
    :type metodoSalida: function
    """
    from datetime import datetime

    opcion = 0 if tipo == "Destino" else 1 if tipo == "Fecha" else 2 if tipo == "Idioma" else 3 if tipo == "Plan" else 4
    filtros = [
        "Filtrar según una clasificación", "Filtrar según un idioma", "Filtrar según un tipo de actividad",
        "Filtrar según una fecha", "Cambiar destino", "Cambiar idioma", "Cambiar fechas"
    ]

    if tipo == "Destino":
        filtros.remove("Cambiar destino")
        filtros.remove("Cambiar idioma")
        filtros.remove("Cambiar fechas")
    elif tipo == "Fecha":
        filtros.remove("Cambiar idioma")
        filtros.remove("Cambiar fechas")
    elif tipo == "Idioma":
        filtros.remove("Cambiar idioma")
        filtros.remove("Filtrar según un idioma")
        filtros.remove("Filtrar según una fecha")
    else:
        filtros.remove("Filtrar según un idioma")
        filtros.remove("Filtrar según una fecha")

    destino = reserva.get_destinoNombre() if reserva.get_destinoNombre() is not None else "Cartagena"
    fechas = reserva.get_fechas()  
    dia = "1/1/2024" if not fechas else fechas[0] 
    mes = datetime.strptime(dia, '%d/%m/%Y').strftime('%B') if reserva.get_fechas() is not None else "Enero"
    cantidadDias = len(reserva.get_fechas()) if reserva.get_fechas() is not None else "30"
    idiomas=reserva.get_idiomas()
    idioma = "Español"  if not idiomas or idiomas is None else reserva.get_idiomas() 

    encabezados = [
        [["Tabla destinos"]], [["Tabla fechas"], ["Destino: " + destino]],
        [["Tabla idiomas"], ["Destino: " + destino], ["Mes: " + mes]],
        [["Tabla paquetes turísticos"], ["Destino: " + destino, "Idioma: " + idioma],["Cantidad días: " + str(cantidadDias),"Fecha inicio: " + dia]],
        [["Tabla hoteles"], ["Destino: " + destino, "Idioma: " + idioma],["Cantidad días: " + str(cantidadDias),"Fecha inicio: " + dia]]]
    

    tituloColumnas = [
        ["Destino", "Actividades", "Promedio $actividades", "Hoteles", "Promedio $hoteles", "Tipo de actividad común", "Idioma común"],
        ["Mes", "Promedio $actividades", "Promedio $hoteles", "Cantidad personas", "Temporada"],
        ["Idioma", "Actividades", "Promedio $actividades", "Guías capacitados", "Tipo de actividad predominante", "Cantidad personas", "Disponibilidad"],
        ["Paquete turístico", "Capacidad", "Precio", "Clasificación", "Tipo de actividad predominante", "Disponibilidad"],
        ["Hotel", "Habitaciones", "Precio", "Suscripción", "Restaurantes", "Restaurante mejor calificado", "Promedio $restaurantes", "Disponibilidad"]
    ]

    ventana_usuario.crearTabla(encabezado=encabezados[opcion], titulo_columnas=tituloColumnas[opcion], filtros=filtros,on_filtro=lambda filtros: filtrarTabla(ventana_usuario=ventana_usuario, opcion=tipo,filtros=filtros,metodoSalida=metodoSalida),eleccion="Salir", on_eleccion=metodoSalida)
    mostrarCuerpo(ventana_usuario, tipo)

        
def mostrarCuerpo(ventana_usuario, opcion, filtros=None):

    destino = reserva.get_destinoNombre() or None
    idioma = reserva.get_idiomas() or None
    tipo = reserva.get_tipo_plan() or None
    clasificacion = reserva.get_clasificacion() or None
    
    if opcion == "Destino":
        for destino in ListaDestinos:
            tabla = Destino.mostrarTablas(idioma=idioma, tipo=tipo, clasificacion=clasificacion, filtros=filtros)
            ventana_usuario.añadirFila([destino, tabla["Objetos"], tabla["Precios"], tabla["Objetos"], tabla["Precios"], tabla["Tipo"], tabla["Idioma"]])
            
    elif opcion == "Fecha":
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        for mes in meses:
            tabla = Destino.mostrarTablas(idioma=idioma, tipo=tipo, clasificacion=clasificacion, filtros=filtros)
            ventana_usuario.añadirFila([mes, tabla["Precios"], tabla["Precios"], tabla["Personas"], tabla["Disponibilidad"]])
    
    elif opcion == "Idioma":
        for idioma in ListaIdiomas:
            tabla = Destino.mostrarTablas(idioma=idioma, tipo=tipo, clasificacion=clasificacion, filtros=filtros)
            ventana_usuario.añadirFila([idioma, tabla["Objetos"], tabla["Precios"], tabla["Objetos"], tabla["Tipo"], tabla["Personas"], tabla["Disponibilidad"]])
    
    elif opcion == "Plan":
                conteo=0
                paquetes = [
                "Tour 5 Cascadas", "Expedición al Amazonas", "Tour por Cascadas", "Aventura en la Playa", "Recorrido artístico", "Naturaleza y Descanso",
                "Escapada Romántica", "Exploración Urbana", "Ruta del Café", "Safari Fotográfico", "Senderismo en Montañas", "Crucero de Lujo",
                "Tour Gastronómico", "Descubre las Islas", "Aventura Extrema"
                ]
                for paquete in paquetes:
                        conteo+=1
                        print("estoy en el for"+paquete)
                        tabla = Destino.mostrarTablas(idioma=idioma, tipo=tipo, clasificacion=clasificacion, filtros=filtros)
                        ventana_usuario.añadirFila([paquete, tabla["Capacidad"], tabla["Precios"], tabla["Clasificacion"], tabla["Tipo"], tabla["Disponibilidad"]])
                        if conteo>9:break
                        
    elif opcion== "Hotel":
        conteo=0
        for hotel in Hotel.mostrarHoteles():
                conteo+=1
                tabla = Destino.mostrarTablas(idioma=idioma, tipo=tipo, clasificacion=clasificacion, filtros=filtros)
                ventana_usuario.añadirFila([hotel, tabla["Objetos"], tabla["Precios"], tabla["Suscripcion"], tabla["Objetos"], tabla["Restaurantes"], tabla["Precios"], tabla["Disponibilidad"]])
                if conteo>9: break
                
def filtrarTabla(ventana_usuario, opcion,metodoSalida, paso=0, seleccion=None, filtros=None):
    ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
    filtros_disponibles = [
        "Filtrar según una clasificación", "Filtrar según un idioma", "Filtrar según un tipo de actividad",
        "Filtrar según una fecha", "Cambiar destino", "Cambiar idioma", "Cambiar fechas"
    ]
    clasificacion_opciones = ["años<7", "7<años13", "13<años<18", "18<años"]
    texto = "".join(textoBase) + f"Actualmente estás filtrando la tabla de {opcion}."
    
    if paso == 0:
        ventana_usuario.opcion=None
        if filtros_disponibles[0] in filtros:
            ventana_usuario.modificarTexto(texto + " Seleccione la clasificación por la cual quiere filtrar:")
            ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: filtrarTabla(ventana_usuario=ventana_usuario, metodoSalida=metodoSalida,opcion=opcion, paso=1, seleccion=seleccion, filtros=filtros), tituloValores="Elige la clasificación:", valores=clasificacion_opciones )
            ventana_usuario.opcion=0
            
        elif (filtros_disponibles[1] or filtros_disponibles[-2]) in filtros:
            ventana_usuario.modificarTexto(texto + " Seleccione el idioma por el cual quiere filtrar:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: filtrarTabla(ventana_usuario=ventana_usuario, metodoSalida=metodoSalida,opcion=opcion, paso=1, seleccion=seleccion, filtros=filtros), tituloValores="Elige el idioma:", valores=ListaIdiomas )
            ventana_usuario.opcion=1
            
        elif filtros_disponibles[2] in filtros:
            ventana_usuario.modificarTexto(texto + " Seleccione el tipo de actividad por la cual quiere filtrar:")
            ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: filtrarTabla(ventana_usuario=ventana_usuario, metodoSalida=metodoSalida,opcion=opcion, paso=1, seleccion=seleccion, filtros=filtros), tituloValores="Elige el tipo de actividad:", valores=ListaTipoActividad )
            ventana_usuario.opcion=2
            
        elif (filtros_disponibles[3] or filtros_disponibles[-1]) in filtros:
            ventana_usuario.modificarTexto(texto + " Ingrese las fechas por las cuales quiere filtrar:")
            excepcionesPlanearFecha = [
                ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
                ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))
            ]
            ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: filtrarTabla(ventana_usuario=ventana_usuario, metodoSalida=metodoSalida,opcion=opcion, paso=1, seleccion=seleccion, filtros=filtros), criterios=["Cantidad de días", "Fecha de inicio"], verificaciones=excepcionesPlanearFecha)
            ventana_usuario.opcion=3
        ventana_usuario.borrarFiltros()
        
    else:
        print("Pase por el else")
        if ventana_usuario.opcion==0:
                reserva.set_clasificacion(seleccion)
                print("pase por clasificacion")
        
        elif ventana_usuario.opcion==1:
                print(seleccion)
                reserva.set_idiomas(seleccion)
        
        elif ventana_usuario.opcion==2:
                reserva.set_tipo_plan(seleccion)
        
        elif ventana_usuario.opcion==3:
                cantidad = int(seleccion["Cantidad de días"])
                fecha = seleccion["Fecha de inicio"]
                fechas = Reserva.mostrarDias(cantidad, fecha)
                reserva.set_fechas(fechas)
        
        mostrarTabla(ventana_usuario =ventana_usuario ,tipo=opcion,metodoSalida=metodoSalida)
