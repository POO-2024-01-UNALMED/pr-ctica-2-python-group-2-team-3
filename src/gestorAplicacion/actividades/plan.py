import pickle
from gestorAplicacion.gestionHum import Guia
from gestorAplicacion.manejoReserva import Actividad, Destino, Grupo, Reserva
from gestorAplicacion.gestionHum import Cliente
from gestorAplicacion.hospedaje import Hotel

class Plan:
    paquetes = []

    def __init__(self, tipo=None, destino=None, actividades=None, clasificacion=None, reserva=None):
        if actividades is None:
            actividades = []
        self.tipo = tipo
        self.destino = destino
        self.actividades = actividades
        self.precio = 0
        self.clasificacion = clasificacion
        self.grupos = []
        self.reserva = reserva
        self.cantidadDias = 0
        self.disponibilidadHabitaciones = {}

        if reserva:
            self.reserva.setPlan(self)
            self.tipo = reserva.getTipoPlan()

    def añadirActividad(self, actividad):
        self.actividades.append(actividad)

    @staticmethod
    def mostrarNombreActividad(actividades):
        nombres = []
        for actividad in actividades:
            nombres.append(actividad.getNombre())
        return nombres

    def mostrarNombreActividad(self):
        nombres = []
        for actividad in self.actividades:
            nombres.append(actividad.getNombre())
        return nombres

    def escogerActividadesIniciales(self, actividadesDisponibles, seleccionadas):
        seleccionInicial = []
        for nombre in seleccionadas:
            for actividad in actividadesDisponibles:
                if actividad.getNombre() == nombre:
                    seleccionInicial.append(actividad)
        return seleccionInicial

    def actividadesDisponiblesDia(self, fecha, seleccionInicial):
        actividadesDisponibles = []
        for actividad in seleccionInicial:
            existenGrupos = Grupo.buscarGrupo(fecha, actividad, self.reserva.getIdiomas()[0], self.reserva.getClientes())
            if len(existenGrupos) > 0:
                actividadesDisponibles.append(actividad)
            else:
                guiasCapacitados = actividad.buscarGuia(self.reserva.getIdiomas()[0])
                guiasConDisponibilidad = Guia.buscarDisponibilidad(guiasCapacitados, fecha)
                if len(guiasConDisponibilidad) > 0:
                    actividadesDisponibles.append(actividad)
        return actividadesDisponibles

    def escogerActividadesDia(self, actividadesPosibles, actividadEscogida, fecha):
        for nombre in actividadEscogida:
            for actividad in actividadesPosibles:
                if actividad.getNombre() == nombre:
                    self.actividades.append(actividad)
                    existenGrupos = Grupo.buscarGrupo(fecha, actividad, self.reserva.getIdiomas()[0], self.reserva.getClientes())
                    if len(existenGrupos) > 0:
                        existenGrupos[0].getListaReservas().append(self.reserva.getClientes())
                        self.grupos.append(existenGrupos[0])
                    else:
                        grupo = Grupo(actividad, self.reserva.getClientes(), fecha, self.reserva.getIdiomas()[0])
                        self.grupos.append(grupo)
        self.asignarPrecio()

    def escogerActividadesDiaPaquete(self, actividadesPosibles, actividadEscogida, fecha):
        for nombre in actividadEscogida:
            for actividad in actividadesPosibles:
                if actividad.getNombre() == nombre:
                    existenGrupos = Grupo.buscarGrupo(fecha, actividad, self.reserva.getIdiomas()[0], self.reserva.getClientes())
                    grupo = Grupo(actividad, self.reserva.getClientes(), fecha, self.reserva.getIdiomas()[0])
                    self.grupos.append(grupo)
        self.asignarPrecio()

    @staticmethod
    def paquetesDisponibles(cantidadPersonas, destino, clasificacion, fechas):
        paquetesPosibles = []
        for plan in Plan.paquetes:
            fechasDisponibles = []
            for fecha in fechas:
                if plan.getDestino() == destino and plan.getClasificacion() <= clasificacion and len(plan.getActividades()) >= len(fechas):
                    for actividad in plan.getActividades():
                        existenGrupos = Grupo.buscarGrupo(fecha, actividad, plan.getReserva().getIdiomas()[0], cantidadPersonas)
                        if len(existenGrupos) > 0:
                            fechasDisponibles.append(fecha)
            if len(fechasDisponibles) == len(fechas):
                paquetesPosibles.append(plan)
        return paquetesPosibles

    @staticmethod
    def asignarTipo(valor):
        if valor == 1:
            return "PP"
        elif valor == 2:
            return "PT"
        return ""

    def asignarPrecio(self):
        for actividad in self.getActividades():
            self.precio += actividad.getPrecio()

    @staticmethod
    def stringPaqueteTuristico(plan):
        paquete = f"Destino: {plan.getDestino().getNombre()}\n"
        paquete += "Actividades: "
        for actividad in plan.getActividades():
            paquete += f"{actividad.getNombre()}, "
        paquete += f"\nPrecio por persona: {plan.getPrecio()}\n"
        return paquete

    # Métodos de acceso

    def getPaquetes(self):
        return Plan.paquetes

    def setPaquetes(self, paquetes):
        Plan.paquetes = paquetes

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getDestino(self):
        return self.destino

    def setDestino(self, destino):
        self.destino = destino

    def getActividades(self):
        return self.actividades

    def setActividades(self, actividades):
        self.actividades = actividades

    def getPrecio(self):
        return self.precio

    def setPrecio(self, precio):
        self.precio = precio

    def getClasificacion(self):
        return self.clasificacion

    def setClasificacion(self, clasificacion):
        self.clasificacion = clasificacion

    def getGrupos(self):
        return self.grupos

    def setGrupos(self, grupos):
        self.grupos = grupos

    def getReserva(self):
        return self.reserva

    def setReserva(self, reserva):
        self.reserva = reserva