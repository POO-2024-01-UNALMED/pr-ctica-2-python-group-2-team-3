
class Plan:
    _paquetes = []

    def __init__(self, tipo=None, destino=None, actividades=None, clasificacion=0, reserva=None, cantidad_dias=0):
        self._tipo = tipo
        self._destino = destino
        self._actividades = actividades if actividades else []
        self._clasificacion = clasificacion
        self._reserva = reserva
        self._grupos = []
        self._cantidad_dias = cantidad_dias
        self._precio = 0.0

        if reserva:
            self._reserva.setPlan(self)
            self._tipo = reserva.getTipoPlan()

        if cantidad_dias > 0:
            Plan._paquetes.append(self)

    def mostrarPlaneacionPlan(self, opc_busqueda, clasificacion, tipo, fecha, idioma):
        from gestorAplicacion.actividad import Actividad
        tabla = []
        posicion1, posicion2, posicion3, posicion4, posicion5 = [], [], [], [], []

        actividades_filtradas = [actividad for actividad in self._actividades if actividad.verificarFiltrosActividad(clasificacion, tipo, fecha, idioma)]

        if opc_busqueda == "1":
            posicion1.append(str(self._cantidad_dias))
            posicion2.append(str(len(self._actividades)))
            posicion3.extend(Actividad.mostrarNombres(actividades_filtradas))
            posicion4.append(Actividad.mostrarClasificacion(self._clasificacion))
            posicion5.append(f"{self._precio}$")
        else:
            posicion1.append(str(self._cantidad_dias))
            posicion2.append(Actividad.mostrarClasificacion(self._clasificacion))
            posicion3.append(str(len(self._actividades)))
            tipo_predominante = self.mostrarTipoPredominante()
            posicion4.append(tipo_predominante.getNombre())
            posicion5.append(tipo_predominante.getDificultad())

        tabla.append(self._destino)  # 0: tipo de plan
        tabla.append(posicion1)  # 1: actividades familiares o disponibilidad de actividades
        tabla.append(posicion2)  # 2: actividades ecológicas o promedio de precios
        tabla.append(posicion3)  # 3: cantidad de personas o actividades ecológicas
        tabla.append(posicion4)  # 4: cantidad de guías o actividades extremas
        tabla.append(posicion5)  # 5: clasificación más solicitada o actividades acuáticas

        return tabla

    @staticmethod
    def mostrarPaquetesDestino(destino):
        return [paquete for paquete in Plan._paquetes if paquete._destino == destino]

    def añadirActividad(self, actividad):
        self._actividades.append(actividad)

    @staticmethod
    def mostrarNombreActividad(actividades):
        return [actividad.getNombre() for actividad in actividades]

    def mostrarTipoPredominante(self):
        from gestorAplicacion.tipoActividad import TipoActividad
        tipo_predominante, cantidad_mayor = None, 0
        for tipo in TipoActividad.values():
            cantidad = sum(1 for actividad in self._actividades if tipo in actividad.getTipo())
            if cantidad > cantidad_mayor:
                cantidad_mayor = cantidad
                tipo_predominante = tipo
        return tipo_predominante


    # Muestra los nombres de las actividades existentes en el plan
    def mostrarNombreActividad(self):
        nombres = [actividad.getNombre() for actividad in self._actividades]
        return nombres

    # Selecciona las actividades iniciales del plan antes de ingresar la fecha
    def escogerActividadesIniciales(self, actividades_disponibles, seleccionadas):
        seleccion_inicial = []
        for nombre in seleccionadas:
            for actividad in actividades_disponibles:
                if actividad.getNombre() == nombre:
                    seleccion_inicial.append(actividad)
        return seleccion_inicial

    # Muestra las actividades disponibles para el día
    def actividadesDisponiblesDia(self, fecha, seleccion_inicial):
        from gestorAplicacion.grupo import Grupo
        from gestorAplicacion.guia import Guia
        actividades_disponibles = []
        for actividad in seleccion_inicial:
            existen_grupos = Grupo.buscarGrupo(fecha, actividad, self._reserva.getIdiomas()[0], self._reserva.getClientes())
            if len(existen_grupos) > 0:
                actividades_disponibles.append(actividad)
            else:
                guias_capacitados = actividad.buscarGuia(self._reserva.getIdiomas()[0])
                guias_disponibles = Guia.buscarDisponibilidad(guias_capacitados, fecha)
                if len(guias_disponibles) > 0:
                    actividades_disponibles.append(actividad)
        return actividades_disponibles

    # Escoge las actividades del día
    def escogerActividadesDia(self, actividades_posibles, actividad_escogida, fecha):
        from gestorAplicacion.grupo import Grupo
        for nombre in actividad_escogida:
            for actividad in actividades_posibles:
                if actividad.getNombre() == nombre:
                    self._actividades.append(actividad)
                    existen_grupos = Grupo.buscarGrupo(fecha, actividad, self._reserva.getIdiomas()[0], self._reserva.getClientes())
                    if len(existen_grupos) > 0:
                        existen_grupos[0].getListaReservas().append(self._reserva.getClientes())
                        self._grupos.append(existen_grupos[0])
                    else:
                        grupo = Grupo(actividad, self._reserva.getClientes(), fecha, self._reserva.getIdiomas()[0])
                        self._grupos.append(grupo)
        self.asignarPrecio()

    # Escoge las actividades del día para un paquete
    def escogerActividadesDiaPaquete(self, actividades_posibles, actividad_escogida, fecha):
        from gestorAplicacion.grupo import Grupo
        for nombre in actividad_escogida:
            for actividad in actividades_posibles:
                if actividad.getNombre() == nombre:
                    grupo = Grupo(actividad, self._reserva.getClientes(), fecha, self._reserva.getIdiomas()[0])
                    self._grupos.append(grupo)
        self.asignarPrecio()

    # Muestra los paquetes turísticos disponibles que cumplan con los parámetros
    @staticmethod
    def paquetesDisponibles(cantidad_personas, destino, clasificacion, fechas):
        from gestorAplicacion.grupo import Grupo
        paquetes_posibles = []
        for plan in Plan._paquetes:
            fechas_disponibles = []
            for fecha in fechas:
                if plan._destino == destino and plan._clasificacion <= clasificacion and len(plan._actividades) >= len(fechas):
                    for actividad in plan._actividades:
                        existen_grupos = Grupo.buscarGrupo(fecha, actividad, plan._reserva.getIdiomas()[0], cantidad_personas)
                        if len(existen_grupos) > 0:
                            fechas_disponibles.append(fecha)
            if len(fechas_disponibles) == len(fechas):
                paquetes_posibles.append(plan)
        return paquetes_posibles

    # Retorna el tipo del plan
    @staticmethod
    def asignarTipo(valor):
        if valor == 1:
            return "PP"
        elif valor == 2:
            return "PT"
        return ""

    # Asigna el precio del plan
    def asignarPrecio(self):
        self._precio = sum(actividad.getPrecio() for actividad in self._actividades)

    # Muestra cómo imprimir los paquetes turísticos
    @staticmethod
    def stringPaqueteTuristico(plan):
        return [
            ("Destino", str(plan._destino.getNombre())),
            ("Actividades", ", ".join([str(actividad.getNombre()) for actividad in plan._actividades])),
            ("Precio por persona", str(plan._precio))]


    # Métodos de acceso
    @staticmethod
    def getPaquetes():
        return Plan._paquetes

    @staticmethod
    def setPaquetes(paquetes):
        Plan._paquetes = paquetes

    def getTipo(self):
        return self._tipo

    def setTipo(self, tipo):
        self._tipo = tipo

    def getDestino(self):
        return self._destino

    def setDestino(self, destino):
        self._destino = destino

    def getActividades(self):
        return self._actividades

    def setActividades(self, actividades):
        self._actividades = actividades

    def getPrecio(self):
        return self._precio

    def setPrecio(self, precio):
        self._precio = precio

    def getClasificacion(self):
        return self._clasificacion

    def setClasificacion(self, clasificacion):
        self._clasificacion = clasificacion

    def getGrupos(self):
        return self._grupos

    def setGrupos(self, grupos):
        self._grupos = grupos

    def getReserva(self):
        return self._reserva

    def setReserva(self, reserva):
        self._reserva = reserva
