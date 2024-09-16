from gestorAplicacion.registrable import Registrable
from gestorAplicacion.persona import Persona

class Guia(Persona, Registrable):
    _guias = []

    def __init__(self, nombre, edad, destino=None, tipo_actividades=[],idiomas=[],dias_ocupados = [],dias_no_disponibles = [],destinoNombre=None):
        super().__init__(nombre, destino, edad,idiomas)
        self._tipo_actividades = tipo_actividades
        self._dias_ocupados = dias_ocupados
        self._dias_no_disponibles = dias_no_disponibles
        self._destinoNombre=destinoNombre
        Guia._guias.append(self)


    def toString(self):
        return [
            ("Nombre:", str(self._nombre)),
            ("Edad:", str(self._edad)),
            ("Destino:", str(self._destinoNombre) if self._destinoNombre else "Cartagena"),
            ("Idiomas",', '.join(str(idioma.getNombre()) for idioma in self._idiomas)),
            ("Tipo Actividades:", ', '.join(str(tipo.getNombre()) for tipo in self._tipo_actividades))]


    def ingresarTipoActividades(self, listaTiposActividad):
        from gestorAplicacion.tipoActividad import TipoActividad

        for tipo in listaTiposActividad:
            obj=TipoActividad.buscarNombre(tipo)
            self._tipo_actividades.append(obj)

    def asignarParametros(self):
        precio_base = 30000
        precio_extra = sum(idioma.getPrecio() for idioma in self.getIdiomas())
        porcentaje_extra = self.getDestino().precioExtraPorDestino() if self.getDestino() else 0.5
        self._precio = (precio_base * porcentaje_extra) + precio_extra

    def ingresarGuia(self):
        if self.getDestino():
            lista_actividades = self.getDestino().mostrarActividadesTipo(self)
            for actividad in lista_actividades:
                if self not in actividad.getGuias():
                    actividad.getGuias().append(self)

    @staticmethod
    def buscarGuia(guiaNombre,guiaEdad,guiaDestino):
        guias=Guia.mostrarGuias()
        for guia in guias:
            if (guia._nombre.lower() == guiaNombre.lower() and
                guia._edad == int(guiaEdad) and
                guia._destinoNombre.lower() == guiaDestino.lower()):
                return guia
        guia=Guia.crear_guia()
        return guia
    
    @staticmethod
    def crear_guia():
        import random
        from gestorAplicacion.reserva import Reserva
        from gestorAplicacion.tipoActividad import TipoActividad
        from gestorAplicacion.idioma import Idioma
        nombres = ["Carlos", "Juan", "Laura", "Ana", "María", "Santiago", "Luisa", "Pedro"]
        destinos = ["Cartagena", "Bogotá", "Medellín", "Santa Marta", "San Andrés", 
                    "Cali", "Parque Nacional Natural Tayrona", "Eje Cafetero", "Salento", "Guatapé"]
        nombre = random.choice(nombres)
        edad = random.randint(18, 60)
        destino = random.choice(destinos)
        actividades_seleccionadas = random.sample(list(TipoActividad), random.randint(1, 3))
        idiomas_seleccionados = random.sample(list(Idioma), random.randint(1, 3))
        dias_ocupados = [Reserva.generar_fecha_aleatoria() for _ in range(random.randint(1, 5))]
        dias_no_disponibles = [Reserva.generar_fecha_aleatoria() for _ in range(random.randint(1, 5))]
        guia = Guia(nombre=nombre, edad=edad, destinoNombre=destino, tipo_actividades=actividades_seleccionadas, dias_ocupados=dias_ocupados, dias_no_disponibles=dias_no_disponibles, idiomas=idiomas_seleccionados)
        return guia

    @staticmethod
    def buscarDisponibilidad(guias_capacitados, fecha):
        return [guia for guia in guias_capacitados if fecha not in guia._dias_ocupados]

    def retirarGuia(self, lista_fechas=None,tipoRetiro="Dar de baja por un tiempo"):
        from gestorAplicacion.grupo import Grupo
        resumen=self.toString()
        resumen.append(("Tipo de retiro:",tipoRetiro))
        for dia in self._dias_ocupados:
            if dia not in self._dias_no_disponibles and (lista_fechas is None or dia in lista_fechas):
                Grupo.retirar_guia(self, dia)

        if lista_fechas:
            for dia in lista_fechas:
                if dia not in self._dias_ocupados:
                    self._dias_ocupados.append(dia)
                if dia not in self._dias_no_disponibles:
                    self._dias_no_disponibles.append(dia)
            resumen.append(("Fechas a retirar:",lista_fechas[0]+" - "+lista_fechas[-1]))
   
        resumen=resumen+Guia.generar_lista_estadisticas()
        return resumen

    def retirarGuiaDespido(self):
        from gestorAplicacion.actividad import Actividad
        resumen=self.retirarGuia(tipoRetiro="Despedir definitivamente")
        Actividad.retirarGuia(self)
        Guia._guias.remove(self)
        return resumen
        
    @staticmethod   
    def generar_lista_estadisticas():
        import random
        estadisticas = ["Grupos eliminados","Reservas reubicadas","Reservas sin reubicar"]
        lista_estadisticas = [(stat, str(random.randint(1, 20))) for stat in estadisticas]
        return lista_estadisticas
    
    @classmethod
    def mostrarGuias(cls):
        from gestorAplicacion.tipoActividad import TipoActividad
        from gestorAplicacion.idioma import Idioma
        from gestorAplicacion.destino import Destino
        from gestorAplicacion.reserva import Reserva
        if cls._guias==[]:
            nombres = ["Carlos", "Ana", "María", "Juan", "Luisa", "Pedro", "Laura", "Santiago", "Laura", "Pablo"]
            edades = [35, 29, 41, 32, 28, 46, 33, 37, 18, 40]
            destinos = Destino.listaNombres()
            actividades = [
                [TipoActividad.CULTURALES, TipoActividad.FAMILIARES],[TipoActividad.ECOLOGICAS, TipoActividad.EXTREMAS],
                [TipoActividad.ACUATICAS],[TipoActividad.DEPORTIVAS],[TipoActividad.RESTAURANTE, TipoActividad.HOSPEDAJE],[TipoActividad.CULTURALES, TipoActividad.DEPORTIVAS],
                [TipoActividad.ECOLOGICAS],[TipoActividad.ACUATICAS, TipoActividad.CULTURALES],
                [TipoActividad.FAMILIARES, TipoActividad.RESTAURANTE],[TipoActividad.EXTREMAS, TipoActividad.DEPORTIVAS]]
            dias_ocupados = Reserva.generar_lista_fechas_aleatorias()
            dias_no_disponibles = Reserva.generar_lista_fechas_aleatorias()
            idiomas = [[Idioma.INGLES, Idioma.ESPANOL], [Idioma.FRANCES, Idioma.ESPANOL], [Idioma.ITALIANO],
                [Idioma.PORTUGUES], [Idioma.ESPANOL, Idioma.INGLES], [Idioma.ESPANOL], [Idioma.INGLES, Idioma.FRANCES],
                [Idioma.ESPANOL, Idioma.ITALIANO], [Idioma.ESPANOL], [Idioma.INGLES, Idioma.PORTUGUES]]

            for i in range(10):
                Guia(nombre=nombres[i],edad=edades[i],destinoNombre=destinos[i],tipo_actividades=actividades[i],dias_ocupados=dias_ocupados[i],dias_no_disponibles=dias_no_disponibles[i],idiomas=idiomas[i])
        return  cls._guias
         
    @staticmethod
    def mostrarDisponibilidadGuias(dia_str, destino=None, idioma=None, guia=None,filtros=None):
        from gestorAplicacion.idioma import Idioma
        from gestorAplicacion.destino import Destino
        import random
        from datetime import datetime 
        actividades = ["Tour en bicicleta", "Excursión en la montaña", "Visita guiada al museo", "Buceo", 
                    "Senderismo", "Paseo en barco", "Tour de comida", "Clase de surf", "Tour histórico", 
                    "Visita a viñedos"]
        destinos =Destino.listaNombres()
        estados = ['Disponible', 'Ocupado']
        guias = ['Carlos', 'María', 'Juan', 'Pedro', 'Ana', 'Luis', 'Fernanda', 'Camila', 'Alejandro', 'Sofia',"Valeria", "Mateo", "Sebastián", "Lucía", "Diego", "Sofía", "Andrés", "Daniela", "Tomás", "Isabella", "Laura", "Paulina", "Santiago", "Lana"]
        dia = datetime.strptime(dia_str, '%d/%m/%Y')
        if filtros:
            filtrosVerDisponibilidadGuias = {
                "Disponibilidad de todos los guías":random.choice(estados),
                "Solo los guías disponibles":'Disponible',
                "Solo los guías ocupados":'Ocupado'}
            estado=filtrosVerDisponibilidadGuias[filtros]
        else:
            estado=random.choice(estados)
        lista_tuplas = {
            "Destino":destino if destino else random.choice(destinos),
            "Nombre":guia if guia else random.choice(guias),
            "Idioma":"Ninguno" if estado!='Ocupado' else idioma if idioma else random.choice([idioma.value[0] for idioma in Idioma]),
            "Dia":dia_str,"Mes":dia.strftime('%B'),
            "Estado":estado,"Actividad":random.choice(actividades) if estado=='Ocupado' else "Ninguna",
            "Personas":"0" if estado!='Ocupado' else str(random.randint(1, 100)),"Guias":str(random.randint(1, 15)),"Actividades":str(random.randint(1, 20))}

        return lista_tuplas

    @staticmethod
    def verificarGuia(guiaNombre,guiaEdad,guiaDestino):
        guias = Guia.mostrarGuias()
        
        for guia in guias:
            if (guia._nombre.lower() == guiaNombre.lower() and
                guia._edad == int(guiaEdad) and
                guia._destinoNombre.lower() == guiaDestino.lower()):
                return True
        return False

            
    def mostrarIntinerario(self, fecha):
        from gestorAplicacion.grupo import Grupo
        from gestorAplicacion.reserva import Reserva
        tabla = []
        estado = "Disponible"
        tipo_actividades = []
        grupo = None
        cantidad_personas = 0

        if fecha in self._dias_ocupados:
            estado = "Ocupado"
            grupo = Grupo.buscarGrupo(fecha, self)
        elif fecha in self._dias_no_disponibles:
            estado = "No disponible"

        for reserva in grupo.getListaReservas():
            cantidad_personas += len(reserva)

        for tipo in grupo.getActividad().getTipo():
            tipo_actividades.append(f"{tipo.getNombre()},")

        tabla.extend([
            fecha[2],  # año
            Reserva.mostrarMes(fecha[1]),  # mes
            fecha[0],  # día
            self.getNombre(),  # nombre
            self.getDestino(),  # destino
            estado,  # estado
            grupo.getActividad().getNombre(),  # actividad
            tipo_actividades,  # tipo actividad
            grupo.getIdioma(),  # idioma
            cantidad_personas,  # cantidad de personas
            grupo.getClasificacion()  # clasificación
        ])

        return tabla

    def asignarGuia(self, grupo):
        self._dias_ocupados.append(grupo.getFecha())
        grupo.setGuia(self)

    def mostrarPrecioGuia(self, fecha):
        porcentaje_extra = self.getDestino().precioExtraPorTemporada(fecha)
        return self._precio * porcentaje_extra

    # Métodos de acceso
    def getTipoActividades(self):
        return self._tipo_actividades

    def setTipoActividades(self, tipo_actividades):
        self._tipo_actividades = tipo_actividades

    def getPrecio(self):
        return self._precio

    def setPrecio(self, precio):
        self._precio = precio
        
    def setDestinoNombre(self,nombre):
        self._destinoNombre=nombre
        
    def getDestinoNombre(self):
        return self._destinoNombre

    def getDiasOcupados(self):
        return self._dias_ocupados

    def setDiasOcupados(self, dias_ocupados):
        self._dias_ocupados = dias_ocupados

    def getDiasNoDisponibles(self):
        return self._dias_no_disponibles

    def setDiasNoDisponibles(self, dias_no_disponibles):
        self._dias_no_disponibles = dias_no_disponibles

    @staticmethod
    def getGuias():
        return Guia._guias

    @staticmethod
    def setGuias(guias):
        Guia._guias = guias
