
from typing import List, Optional
import copy

from gestorAplicacion.enums import idiomas, tiposActividad
from gestorAplicacion.gestionHum import cliente, guia
from gestorAplicacion.manejoReserva import reserva, actividad
from gestorAplicacion.manejoReserva import destino

class Grupo:
    grupos = []

    def __init__(self, guia: Optional[guia] = None, 
                 fecha: Optional[List[int]] = None, 
                 actividad: Optional[actividad] = None, 
                 idioma: Optional[idiomas] = None, 
                 listaReservas: Optional[List[List[cliente]]] = None, 
                 tipoHabitacion: Optional[str] = None, 
                 capacidad: Optional[int] = None, 
                 tipoMesa: Optional[str] = None):
        """
        Inicializa una instancia de Grupo.

        :param guia: Guia asignado al grupo.
        :param fecha: Fecha del grupo (en formato [año, mes, día]).
        :param actividad: Actividad del grupo.
        :param idioma: Idioma del grupo.
        :param listaReservas: Lista de reservas del grupo.
        :param tipoHabitacion: Tipo de habitación del grupo.
        :param capacidad: Capacidad máxima del grupo.
        :param tipoMesa: Tipo de mesa del grupo.
        """
        self.fecha = fecha
        self.guia = guia
        self.actividad = actividad
        self.idioma = idioma
        self.listaReservas = listaReservas if listaReservas is not None else []
        self.capacidad = capacidad
        self.clasificacion = self.actividad.getClasificacion() if self.actividad else 0
        self.tipoMesa = tipoMesa
        self.tipoHabitacion = tipoHabitacion
        self.fechaOcupadas = []
        self.clientes = []

        Grupo.grupos.append(self)

    @staticmethod
    def retirarGuia(guia: Guia, fecha: List[int]):
        """
        Retira un guía y reasigna sus reservas a otros grupos disponibles.

        :param guia: Guia a retirar.
        :param fecha: Fecha del grupo del guía.
        """
        grupo = next((x for x in Grupo.grupos if x.guia == guia and x.fecha == fecha), None)
        if grupo:
            reemplazo = grupo.elegirGuia()
            if reemplazo is None:
                gruposSustitutos = Grupo.buscarGrupo(grupo.fecha, grupo.actividad, grupo.idioma)
                listaReservasPendientes = copy.deepcopy(grupo.listaReservas)
                for x in gruposSustitutos:
                    reservasPendientes = x.reubicarReservas(listaReservasPendientes)
                    if not reservasPendientes:
                        break
                    listaReservasPendientes = reservasPendientes
                if listaReservasPendientes:
                    for reserva in listaReservasPendientes:
                        reservaFaltante = Reserva.buscarReserva(grupo, reserva)
                        reservaFaltante.cancelarActividad(grupo.actividad)
                Grupo.grupos.remove(grupo)
            else:
                grupo.guia = reemplazo
                diasOcupados = reemplazo.getDiasOcupados()
                diasOcupados.append(fecha)
                reemplazo.setDiasOcupados(diasOcupados)

    def retirarClientes(self, reserva: List[Cliente]) -> bool:
        """
        Retira una reserva de clientes del grupo y reubica las reservas si es necesario.

        :param reserva: Reserva de clientes a retirar.
        :return: True si el grupo ha sido removido, False de lo contrario.
        """
        self.listaReservas.remove(reserva)
        gruposSustitutos = Grupo.buscarGrupo(self.fecha, self.actividad, self.idioma)
        listaReservasPendientes = copy.deepcopy(self.listaReservas)
        for x in gruposSustitutos:
            reservasPendientes = x.reubicarReservas(listaReservasPendientes)
            if not reservasPendientes:
                break
            listaReservasPendientes = reservasPendientes
        if not listaReservasPendientes:
            diasOcupados = self.guia.getDiasOcupados()
            diasOcupados.remove(self.fecha)
            self.guia.setDiasOcupados(diasOcupados)
            Grupo.grupos.remove(self)
            return True
        return False

    def verificarParametrosGrupo(self, idiomaVerificable: Idiomas, fechasVerificables: List[List[int]], clientesVerificables: List[Cliente]) -> bool:
        """
        Verifica si el grupo puede ser asignado basado en idioma, fechas y clientes.

        :param idiomaVerificable: Idioma a verificar.
        :param fechasVerificables: Fechas a verificar.
        :param clientesVerificables: Clientes a verificar.
        :return: True si el grupo puede ser asignado, False de lo contrario.
        """
        if self.idioma != idiomaVerificable or not any(cliente in clientesVerificables for cliente in self.clientes):
            hayCapacidad = True
            for reserva in self.listaReservas:
                clientesExtras = copy.deepcopy(clientesVerificables)
                for clienteVerificable in clientesVerificables:
                    if clienteVerificable in reserva:
                        clientesExtras.remove(clienteVerificable)
                if len(clientesExtras) > self.capacidad:
                    hayCapacidad = False
            if not self.guia.getIdiomas().contains(idiomaVerificable) or not hayCapacidad:
                gruposSustitutos = Grupo.buscarGrupo(self.fecha, self.actividad, idiomaVerificable)
                if not gruposSustitutos:
                    return False
        if self.fecha not in fechasVerificables:
            return False
        return True

    def reubicarReservas(self, listaReservas: List[List[Cliente]]) -> List[List[Cliente]]:
        """
        Reubica reservas en el grupo si hay capacidad suficiente.

        :param listaReservas: Lista de reservas a reubicar.
        :return: Lista de reservas que no se pudieron reubicar.
        """
        listaFinal = copy.deepcopy(listaReservas)
        for lista in listaReservas:
            if len(lista) <= self.capacidad:
                self.listaReservas.append(lista)
                self.asignarCapacidad()
                self.modificarCapacidad()
                listaFinal.remove(lista)
        return listaFinal

    def asignarCapacidad(self):
        """
        Asigna la capacidad del grupo según la actividad.
        """
        if self.actividad:
            self.capacidad = self.actividad.getCapacidad()

    def modificarCapacidad(self):
        """
        Modifica la capacidad restante del grupo según las reservas actuales.
        """
        personasPresentes = sum(len(reserva) for reserva in self.listaReservas)
        self.capacidad -= personasPresentes

    @staticmethod
    def buscarGrupo(fecha: List[int], actividad: Actividad, idioma: Optional[Idiomas] = None, personasAAgregar: Optional[List[Cliente]] = None, cantidadPersonas: Optional[int] = None) -> List['Grupo']:
        """
        Busca grupos disponibles según la fecha, actividad, idioma y capacidad.

        :param fecha: Fecha del grupo.
        :param actividad: Actividad del grupo.
        :param idioma: Idioma del grupo (opcional).
        :param personasAAgregar: Lista de personas a agregar (opcional).
        :param cantidadPersonas: Cantidad de personas a verificar (opcional).
        :return: Lista de grupos que cumplen con los criterios.
        """
        gruposEncontrados = [grupo for grupo in Grupo.grupos if grupo.fecha == fecha and grupo.actividad == actividad]
        if idioma:
            gruposEncontrados = [grupo for grupo in gruposEncontrados if grupo.idioma == idioma]
        if personasAAgregar is not None:
            gruposEncontrados = [grupo for grupo in gruposEncontrados if grupo.capacidad >= len(personasAAgregar)]
        if cantidadPersonas is not None:
            gruposEncontrados = [grupo for grupo in gruposEncontrados if grupo.capacidad >= cantidadPersonas]
        return gruposEncontrados

    @staticmethod
    def buscarGrupo(fecha: List[int], guia: Guia) -> Optional['Grupo']:
        """
        Busca un grupo por fecha y guía.

        :param fecha: Fecha del grupo.
        :param guia: Guia del grupo.
        :return: El grupo encontrado o None si no se encuentra.
        """
        for grupo in Grupo.grupos:
            if grupo.fecha == fecha and grupo.guia == guia:
                return grupo
        return None

    def elegirGuia(self) -> Optional[Guia]:
        """
        Elige un guía de reemplazo basado en disponibilidad y costo.

        :return: El guía elegido o None si no se encuentra ninguno.
        """
        guiasCapacitados = self.actividad.buscarGuia(self.idioma)
        guiasDisponibles = Guia.buscarDisponibilidad(guiasCapacitados, self.fecha)
        tipoActividad = self.actividad.getTipo()
        guiasFinal = []
        mayorConcidencia = 0

        for guia in guiasDisponibles:
            concidencia = sum(tipo in guia.getTipoActividades() for tipo in tipoActividad)
            if concidencia == mayorConcidencia:
                guiasFinal.append(guia)
            elif concidencia > mayorConcidencia:
                mayorConcidencia = concidencia
                guiasFinal = [guia]

        if len(guiasFinal) == 1:
            return guiasFinal[0]
        return Guia.elegirGuiaPorCosto(guiasFinal)

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del grupo.

        :return: Cadena con la información del grupo.
        """
        idioma = self.idioma.name if self.idioma else "No especificado"
        actividad = self.actividad.getNombre() if self.actividad else "No especificada"
        return (f"Fecha: {self.fecha}, Guía: {self.guia}, Actividad: {actividad}, "
                f"Idioma: {idioma}, Capacidad: {self.capacidad}, Tipo de mesa: {self.tipoMesa}, "
                f"Tipo de habitación: {self.tipoHabitacion}, Clasificación: {self.clasificacion}, "
                f"Clientes: {', '.join(str(cliente) for reserva in self.listaReservas for cliente in reserva)}")
