
class Destino:
    _destinos = []

    def __init__(self, nombre):
        self._nombre = nombre
        self._guias = []
        self._actividades = []
        Destino._destinos.append(self)

    @staticmethod
    def elegirDestinoGuia(guia):
        mayor_cantidad = 0
        lista_destinos = []
        
        for destino in Destino._destinos:
            lista_actividades = destino.mostrarActividadesTipo(guia.getTipoActividades())
            if len(lista_actividades) == mayor_cantidad:
                lista_destinos.append(destino)
            elif len(lista_actividades) > mayor_cantidad:
                mayor_cantidad = len(lista_actividades)
                lista_destinos.clear()
                lista_destinos.append(destino)

        if len(lista_destinos) > 1:
            menor_cantidad = len(lista_destinos[0]._guias)
            lista_final = []
            for destino in lista_destinos:
                if len(destino._guias) == menor_cantidad:
                    lista_final.append(destino)
                elif len(destino._guias) < menor_cantidad:
                    menor_cantidad = len(destino._guias)
                    lista_final.clear()
                    lista_final.append(destino)
            lista_destinos = lista_final

        if lista_destinos is [] or not lista_destinos :
                lista_destinos=Destino.seleccionarDestinos()
        else:
            lista_destinos=', '.join(str(destino.getNombre()) for destino in lista_destinos)
        
        return lista_destinos

    @staticmethod
    def seleccionarDestinos():
        import random
        destinos= ["Cartagena", "Bogotá", "Medellín", "Santa Marta", "San Andrés", 
        "Cali","Parque Nacional Natural Tayrona","Eje Cafetero", "Salento", "Guatapé"]

        cantidad_destinos = random.randint(1, len(destinos))
        destinos_random = random.sample(destinos, cantidad_destinos)
        return destinos_random

    def actividadesDisponiblesDestino(self, clasificacion, cantidad_personas):
        actividades_posibles = []
        for actividad in self._actividades:
            if actividad.getClasificacion() <= clasificacion and actividad.getCapacidad() >= cantidad_personas:
                actividades_posibles.append(actividad)
        return actividades_posibles

    def mostrarActividadesTipo(self, guia):
        lista_actividades = []
        tipos_guia = guia.getTipoActividades()
        for tipo_guia in tipos_guia:
            for actividad in self._actividades:
                if tipo_guia in actividad.getTipo() and actividad not in lista_actividades:
                    lista_actividades.append(actividad)
        return lista_actividades

    def mostrarActividadesTipoLista(self, lista):
        lista_actividades = []
        for tipo_guia in lista:
            for actividad in self._actividades:
                if tipo_guia in actividad.getTipo() and actividad not in lista_actividades:
                    lista_actividades.append(actividad)
        return lista_actividades

    @staticmethod
    def ingresarGuia(guia, destino):
        if isinstance(destino,Destino):
            destino._guias.append(guia)
            guia.setDestino(destino)
            guia.setDestinoNombre(destino.getNombre)
        else:
            guia.setDestinoNombre(destino)

    @staticmethod
    def buscarDestinoComun(lista_destinos):
        cantidad_maxima = 0
        destino_final = []

        for destino in Destino._destinos:
            contador = sum(1 for x in lista_destinos if x == destino)

            if contador == cantidad_maxima:
                destino_final.append(destino)
            elif contador > cantidad_maxima:
                destino_final.clear()
                destino_final.append(destino)
                cantidad_maxima = contador

        lista_destino = [f"{destino}={cantidad_maxima}/{len(lista_destinos)}" for destino in destino_final]
        return lista_destino

    def precioExtraPorTemporada(self, fecha):
        from gestorAplicacion.grupo import Grupo
        mes = fecha[1]
        porcentaje_precio_extra = {
            12: 1.4, 1: 1.4, 6: 1.4, 7: 1.4,
            2: 0.8, 3: 0.8, 11: 0.8
        }.get(mes, 1.0)

        cantidad_clientes = Grupo.cantidadClientesDestino(self, fecha)
        if cantidad_clientes > len(self._guias) * 10:
            porcentaje_precio_extra += 0.3
        elif cantidad_clientes < len(self._guias) * 4:
            porcentaje_precio_extra -= 0.3

        return porcentaje_precio_extra

    def precioExtraPorDestino(self):
        from gestorAplicacion.grupo import Grupo
        porcentaje_extra = 1
        destinos_con_mas_actividades = destinos_con_menos_actividades = 0
        destinos_con_mas_clientes = destinos_con_menos_clientes = 0
        
        for destino in Destino._destinos:
            if len(destino.getActividades()) > len(self._actividades):
                destinos_con_mas_actividades += 1
            else:
                destinos_con_menos_actividades += 1

            if Grupo.cantidadClientesDestino(destino, None) > Grupo.cantidadClientesDestino(self, None):
                destinos_con_mas_clientes += 1
            else:
                destinos_con_menos_clientes += 1

        if ((destinos_con_mas_actividades + destinos_con_menos_actividades) / 4) > destinos_con_mas_actividades:
            porcentaje_extra += 0.5
        elif ((destinos_con_mas_actividades + destinos_con_menos_actividades) / 2) > destinos_con_mas_actividades:
            porcentaje_extra += 0.3
        elif ((destinos_con_mas_actividades + destinos_con_menos_actividades) / 4) > destinos_con_menos_actividades:
            porcentaje_extra -= 0.3

        if ((destinos_con_mas_clientes + destinos_con_menos_clientes) / 4) > destinos_con_mas_clientes:
            porcentaje_extra += 0.5
        elif ((destinos_con_mas_clientes + destinos_con_menos_clientes) / 4) > destinos_con_menos_clientes:
            porcentaje_extra -= 0.3

        return porcentaje_extra

    @staticmethod
    def listaNombres():
        nombres=["Cartagena", "Bogotá", "Medellín", "Santa Marta", "San Andrés", 
                    "Cali", "Parque Nacional Natural Tayrona", "Eje Cafetero", "Salento", "Guatapé"]
        lista=(destino.getNombre() for destino in Destino._destinos)if Destino._destinos is not ([] or None) else nombres
        return nombres

    @staticmethod
    def buscarNombre(nombre):
        for destino in Destino._destinos:
            if destino.getNombre() == nombre:
                return destino
        return None

    def mostrarPlaneacionFecha(self, opc_busqueda, clasificacion, tipo, fechas, idioma):
        from gestorAplicacion.reserva import Reserva
        from gestorAplicacion.hotel import Hotel
        from gestorAplicacion.actividad import Actividad
        tabla = []
        posicion = fechas[0][0] if opc_busqueda == "3" else Reserva.mostrarMes(fechas[0][1])

        posicion0 = [posicion]
        posicion1 = []
        posicion2 = []
        posicion3 = []
        posicion4 = []
        posicion5 = []

        actividades_filtradas = [actividad for actividad in self._actividades if actividad.verificarFiltrosActividad(clasificacion, tipo, fechas, idioma)]
        hoteles_filtrados = [Hotel.mostrarHotelesFiltrados(self, fecha) for fecha in fechas]

        if opc_busqueda == "1":
            posicion1.append(str(len(actividades_filtradas)))
            posicion2.append(str(len(hoteles_filtrados)))
            posicion3.append(self.buscarIdiomaComun().getNombre())
            posicion4.append(str(Reserva.mostrarCantidadPersonasDestino(self, fechas)))
            posicion5.append(self.definirOferta(actividades_filtradas))
        elif opc_busqueda == "2":
            posicion1.append(Reserva.actividadPrincipalDestino(self).getTipo()[0].getNombre())
            posicion2.append(str(Actividad.cantidadGuiasDisponiblesLista(actividades_filtradas)))
            posicion3.append(str((Hotel.promedioPreciosHoteles(hoteles_filtrados) + Actividad.promedioPreciosActividades(actividades_filtradas)) / 2))
            posicion4.append(str(len(actividades_filtradas)))
            posicion5.append(self.definirOferta(actividades_filtradas))
        else:
            posicion1.append(str(len(actividades_filtradas)))
            posicion2.append(str(Actividad.promedioPreciosActividades(actividades_filtradas)))
            posicion3.append(str(len(hoteles_filtrados)))
            posicion4.append(str(Hotel.promedioPreciosHoteles(hoteles_filtrados)))
            posicion5.append(str(Reserva.mostrarCantidadPersonasDestino(self, fechas)))

        tabla.extend([posicion0, posicion1, posicion2, posicion3, posicion4, posicion5])
        return tabla

    def mostrarPlaneacionDestino(self, opc_busqueda, clasificacion, tipo, fecha, idioma):
        from gestorAplicacion.tipoActividad import TipoActividad
        from gestorAplicacion.reserva import Reserva
        from gestorAplicacion.hotel import Hotel
        from gestorAplicacion.actividad import Actividad
        tabla = []

        posicion1 = []
        posicion2 = []
        posicion3 = []
        posicion4 = []
        posicion5 = []
        posicion6 = []
        posicion7 = []

        actividades_filtradas = [actividad for actividad in self._actividades if actividad.verificarFiltrosActividad(clasificacion, tipo, fecha, idioma)]
        
        if opc_busqueda == "1":
            posicion1.append(str(len(actividades_filtradas)))
            posicion2.append(str(Actividad.promedioPreciosActividades(actividades_filtradas)))
            posicion3.append(str(Actividad.cantidadGuiasDisponiblesLista(actividades_filtradas)))
            posicion4.append(str(Hotel.cantidadHotelesDestino(self)))
            posicion5.append(self.buscarIdiomaComun().getNombre())
            posicion6.append(Actividad.mostrarClasificacion(Reserva.mostrarClasificacionComun(self)))
            posicion7.append(self.definirOferta(actividades_filtradas))
        elif opc_busqueda == "2":
            posicion1.append(f"C{self.cantidadActividadesTipo(TipoActividad.CULTURALES, actividades_filtradas)}")
            posicion1.append(f"P{Actividad.promedioPreciosActividades(actividades_filtradas, TipoActividad.CULTURALES)}")
            posicion2.append(f"C{self.cantidadActividadesTipo(TipoActividad.FAMILIARES, actividades_filtradas)}")
            posicion2.append(f"P{Actividad.promedioPreciosActividades(actividades_filtradas, TipoActividad.FAMILIARES)}")
            # Similar logic for other types of activities
            posicion7.append(str(len(actividades_filtradas)))
        else:
            posicion1.append(str(len(actividades_filtradas)))
            posicion2.append(str(Actividad.promedioPreciosActividades(actividades_filtradas)))
            posicion3.append(str(Hotel.cantidadHotelesDestino(self)))
            posicion4.append(str(Hotel.promedioPreciosHoteles(self)))
            posicion5.append(str(Reserva.mostrarCantidadPersonasDestino(self)))
            posicion6.append(Reserva.actividadPrincipalDestino(self).getNombre())
            posicion7.append(self.definirOferta(actividades_filtradas))

        tabla.extend([self._nombre, posicion1, posicion2, posicion3, posicion4, posicion5, posicion6, posicion7])
        return tabla

    def mostrarPlaneacionIdioma(self, opc_busqueda, clasificacion, tipo, fecha, idioma):
        from gestorAplicacion.tipoActividad import TipoActividad
        from gestorAplicacion.reserva import Reserva
        from gestorAplicacion.actividad import Actividad
        tabla = []

        posicion1 = []
        posicion2 = []
        posicion3 = []
        posicion4 = []
        posicion5 = []
        posicion6 = []
        posicion7 = []

        actividades_filtradas = [actividad for actividad in self._actividades if actividad.verificarFiltrosActividad(clasificacion, tipo, fecha, idioma)]

        if opc_busqueda == "1":
            posicion1.append(f"C{self.cantidadActividadesTipo(TipoActividad.CULTURALES, actividades_filtradas)}")
            posicion1.append(f"P{Actividad.promedioPreciosActividades(actividades_filtradas, TipoActividad.CULTURALES)}")
            posicion2.append(f"C{self.cantidadActividadesTipo(TipoActividad.FAMILIARES, actividades_filtradas)}")
            posicion2.append(f"P{Actividad.promedioPreciosActividades(actividades_filtradas, TipoActividad.FAMILIARES)}")
            # Similar logic for other types of activities
            posicion7.append(str(len(actividades_filtradas)))
        else:
            posicion1.append(str(len(actividades_filtradas)))
            posicion2.append(str(Actividad.promedioPreciosActividades(actividades_filtradas)))
            posicion3.append(str(Reserva.mostrarCantidadPersonasDestino(self, fecha, idioma)))
            posicion4.append(str(Actividad.cantidadGuiasDisponiblesLista(actividades_filtradas)))
            posicion5.append(Actividad.mostrarClasificacion(Reserva.mostrarClasificacionComun(self, fecha, idioma)))
            posicion6.append(self.definirOferta(actividades_filtradas))

        tabla.extend([idioma.getNombre(), posicion1, posicion2, posicion3, posicion4, posicion5, posicion6, posicion7])
        return tabla

    def buscarIdiomaComun(self):
        from gestorAplicacion.idioma import Idioma
        cantidad_mayor = 0
        idioma_comun = None
        for idioma in Idioma:
            cantidad_idioma = sum(1 for guia in self._guias if idioma in guia.getIdiomas())
            if cantidad_idioma > cantidad_mayor:
                cantidad_mayor = cantidad_idioma
                idioma_comun = idioma
        return idioma_comun

    def definirOferta(self, actividades_lista):
        total_actividades = len(self._actividades)
        if len(actividades_lista) > total_actividades * 0.75:
            return "Alta"
        elif len(actividades_lista) > total_actividades * 0.45:
            return "Normal"
        return "Baja"

    @staticmethod
    def cantidadActividadesTipo(tipo_filtro, actividades_filtradas):
        return sum(1 for actividad in actividades_filtradas if tipo_filtro in actividad.getTipo())

    # Métodos de acceso
    def getActividades(self):
        return self._actividades

    def setActividades(self, actividades):
        self._actividades = actividades

    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    @staticmethod
    def getDestinos():
        return Destino._destinos

    @staticmethod
    def setDestinos(destinos):
        Destino._destinos = destinos

    def getGuias(self):
        return self._guias

    def setGuias(self, guias):
        self._guias = guias

