import tkinter as tk
from modulos.excepciones import *
from modulos.metodos import *

def reservarActividades(ventana_usuario, opcion=0, opcionEscogidaAdmin=None):
        textoBase=["Actualmente se encuentra en la ventana de reservar actividades turísticas. Aqui podras registrar tu reserva,",
            "\ncomprar una suscripcion y elegir un plan personalizado de actividades o un paquete turístico ya planeado.\n\n"]
    
        ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)

        if opcion == 0:  # Paso 0:Ingresar opcion de reserva
                opcionesReservarActividades=[
                        "Realizar una nueva reserva",
			"Buscar reserva existente para agregar las actividades"]
        
                ventana_usuario.modificarTexto("".join(textoBase)+"Empecemos eligiendo su tipo de reserva, si ya tienes una reserva creada anteriormente y quieres añadirle un plan de actividades\npuedes busacr tu reserva anterios con el codigo que te dieron, pero si no tienes ninguna reserva creada no te preocupes aca podras crear tu reserva desde cero 😊:")
                ventana_usuario.crearFormulario(tipo_formulario=0, on_accept=lambda seleccion: reservarActividades(ventana_usuario, 1, seleccion), tituloValores="¿Qué desea hacer?", valores=opcionesReservarActividades)
        if opcion == 1: # Paso 1: Realizar reserva
                if opcion =="Buscar reserva existente para agregar las actividades":
                        excepcionesReservarActividades1 = [
                        ("Codigo", lambda seleccion: verificarCodigo(seleccion))]
                        
                        ventana_usuario.modificarTexto("".join(textoBase)+"Empecemos ingresando el codigo de tu reserva, recuerda que es el codigo que te dieron al realizar tu reserva:")
                        ventana_usuario.crearFormulario(tipo_formulario=3, on_accept=lambda seleccion: reservarActividades(ventana_usuario, 2, seleccion),criterios=["Codigo"], verificaciones=excepcionesReservarActividades1)
                else:
                        ventana_usuario.reserva=realizarReserva(ventana_usuario=ventana_usuario,textobase=textoBase[0])



