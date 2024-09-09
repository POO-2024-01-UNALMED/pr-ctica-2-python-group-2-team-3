from gestorAplicacion.enums import idiomas, tiposActividad
from gestorAplicacion.interfaces import registrable
from gestorAplicacion.manejoReserva import actividad, destino, grupo, reserva
from gestorAplicacion.gestionHum import persona

from multimethod import multimethod
import copy

class Guia(persona, registrable):
    """
    La clase Guia representa a un guía turístico.
    Extiende de la clase Persona y contiene información sobre el nombre,
    idiomas, tipos de actividades que puede realizar, destino asignado,
    precio, y días ocupados y no disponibles.
    """

    guias = []

    def __init__(self, nombre=None, edad=18):
        super().__init__(nombre,None, edad)
        self.tipoActividades = []
        self.diasOcupados = []
        self.diasNoDisponibles = []
        self.precio = 0.0
        Guia.guias.append(self)

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto Guia.

        :return: Una cadena que representa al guía.
        """
        return f"Nombre del guia: {self.nombre},\nIdiomas que domina: {self.idiomas()},\nTipo de actividades: {self.tipoActividades},\nDestino asignado: {self.destino.nombre()}"

    def ingresarIdiomas(self, idiomas):
        """
        Ingresa los idiomas que el guía domina.

        :param idiomas: Una cadena que representa los idiomas.
        """
        listaString = idiomas.split(" ")
        for numero in listaString:
            indice = int(numero)
            self.idiomas.append(idiomas.values()[indice - 1])

    def ingresarTipoActividades(self, tipoActividades):
        """
        Ingresa los tipos de actividades que puede realizar el guía a partir de una cadena.

        :param tipoActividades: Una cadena que representa los tipos de actividades.
        """
        listaString = tipoActividades.split(" ")
        for numero in listaString:
            indice = int(numero)
            self.tipoActividades.append(tiposActividad.values()[indice - 1])

    def asignarParametros(self):
        """
        Asigna un precio al guía basado en los idiomas que domina y el destino asignado.
        """
        precioBase = 30000
        precioExtra = 0
        porcentajeExtra = self.destino().precioExtraPorDestino()
        for idioma in self.idiomas():
            precioExtra += idioma.precio()

        precioFinal = (precioBase * porcentajeExtra) + precioExtra
        self.precio = precioFinal

    def ingresarGuia(self):
        """
        Ingresa el guía a las actividades que puede realizar en su destino.
        """
        listaActividades = self.destino().mostrarActividadesTipo(self)
        for actividad in listaActividades:
            if self not in actividad.guias():
                actividad.guias().append(self)

    @staticmethod
    def buscarGuia(nombre):
        """
        Busca un guía por su nombre.

        :param nombre: El nombre del guía a buscar.
        :return: El guía encontrado o None si no se encuentra.
        """
        for guia in Guia.guias:
            if nombre == guia.nombre():
                return guia
        return None

    @staticmethod
    def buscarDisponibilidad(guiasCapacitados, fecha):
        """
        Busca guías disponibles en una fecha específica entre los guías capacitados.

        :param guiasCapacitados: Una lista de guías capacitados.
        :param fecha: La fecha a verificar.
        :return: Una lista de guías disponibles.
        """
        guiasDisponibles = []
        for guia in guiasCapacitados:
            if fecha not in guia.diasOcupados:
                guiasDisponibles.append(guia)
        return guiasDisponibles

    @staticmethod
    def retirarGuia(retirado, listaFechas=None):
        """
        Retira un guía en una fecha específica y actualiza sus días ocupados y no disponibles.

        :param retirado: El guía a retirar.
        :param listaFechas: Una lista de fechas a actualizar.
        """
        for dia in copy.deepcopy(retirado.diasOcupados):
            if dia not in retirado.diasNoDisponibles and (listaFechas is None or dia in listaFechas):
                grupo.retirarGuia(retirado, dia)

        if listaFechas:
            for dia in listaFechas:
                if dia not in retirado.diasOcupados:
                    retirado.diasOcupados.append(dia)
                if dia not in retirado.diasNoDisponibles:
                    retirado.diasNoDisponibles.append(dia)

    @staticmethod
    def retirarGuia(despedido):
        """
        Retira un guía despedido.

        :param despedido: El guía a despedir.
        """
        Guia.retirarGuia(despedido, None)
        actividad.retirarGuia(despedido)
        Guia.guias.remove(despedido)

    @staticmethod
    def mostrarDisponibilidadGuias(fecha, destino=None, idioma=None):
        """
        Muestra la tabla de disponibilidad de los guías en una fecha específica.

        :param fecha: La fecha a verificar.
        :param destino: El destino a verificar (puede ser None).
        :param idioma: El idioma a verificar (puede ser None).
        :return: Una lista de objetos con la disponibilidad de los guías.
        """
        tabla = []

        guiasOcupados = 0
        guiasDisponibles = 0
        destinos = []
        idiomas = []
        actividades = []
        contadorActividades = 0
        contadorClientes = 0
        contadorGuiasIdioma = 0

        for guia in Guia.guias:
            grupoGuia = Grupo.buscarGrupo(fecha, guia)
            isDestinoMatch = (destino is None) or guia.getDestino() == destino
            isIdiomaMatch = (idioma is None) or grupoGuia.getIdioma() == idioma

            if isDestinoMatch and fecha in guia.diasOcupados and isIdiomaMatch:
                guiasOcupados += 1

                destinos.append(guia.getDestino())
                idiomas.append(grupoGuia.getIdioma())
                for reserva in grupoGuia.getListaReservas():
                    contadorClientes += len(reserva)

                if grupoGuia.getActividad() not in actividades:
                    actividades.append(grupoGuia.getActividad())
                    contadorActividades += 1
            else:
                guiasDisponibles += 1

            if idioma and idioma in guia.getIdiomas():
                contadorGuiasIdioma += 1

        actividad = f"{contadorActividades}/{len(actividades)}"
        destinoComun = destino.buscarDestinoComun(destinos)
        listIdioma = grupo.buscarIdiomaMasUsado(idiomas)

        tabla.append(fecha[2])  # año
        tabla.append(reserva.mostrarMes(fecha[1]))  # mes
        tabla.append(fecha[0])  # día
        tabla.append(guiasDisponibles)  # guías disponibles
        tabla.append(guiasOcupados)  # guías ocupados
        tabla.append(actividad)  # contador actividades

        if destino is None:
            tabla.append(destino)
        else:
            tabla.append(destinoComun)  # destino común

        if idioma is None:
            tabla.append(idioma)
        else:
            tabla.append(listIdioma)  # idioma más usado

        tabla.append(contadorClientes)  # contador clientes
        tabla.append(contadorGuiasIdioma)  # contador guías por idioma

        return tabla

    def mostrarIntinerario(self, fecha):
        """
        Muestra la tabla del itinerario del guía en una fecha específica.

        :param fecha: La fecha a verificar.
        :return: Una lista de objetos con el itinerario del guía.
        """
        tabla = []

        estado = "Disponible"
        tipo = []
        grupo = None
        cantidadPersonas = 0

        if fecha in self.diasOcupados:
            estado = "Ocupado"
            grupo = Grupo.buscarGrupo(fecha, self)
        elif fecha in self.diasNoDisponibles:
            estado = "No disponible"

        if grupo:
            for reserva in grupo.getListaReservas():
                cantidadPersonas += len(reserva)

            for x in grupo.getActividad().getTipo():
                tipo.append(x.getNombre() + ",")

        tabla.append(fecha[2])  # año
        tabla.append(reserva.mostrarMes(fecha[1]))  # mes
        tabla.append(fecha[0])  # día
        tabla.append(self.getNombre())  # nombre
        tabla.append(self.getDestino())  # destino
        tabla.append(estado)  # estado
        tabla.append(grupo.getActividad().getNombre() if grupo else None)  # actividad
        tabla.append(tipo)  # tipo actividad
        tabla.append(grupo.getIdioma() if grupo else None)  # idioma
        tabla.append(cantidadPersonas)  # cantidad de personas
        tabla.append(grupo.getClasificacion() if grupo else None)  # clasificación

        return tabla

    def asignarGuia(self, grupo):
        """
        Asigna un guía a un grupo.

        :param grupo: El grupo al cual se asignará el guía.
        """
        for guia in Guia.guias:
            if self == guia:
                grupo.setGuia(guia)
                break

# ///////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////// Métodos de acceso //////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////

