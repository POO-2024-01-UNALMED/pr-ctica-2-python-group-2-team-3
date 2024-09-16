
class Grupo:
    _grupos = []

    def __init__(self, fecha=None, guia=None, actividad=None, idioma=None, lista_reservas=None, capacidad=None, tipo_habitacion=None, tipo_mesa=None, lista_reserva_extra=None):
        self._fecha = fecha
        self._guia = guia
        self._actividad = actividad
        self._idioma = idioma
        self._lista_reservas = lista_reservas or []
        self._capacidad = capacidad
        self._tipo_habitacion = tipo_habitacion
        self._tipo_mesa = tipo_mesa
        self._clasificacion = None
        self._fecha_ocupadas = []
        self._clientes = []

        # Caso 1: Si se pasa solo la guía
        if guia and not actividad and not capacidad and not tipo_habitacion and not tipo_mesa:
            Grupo._grupos.append(self)
            return
        
        # Caso 2: Si se pasa fecha, guía, actividad, idioma, y lista_reservas
        if fecha and guia and actividad and idioma and lista_reservas:
            self._clasificacion = self._actividad.getClasificacion()
            self.asignar_capacidad()
            self.modificar_capacidad()
            Grupo._grupos.append(self)
            return
        
        # Caso 3: Si se pasa actividad, lista_reserva_extra, fecha, idioma
        if actividad and lista_reserva_extra and fecha and idioma:
            self._lista_reservas = [lista_reserva_extra]
            self.asignar_capacidad()
            self.modificar_capacidad()
            self._guia = self.elegir_guia()
            Grupo._grupos.append(self)
            return
        
        # Caso 4: Si se pasa tipo_habitacion y capacidad (Actividad: "Hospedaje")
        if tipo_habitacion and capacidad:
            from gestorAplicacion.actividad import Actividad
            from gestorAplicacion.tipoActividad import TipoActividad
            
            self._actividad = Actividad("Hospedaje", TipoActividad.HOSPEDAJE)
            self._clientes = []
            Grupo._grupos.append(self)
            return

        # Caso 5: Si se pasa capacidad y tipo_mesa (Actividad: "Restaurante")
        if capacidad and tipo_mesa:
            self._actividad = Actividad("Restaurante", TipoActividad.RESTAURANTE)
            self._clientes = []
            Grupo._grupos.append(self)
            return
        
        # Caso general: Si se pasa cualquier combinación válida de parámetros
        if actividad:
            self._clasificacion = self._actividad.getClasificacion() if actividad else None
        Grupo._grupos.append(self)


    @staticmethod
    def retirar_guia(guia, fecha):
        from gestorAplicacion.reserva import Reserva
        grupo = None
        for g in Grupo._grupos:
            if g._guia == guia and g._fecha == fecha:
                grupo = g
                break
        if grupo==None:
            return
        reemplazo = grupo.elegir_guia() if grupo else None
        if reemplazo is None:
            grupos_sustitutos = Grupo.buscar_grupo(grupo._fecha, grupo._actividad, grupo._idioma)
            lista_reservas_pendientes = grupo._lista_reservas
            
            for g in grupos_sustitutos:
                reservas_pendientes = g.reubicar_reservas(lista_reservas_pendientes)
                if not reservas_pendientes:
                    break
                lista_reservas_pendientes = reservas_pendientes

            if lista_reservas_pendientes:
                for reserva in lista_reservas_pendientes:
                    reserva_faltante = Reserva.buscar_reserva(grupo, reserva)
                    reserva_faltante.cancelar_actividad(grupo._actividad)
            Grupo._grupos.remove(grupo)
        else:
            grupo._guia = reemplazo
            reemplazo.getDiasOcupados().append(fecha)
            reemplazo.setDiasOcupados(reemplazo.getDiasOcupados())

    def retirar_clientes(self, reserva):
        self._lista_reservas.remove(reserva)
        grupos_sustitutos = Grupo.buscar_grupo(self._fecha, self._actividad, self._idioma)
        lista_reservas_pendientes = self._lista_reservas
        
        for g in grupos_sustitutos:
            reservas_pendientes = g.reubicar_reservas(lista_reservas_pendientes)
            if not reservas_pendientes:
                break
            lista_reservas_pendientes = reservas_pendientes
        
        if not lista_reservas_pendientes:
            self._guia.getDiasOcupados().remove(self._fecha)
            Grupo._grupos.remove(self)
            return True
        return False

    def verificar_parametros_grupo(self, idioma_verificable, fechas_verificables, clientes_verificables):
        if self._idioma != idioma_verificable or not set(clientes_verificables).issubset(self._clientes):
            hay_capacidad = all(len(reserva) + len(clientes_verificables) <= self._capacidad for reserva in self._lista_reservas)
            if not (self._guia.getIdiomas() and hay_capacidad):
                if not Grupo.buscar_grupo(self._fecha, self._actividad, idioma_verificable, clientes_verificables):
                    return False
        return self._fecha in fechas_verificables

    def reubicar_reservas(self, lista_reservas):
        lista_final = lista_reservas.copy()
        for reserva in lista_reservas:
            if len(reserva) <= self._capacidad:
                self._lista_reservas.append(reserva)
                self.asignar_capacidad()
                self.modificar_capacidad()
                lista_final.remove(reserva)
        return lista_final

    def asignar_capacidad(self):
        self._capacidad = self._actividad.getCapacidad()

    def modificar_capacidad(self):
        personas_presentes = sum(len(lista) for lista in self._lista_reservas)
        self._capacidad -= personas_presentes

    @staticmethod
    def buscar_grupo(fecha, actividad, idioma=None, personas_a_agregar=None):
        grupos_encontrados = []
        for grupo in Grupo._grupos:
            if grupo._fecha == fecha and grupo._actividad == actividad:
                if idioma is None or grupo._idioma == idioma:
                    if personas_a_agregar is None or grupo._capacidad >= len(personas_a_agregar):
                        grupos_encontrados.append(grupo)
        return grupos_encontrados

    @staticmethod
    def buscar_grupo_por_guia(fecha, guia):
        for grupo in Grupo._grupos:
            if grupo._fecha == fecha and grupo._guia == guia:
                return grupo
        return None

    def elegir_guia(self):
        from gestorAplicacion.guia import Guia
        guias_capacitados = self._actividad.buscar_guia(self._idioma)
        guias_disponibles = Guia.buscar_disponibilidad(guias_capacitados, self._fecha)
        tipo_actividad = self._actividad.getTipo()
        guias_final = []
        mayor_concidencia = 0

        for guia in guias_disponibles:
            concidencia = sum(1 for tipo in guia.getTipoActividades() if tipo in tipo_actividad)
            if concidencia == mayor_concidencia:
                guias_final.append(guia)
            elif concidencia > mayor_concidencia:
                mayor_concidencia = concidencia
                guias_final = [guia]

        if len(guias_final) == 1:
            return guias_final[0]
        elif guias_final:
            guia_elegido = min(guias_final, key=lambda g: g.getPrecio())
            return guia_elegido
        return None

    @staticmethod
    def retirar_actividad(actividad, fecha=None):
        from gestorAplicacion.reserva import Reserva
        for grupo in Grupo._grupos:
            if grupo._actividad == actividad and (not fecha or grupo._fecha in fecha):
                for reserva in grupo._lista_reservas:
                    reserva_faltante = Reserva.buscar_reserva(grupo, reserva)
                    reserva_faltante.cancelar_actividad(grupo._actividad)
                grupo._guia.getDiasOcupados().remove(grupo._fecha)
                Grupo._grupos.remove(grupo)

    @staticmethod
    def buscar_idioma_mas_usado(lista_idiomas):
        from gestorAplicacion.idioma import Idioma
        idioma_frecuencia = {idioma: lista_idiomas.count(idioma) for idioma in Idioma}
        max_frecuencia = max(idioma_frecuencia.values())
        idioma_mas_usado = [f"{idioma}={max_frecuencia}/{len(lista_idiomas)}" for idioma, freq in idioma_frecuencia.items() if freq == max_frecuencia]
        return idioma_mas_usado

    @staticmethod
    def cantidad_clientes_idioma(lista_fechas, idioma):
        cantidad = 0
        for grupo in Grupo._grupos:
            if grupo._idioma == idioma and grupo._fecha in lista_fechas:
                cantidad += sum(len(reserva) for reserva in grupo._lista_reservas)
        return cantidad

    @staticmethod
    def cantidad_clientes_destino(destino, fecha=None):
        cantidad_clientes = 0
        for grupo in Grupo._grupos:
            if grupo._actividad.getDestino() == destino and (not fecha or grupo._fecha[1] == fecha[1]):
                cantidad_clientes += sum(len(reserva) for reserva in grupo._lista_reservas)
        return cantidad_clientes

    def añadir_fecha_ocupada(self, fecha):
        self._fecha_ocupadas.append(fecha)

    # Métodos de acceso
    @staticmethod
    def get_grupos():
        return Grupo._grupos

    @staticmethod
    def set_grupos(grupos):
        Grupo._grupos = grupos

    def get_fecha(self):
        return self._fecha

    def set_fecha(self, fecha):
        self._fecha = fecha

    def get_guia(self):
        return self._guia

    def set_guia(self, guia):
        self._guia = guia

    def get_actividad(self):
        return self._actividad

    def set_actividad(self, actividad):
        self._actividad = actividad

    def get_idioma(self):
        return self._idioma

    def set_idioma(self, idioma):
        self._idioma = idioma

    def get_lista_reservas(self):
        return self._lista_reservas

    def set_lista_reservas(self, lista_reservas):
        self._lista_reservas = lista_reservas

    def get_capacidad(self):
        return self._capacidad

    def set_capacidad(self, capacidad):
        self._capacidad = capacidad

    def get_tipo_habitacion(self):
        return self._tipo_habitacion

    def set_tipo_habitacion(self, tipo_habitacion):
        self._tipo_habitacion = tipo_habitacion

    def get_tipo_mesa(self):
        return self._tipo_mesa

    def set_tipo_mesa(self, tipo_mesa):
        self._tipo_mesa = tipo_mesa

    def get_fecha_ocupadas(self):
        return self._fecha_ocupadas

    def set_fecha_ocupadas(self, fecha_ocupadas):
        self._fecha_ocupadas = fecha_ocupadas

    def get_clasificacion(self):
        return self._clasificacion

    def set_clasificacion(self, clasificacion):
        self._clasificacion = clasificacion

    def get_clientes(self):
        return self._clientes

    def set_clientes(self, clientes):
        self._clientes = clientes
