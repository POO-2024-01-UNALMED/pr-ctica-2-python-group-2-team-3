from gestorAplicacion.registrable import Registrable

class Actividad(Registrable):
    _actividades=[]
    def __init__(self, nombre, destino=None,destinoNombre=None, tiposActividad=[], guias=[], capacidad=0, clasificacion=0, precio=0.0):
        self._nombre = nombre
        self._destino = destino
        self._tipo = tiposActividad
        self._guias = guias
        self._deestinonombre=destinoNombre
        self._capacidad = capacidad
        self._clasificacion = clasificacion
        self._precio = precio
        if destinoNombre or destino.getNombre():
            destinop=destinoNombre if destinoNombre else destino.getNombre()
            Actividad._actividades.append((nombre,destinop))

    def toString(self):
        return [
            ("Nombre:", str(self._nombre)),
            ("Destino:", self._destino.getNombre()),
            ("Tipos de Actividad:", ', '.join(TipoActividad.getNombre() for TipoActividad in self._tipo)),
            ("Guias:", ', '.join(guia.getNombre() for guia in self._guias)),
            ("Capacidad:", str(self._capacidad)),
            ("Clasificacion:", str(self._clasificacion)),
            ("Precio:", str(self._precio))
        ]

    def ingresarGuia(self):
        from gestorAplicacion.guia import Guia
        for tipo in self._tipo:
            for guia in Guia.getGuias():
                if tipo in guia.getTipoActividades() and guia.getDestino() == self._destino and guia not in self._guias:
                    self._guias.append(guia)

    def ingresarTipoActividades(self, listaTiposActividad):
        from gestorAplicacion.tipoActividad import TipoActividad
        for tipo in listaTiposActividad:
            obj=TipoActividad.buscarNombre(tipo)
            self._tipo.append(obj)
        if len(self._tipo) == 1:
            self._tipo.append(self._tipo[0])

    @staticmethod
    def verificarActividad(actividadNombre,actividadDestino):
        actividades=Actividad.mostrarActividades()
        for a in actividades:
            if a._nombre==actividadNombre and a._destinoNombre==actividadDestino:
                return True
            else : return False

    def mostrarActividades(cls):
        if cls._actividades==[]:
            nombres = ["Tour Ciudad", "Aventura Extrema", "Visita Histórica", "Recorrido Gastronómico", "Safari Ecológico", "Tour Nocturno", "Excursión Acuática", "Escalada de Montaña", 
                "Taller Cultural", "Senderismo", "Exploración Submarina", "Paseo en Bicicleta", "Trekking en la Selva", "Tour de Arte Urbano", "Ruta del Café"]
            destinos = ["Cartagena", "Bogotá", "Medellín", "Santa Marta", "San Andrés", "Cali", "Parque Nacional Natural Tayrona", 
                "Eje Cafetero", "Salento", "Guatapé", "San Andrés", "Bogotá", "Eje Cafetero", "Medellín", "Salento"]
            
            actividades = {nombres[i]: destinos[i] for i in range(15)}
        else:
            actividades=cls._actividades
        return actividades
            
    def asignarParametros(self):
        capacidad = 0
        clasificacion = 0
        precioB = 0
        for tipo in self._tipo:
            if tipo.getDificultad() == "Baja":
                capacidad += 15
                clasificacion += 30
            elif tipo.getDificultad() == "Media":
                capacidad += 10
                clasificacion += 15
                precioB += 10
            elif tipo.getDificultad() == "Alta":
                capacidad += 8
                clasificacion += 10
                precioB += 100
            elif tipo.getDificultad() == "Extrema":
                capacidad += 5
                clasificacion += 5
                precioB += 1000

        self._capacidad = capacidad
        self._clasificacion = 1 if clasificacion > 30 else 2 if clasificacion > 20 else 3 if clasificacion > 10 else 4
        self._precio = round(self.calcularPrecio(precioB, capacidad))

    def calcularPrecio(self, precioB, capacidad):
        if precioB > 1000:
            return (60000 * capacidad + 930000) / capacidad
        elif precioB > 100:
            return (30000 * capacidad + 1150000) / capacidad
        elif precioB > 10:
            return (4000 * capacidad + 1400000) / capacidad
        else:
            return 1200000 / capacidad

    
    def verificarFiltrosActividad(self, clasificacionFiltro, tipoFiltro, fechaFiltro, idiomaFiltro):
        is_clasificacion_match = (clasificacionFiltro == 0) or self._clasificacion == clasificacionFiltro
        is_tipo_match = (tipoFiltro is None) or self.verificarTipoActividad(tipoFiltro)
        is_idioma_match = (idiomaFiltro is None) or len(self.buscarGuia(idiomaFiltro)) > 0
        is_fecha_disponible = any(self.verificaActividadDisponible(fecha, idiomaFiltro) for fecha in fechaFiltro)
        is_fecha_match = (fechaFiltro is None) or is_fecha_disponible
        return is_clasificacion_match and is_tipo_match and is_idioma_match and is_fecha_match

    def verificarTipoActividad(self, tipoFiltro):
        return tipoFiltro in self._tipo

    @staticmethod
    def mostrarNombres(actividades_lista):
        return [actividad._nombre for actividad in actividades_lista] if actividades_lista else None

    def verificaActividadDisponible(self, fecha, idioma):
        from gestorAplicacion.guia import Guia
        from gestorAplicacion.grupo import Grupo
        existen_grupos = Grupo.buscarGrupo(fecha, self) if idioma is None else Grupo.buscarGrupo(fecha, self, idioma)
        if existen_grupos:
            return True
        guias_con_disponibilidad = Guia.buscarDisponibilidad(self._destino.getGuias(), fecha)
        return bool(guias_con_disponibilidad)


    def mostrarPlaneacionActividades(self, opcBusqueda, clasificacion, tipo, fecha, idioma):
        from gestorAplicacion.reserva import Reserva
        
        tabla = []

        posicion1 = []  # "1"=actividades familiares;"2"=disponibilidad de actividades
        posicion2 = []  # "1"=actividades ecologicas;"2"=promedio de precios actividades
        posicion3 = []  # "1"=actividades ecologicas;"2"=cantidad de personas
        posicion4 = []  # "1"=actividades extremas;"2"=cantidad de guias
        posicion5 = []  # "1"=actividades acuaticas;"2"= clasificacion mas solicitada
        posicion6 = []  # "1"=actividades deportivas;"2"=oferta
        posicion7 = []  # "1"=total de actividades;"2"=[];

        posicion1.append(str(self._capacidad))
        posicion2.append(self.mostrarClasificacion(self._clasificacion))
        posicion3.append(str(Reserva.mostrarCantidadReservasActividad(self._destino, fecha, self)))
        posicion4.append(self._tipo[0].getNombre())
        posicion5.append(self._tipo[0].getDificultad())
        posicion6.append(self.buscarIdiomaComun().getNombre())
        posicion7.append(f"{self._precio}$")

        tabla.append(idioma.getNombre())  # 0. nombre del idioma
        tabla.append(posicion1)  # 1. actividades familiares/disponibilidad
        tabla.append(posicion2)  # 2. actividades ecológicas/precios
        tabla.append(posicion3)  # 3. cantidad de personas
        tabla.append(posicion4)  # 4. cantidad de guías
        tabla.append(posicion5)  # 5. clasificación solicitada
        tabla.append(posicion6)  # 6. oferta
        tabla.append(posicion7)  # 7. total de actividades

        return tabla

    def buscarIdiomaComun(self):
        from gestorAplicacion.idioma import Idioma
        cantidadMayor = 0
        idiomaComun = None
        for idioma in Idioma.values():
            cantidadIdioma = 0
            for guia in self._guias:
                if idioma in guia.getIdiomas():
                    cantidadIdioma += 1
            if cantidadIdioma > cantidadMayor:
                cantidadMayor = cantidadIdioma
                idiomaComun = idioma
        return idiomaComun

    @staticmethod
    def promedioPreciosActividades(actividades_lista):
        if not actividades_lista:
            return 0
        promedio = sum(actividad._precio for actividad in actividades_lista)
        return promedio // len(actividades_lista)

    @staticmethod
    def promedioPreciosActividadesFiltrado(actividades_lista, tipoFiltro):
        if not actividades_lista:
            return 0
        promedio = sum(actividad._precio for actividad in actividades_lista if tipoFiltro in actividad._tipo)
        return promedio // len(actividades_lista)

    @staticmethod
    def cantidadGuiasDisponiblesLista(actividades_lista):
        if actividades_lista is None:
            return 0
        guias = set()
        for actividad in actividades_lista:
            for guia in actividad._guias:
                guias.add(guia)
        return len(guias)

    def buscarGuia(self, idioma):
        return [guia for guia in self._guias if idioma in guia.getIdiomas()]

    @staticmethod
    def retirarGuia(guia):
        from gestorAplicacion.destino import Destino
        destino = guia.getDestino()
        if isinstance(destino,Destino):
            actividades = destino.mostrarActividadesTipo(guia)
            for actividad in actividades:
                if guia in actividad._guias:
                    actividad._guias.remove(guia)

    @staticmethod
    def buscarActividad(nombre, destino):
        from gestorAplicacion.destino import Destino     

        destino_actividad = Destino.buscarNombre(destino)
        if destino_actividad:
            for actividad in destino_actividad.getActividades():
                if nombre == actividad._nombre:
                    return actividad
        return None

    @staticmethod
    def retirarActividad(actividad):
        from gestorAplicacion.grupo import Grupo
        Grupo.retirarActividad(actividad, None)
        actividades = actividad._destino.getActividades()
        actividades.remove(actividad)
        actividad._destino.setActividades(actividades)
        actividad = None
        return True

    @staticmethod
    def mostrarClasificacion(indice):
        opcionesClasificacion = ["[0<edad<7]", "[7<edad<15]", "[15<edad<18]", "[18<edad]"]
        return opcionesClasificacion[indice - 1]


    # Métodos de acceso
    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_destino(self):
        return self._destino

    def set_destino(self, destino):
        self._destino = destino

    def get_tipo(self):
        return self._tipo

    def set_tipo(self, tipo):
        self._tipo = tipo

    def get_guias(self):
        return self._guias

    def set_guias(self, guias):
        self._guias = guias

    def get_capacidad(self):
        return self._capacidad

    def set_capacidad(self, capacidad):
        self._capacidad = capacidad

    def get_clasificacion(self):
        return self._clasificacion

    def set_clasificacion(self, clasificacion):
        self._clasificacion = clasificacion

    def get_precio(self):
        return self._precio

    def set_precio(self, precio):
        self._precio = precio