def realizarReserva(ventana_usuario, opcion=0, seleccion=None, textobase=None):
        ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
        ventana_usuario.texto_base=textobase if textobase is not None else "Actualmente se encuentra creando una nueva reserva.\n"
        if opcion == 0:
                excepcionesReservarActividades0 = [
                ("Cantidad de días", lambda seleccion: verificarNumero(seleccion)),
                ("Fecha de inicio", lambda seleccion: verificarFormato(seleccion, "Fecha de inicio", 1))]
            
                ventana_usuario.modificarTexto("".join(ventana_usuario.texto_base) + "Empezaremos a crear su reserva desde 0, primero ingrese el periodo de tiempo en el que planea reservar:")
                ventana_usuario.crearFormulario( tipo_formulario=3,  on_accept=lambda seleccion: realizarReserva(ventana_usuario, 1, seleccion), criterios=["Cantidad de días", "Fecha de inicio"], verificaciones=excepcionesReservarActividades0)
        if opcion == 1:
                ventana_usuario.fecha=seleccion
                ventana_usuario.tituloResultados()
                ventana_usuario.frameResultados(criterios=["Cantidad de días","Fecha de inicio"], valores=[seleccion["Cantidad de días"],seleccion["Fecha de inicio"]])
                
                excepcionesReservarActividades1 = [
                ("Nombre", lambda seleccion: verificarNombre(seleccion)),
                ("Edad", lambda seleccion: verificarTitular(seleccion))]
                
                ventana_usuario.modificarTexto("".join(ventana_usuario.textoBase) + "Ahora ingrese la información de la persona que va a ser el titular de la reserva:")
                ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 2, seleccion), criterios=["Nombre", "Edad"], verificaciones=excepcionesReservarActividades1)
        if opcion == 2:
                ventana_usuario.titular=SuscripcionverificarSuscripcion(seleccion)
                ventana_usuario.frameResultados(criterios=["Nombre del titular:","Edad del titular:"], valores=[seleccion["Nombre"],seleccion["Edad"]])
                
                if ventana_usuario.titular==None:
                     ventana_usuario.titular=newCliente(seleccion)
                     ventana_usuario.modificarTexto("".join(ventana_usuario.textoBase) + "Actualmente no cuenta con una suscripción con nosotros, elija como quiere proceder con su reserva:")
                     ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 3, seleccion), tituloValores="¿Desea comprar una suscripción para recibir descuentos impresionantes para su reserva?",  valores=["Si quiero comprar","No, gracias"])
                else:
                    realizarReserva(ventana_usuario, 3)
        
        if opcion==3:
                if seleccion=="Si quiero comprar":
                       ventana_usuario.suscripcion=comprarSuscripcion(ventana_usuario)
                else:
                        ventana_usuario.suscripcion="No se aplicara una suscripcion a la reserva"
                ventana_usuario.frameResultados(criterios=["Suscripcion:"], valores=[seleccion[ventana_usuario.suscripcion]])
                excepcionesReservarActividades2 = [
                        ("Cantidad de clientes", lambda seleccion: verificarNumero(seleccion))]
                ventana_usuario.reserva=newReserva()
                ventana_usuario.modificarTexto("".join(ventana_usuario.textoBase) + "Ingrese la cantidad de clientes que van a reservar, sin contar al titular:")
                ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 4, seleccion), criterios=["Cantidad de clientes"], verificaciones=excepcionesReservarActividades2)
        if opcion==4:
                ventana_usuario.cantidadClientes=int(seleccion)
                realizarReserva(ventana_usuario, 5)
        if opcion==5:
                if seleccion==None:
                        ventana_usuario.contador=0
                        ventana_usuario.clientes=[]
                else:
                       ventana_usuario.contador+=1
                       cliente=ingresarCliente(seleccion)
                       ventana_usuario.reserva.append(cliente)
                       ventana_usuario.clientes.append(cliente)
                seleccionx="None" if ventana_usuario.contador==ventana_usuario.cantidadClientes else None
                realizarReserva(ventana_usuario, 6,seleccionx)
        if opcion==6:
                if seleccion=="None":
                        ventana_usuario.frameResultados(criterios=["Clientes:"], valores=ventana_usuario.clientes)
                        ventana_usuario.reserva=asignarClasificacion(ventana_usuario.reserva)
                        ventana_usuario.reserva=aplicarSuscripcion(ventana_usuario.reserva)
                else: 
                        excepcionesReservarActividades3 = [
                        ("Nombre", lambda seleccion: verificarNombre(seleccion)),
                        ("Edad", lambda seleccion: verificarTitular(seleccion))]
                        
                        ventana_usuario.modificarTexto("".join(ventana_usuario.textoBase) + "Ahora ingrese la infomarcion del cliente "+ventana_usuario.contador+":")
                        ventana_usuario.crearFormulario( tipo_formulario=3, on_accept=lambda seleccion: realizarReserva(ventana_usuario, 5, seleccion), criterios=["Nombre", "Edad"], verificaciones=excepcionesReservarActividades3)
        return ventana_usuario.reserva
                     
def comprarSuscripcion(ventana_usuario,opcion=0,seleccion=None):
        suscripcionesDisponibles = SuscripcionmostrarPosiblesSuscripciones()
        if opcion==0:
                ventana_usuario.modificarTexto("".join(ventana_usuario.textoBase) + "Actualmente no cuenta con una suscripción con nosotros, elija como quiere proceder con su reserva:")
                ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: comprarSuscripcion(ventana_usuario, 1, seleccion), tituloValores="¿Desea comprar una suscripción para recibir descuentos impresionantes para su reserva?",  valores=["Si quiero comprar","No, gracias"])
        
        if opcion==1:
                if seleccion=="Básica":
                        nuevaSuscripcion= newSuscripcion(ventana_usuario.titular)
                elif seleccion=="General":
                         nuevaSuscripcion= newSuscripcion(ventana_usuario.titular)
                elif seleccion== "Premium":
                        nuevaSuscripcion= newSuscripcion(ventana_usuario.titular)
                elif seleccion=="VIP":
                         nuevaSuscripcion= newSuscripcion(ventana_usuario.titular)
        return nuevaSuscripcion

def elegirPlanTuristico(ventana_usuario,opcion=0,seleccion=None):
        ventana_usuario.borrarFrame(ventana_usuario.procesosYConsultas_frame)
        planesPosibles = ["Plan personalizado (Se escogen las actividades desde 0 de manera manual)",
			"Paquete turistico (Se escoge un plan turistico predefinido, con actividades generales ya establecidas)"]
	
        if opcion==0:
                ventana_usuario.modificarTexto("".join(ventana_usuario.textoBase) + "Ahora te guiaremos para que elijas tu plan o paquete turistico, primero elije la opcion que deseas realizar:")
                ventana_usuario.crearFormulario( tipo_formulario=0, on_accept=lambda seleccion: comprarSuscripcion(ventana_usuario, 1, seleccion), tituloValores="¿Que desea hacer?",  valores=planesPosibles)
        if opcion==1:
                pass