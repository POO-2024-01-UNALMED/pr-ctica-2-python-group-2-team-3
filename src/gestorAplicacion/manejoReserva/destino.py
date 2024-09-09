from typing import List, Optional
from gestorAplicacion.enums import idiomas, tiposActividad
from gestorAplicacion.gestionHum import guia
from gestorAplicacion.hospedaje import hotel
from gestorAplicacion.manejoReserva import actividad, grupo, reserva
from multimethod import multimethod

class Destino:
    destinos: List['Destino'] = []

    def __init__(self, nombre: str):
        self.guias: List[Guia] = []
        self.actividades: List[Actividad] = []
        self.nombre = nombre
        Destino.destinos.append(self)

    @staticmethod
    def elegir_destino_guia(guia: Guia) -> List['Destino']:
        mayor_cantidad = 0
        lista_destinos = []
        for destino in Destino.destinos:
            lista_actividades = destino.mostrar_actividades_tipo(guia.get_tipo_actividades())
            if len(lista_actividades) == mayor_cantidad:
                lista_destinos.append(destino)
            elif len(lista_actividades) > mayor_cantidad:
                mayor_cantidad = len(lista_actividades)
                lista_destinos.clear()
                lista_destinos.append(destino)
        
        if len(lista_destinos) > 1:
            menor_cantidad = len(lista_destinos[0].guias)
            lista_final = []
            for destino in lista_destinos:
                if len(destino.guias) == menor_cantidad:
                    lista_final.append(destino)
                elif len(destino.guias) < menor_cantidad:
                    menor_cantidad = len(destino.guias)
                    lista_final.clear()
                    lista_final.append(destino)
            lista_destinos = lista_final
        
        if len(lista_destinos) != 1:
            Destino.ingresar_guia(guia, lista_destinos, 1)
        
        return lista_destinos

    def actividades_disponibles_destino(self, clasificacion: int, cantidad_personas: int) -> List[Actividad]:
        actividades_posibles = []
        for actividad in self.actividades:
            if actividad.get_clasificacion() <= clasificacion and actividad.get_capacidad() >= cantidad_personas:
                actividades_posibles.append(actividad)
        return actividades_posibles

    @multimethod
    def mostrar_actividades_tipo(self, guia: Guia) -> List[Actividad]:
        lista = guia.get_tipo_actividades()
        lista_actividades = []
        for tipo_guia in lista:
            for actividad in self.actividades:
                if tipo_guia in actividad.get_tipo() and actividad not in lista_actividades:
                    lista_actividades.append(actividad)
        return lista_actividades

    @multimethod
    def mostrar_actividades_tipo(self, lista: List[TiposActividad]) -> List[Actividad]:
        lista_actividades = []
        for tipo_guia in lista:
            for actividad in self.actividades:
                if tipo_guia in actividad.get_tipo() and actividad not in lista_actividades:
                    lista_actividades.append(actividad)
        return lista_actividades

    @staticmethod
    def ingresar_guia(guia: Guia, lista: List['Destino'], n: int):
        n -= 1
        destino = lista[n]
        destino.guias.append(guia)
        guia.set_destino(destino)

    @staticmethod
    def buscar_destino_comun(lista_destinos: List['Destino']) -> List[str]:
        contador = 0
        cantidad_maxima = 0
        destino_final = []

        for destino in Destino.destinos:
            contador = 0
            for x in lista_destinos:
                if x == destino:
                    contador += 1

            if contador == cantidad_maxima:
                destino_final.append(destino)
            elif contador > cantidad_maxima:
                destino_final.clear()
                destino_final.append(destino)
                cantidad_maxima = contador

        lista_destino = [f"{destino.nombre}={cantidad_maxima}/{len(lista_destinos)}" for destino in destino_final]

        return lista_destino

    def precio_extra_por_temporada(self, fecha: List[int]) -> float:
        porcentaje_precio_extra = 0.0
        mes = fecha[1]

        if mes in [12, 1, 6, 7]:
            porcentaje_precio_extra = 1.4
        elif mes in [2, 3, 11]:
            porcentaje_precio_extra = 0.8
        else:
            porcentaje_precio_extra = 1.0

        cantidad_clientes = Grupo.cantidad_clientes_destino(self, fecha)
        if cantidad_clientes > len(self.guias) * 10:
            porcentaje_precio_extra += 0.3
        elif cantidad_clientes < len(self.guias) * 4:
            porcentaje_precio_extra -= 0.3

        return porcentaje_precio_extra

    def precio_extra_por_destino(self) -> float:
        porcentaje_extra = 1

        destinos_con_mas_actividades = 0
        destinos_con_menos_actividades = 0
        destinos_con_mas_clientes = 0
        destinos_con_menos_clientes = 0

        for destino in Destino.destinos:
            if len(destino.actividades) > len(self.actividades):
                destinos_con_mas_actividades += 1
            else:
                destinos_con_menos_actividades += 1

            if Grupo.cantidad_clientes_destino(destino, None) > Grupo.cantidad_clientes_destino(self, None):
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
    def lista_nombres() -> List[str]:
        return [destino.nombre for destino in Destino.destinos]

    @staticmethod
    def buscar_nombre(nombre: str) -> Optional['Destino']:
        for destino in Destino.destinos:
            if nombre == destino.nombre:
                return destino
        return None

    def mostrar_planeacion_fecha(self, opc_busqueda: str, clasificacion: int, tipo: TiposActividad, fechas: List[List[int]], idioma: Idiomas) -> List[object]:
        posicion = fechas[0][0] if opc_busqueda == "3" else Reserva.mostrar_mes(fechas[0][1])

        posicion0 = [str(posicion)]
        posicion1 = []
        posicion2 = []
        posicion3 = []
        posicion4 = []
        posicion5 = []

        actividades_filtradas = [actividad for actividad in self.actividades if actividad.verificar_filtros_actividad(clasificacion, tipo, fechas, idioma)]
        hoteles_filtrados = []
        for fecha in fechas:
            hoteles_filtrados.extend(Hotel.mostrar_hoteles_filtrados(self, fecha))

        if opc_busqueda == "1":
            posicion1.append(str(len(actividades_filtradas)))
            posicion2.append(str(len(hoteles_filtrados)))
            posicion3.append(self.buscar_idioma_comun().get_nombre())
            posicion4.append(str(Reserva.mostrar_cantidad_personas_destino(self, fechas)))
            posicion5.append(self.definir_oferta(actividades_filtradas))
        elif opc_busqueda == "2":
            posicion1.append(Reserva.actividad_principal_destino(self).get_tipo()[0].get_nombre())
            posicion2.append(str(Actividad.cantidad_guias_disponibles_lista(actividades_filtradas)))
            posicion3.append(str((Hotel.promedio_precios_hoteles(hoteles_filtrados) + Actividad.promedio_precios_actividades(actividades_filtradas)) / 2))
            posicion4.append(str(len(actividades_filtradas)))
            posicion5.append(self.definir_oferta(actividades_filtradas))
        else:
            posicion1.append(str(len(actividades_filtradas)))
            posicion2.append(str(Actividad.promedio_precios_actividades(actividades_filtradas)))
            posicion3.append(str(len(hoteles_filtrados)))
            posicion4.append(str(Hotel.promedio_precios_hoteles(hoteles_filtrados)))
            posicion5.append(str(Reserva.mostrar_cantidad_personas_destino(self, fechas)))

        tabla = [posicion0, posicion1, posicion2, posicion3, posicion4, posicion5]
        return tabla
from typing import List, Optional
from gestorAplicacion.enums import Idiomas, TiposActividad
from gestorAplicacion.gestionHum import Guia
from gestorAplicacion.hospedaje import Hotel
from gestorAplicacion.manejoReserva import Actividad, Grupo, Reserva
from multimethod import multimethod

class Destino:
    """
    Clase Destino que representa un destino turístico con guías y actividades disponibles.
    """

    destinos: List['Destino'] = []

    def __init__(self, nombre: str):
        """
        Constructor de la clase Destino.
        :param nombre: Nombre del destino.
        """
        self.guias: List[Guia] = []
        self.actividades: List[Actividad] = []
        self.nombre = nombre
        Destino.destinos.append(self)

    @staticmethod
    def elegir_destino_guia(guia: Guia) -> List['Destino']:
        """
        Método para elegir un destino para un guía en función de la cantidad de actividades que puede realizar.
        :param guia: Objeto de tipo Guia.
        :return: Lista de destinos sugeridos para el guía.
        """
        mayor_cantidad = 0
        lista_destinos = []
        for destino in Destino.destinos:
            lista_actividades = destino.mostrar_actividades_tipo(guia.get_tipo_actividades())
            if len(lista_actividades) == mayor_cantidad:
                lista_destinos.append(destino)
            elif len(lista_actividades) > mayor_cantidad:
                mayor_cantidad = len(lista_actividades)
                lista_destinos.clear()
                lista_destinos.append(destino)
        
        if len(lista_destinos) > 1:
            menor_cantidad = len(lista_destinos[0].guias)
            lista_final = []
            for destino in lista_destinos:
                if len(destino.guias) == menor_cantidad:
                    lista_final.append(destino)
                elif len(destino.guias) < menor_cantidad:
                    menor_cantidad = len(destino.guias)
                    lista_final.clear()
                    lista_final.append(destino)
            lista_destinos = lista_final
        
        if len(lista_destinos) != 1:
            Destino.ingresar_guia(guia, lista_destinos, 1)
        
        return lista_destinos

    def actividades_disponibles_destino(self, clasificacion: int, cantidad_personas: int) -> List[Actividad]:
        """
        Método para obtener las actividades disponibles en el destino según la clasificación y la cantidad de personas.
        :param clasificacion: Clasificación requerida para las actividades.
        :param cantidad_personas: Cantidad de personas que participarán en las actividades.
        :return: Lista de actividades disponibles que cumplen con los requisitos.
        """
        actividades_posibles = []
        for actividad in self.actividades:
            if actividad.get_clasificacion() <= clasificacion and actividad.get_capacidad() >= cantidad_personas:
                actividades_posibles.append(actividad)
        return actividades_posibles

    @multimethod
    def mostrar_actividades_tipo(self, guia: Guia) -> List[Actividad]:
        """
        Método para mostrar las actividades del destino que coinciden con los tipos de actividades que puede realizar el guía.
        Sobrecarga para manejar un objeto de tipo Guia.
        :param guia: Objeto de tipo Guia.
        :return: Lista de actividades que el guía puede realizar.
        """
        lista = guia.get_tipo_actividades()
        lista_actividades = []
        for tipo_guia in lista:
            for actividad in self.actividades:
                if tipo_guia in actividad.get_tipo() and actividad not in lista_actividades:
                    lista_actividades.append(actividad)
        return lista_actividades

    @multimethod
    def mostrar_actividades_tipo(self, lista: List[TiposActividad]) -> List[Actividad]:
        """
        Método para mostrar las actividades del destino que coinciden con una lista de tipos de actividades.
        Sobrecarga para manejar una lista de TiposActividad.
        :param lista: Lista de tipos de actividades.
        :return: Lista de actividades que coinciden con los tipos proporcionados.
        """
        lista_actividades = []
        for tipo_guia in lista:
            for actividad in self.actividades:
                if tipo_guia in actividad.get_tipo() and actividad not in lista_actividades:
                    lista_actividades.append(actividad)
        return lista_actividades

    @staticmethod
    def ingresar_guia(guia: Guia, lista: List['Destino'], n: int):
        """
        Método para asignar un guía a un destino específico.
        :param guia: Objeto de tipo Guia.
        :param lista: Lista de destinos sugeridos.
        :param n: Índice del destino seleccionado dentro de la lista.
        """
        n -= 1
        destino = lista[n]
        destino.guias.append(guia)
        guia.set_destino(destino)

    @staticmethod
    def buscar_destino_comun(lista_destinos: List['Destino']) -> List[str]:
        """
        Método para encontrar el destino más común en una lista de destinos.
        :param lista_destinos: Lista de destinos a analizar.
        :return: Lista de nombres de destinos más comunes con su frecuencia.
        """
        contador = 0
        cantidad_maxima = 0
        destino_final = []

        for destino in Destino.destinos:
            contador = 0
            for x in lista_destinos:
                if x == destino:
                    contador += 1

            if contador == cantidad_maxima:
                destino_final.append(destino)
            elif contador > cantidad_maxima:
                destino_final.clear()
                destino_final.append(destino)
                cantidad_maxima = contador

        lista_destino = [f"{destino.nombre}={cantidad_maxima}/{len(lista_destinos)}" for destino in destino_final]

        return lista_destino

    def precio_extra_por_temporada(self, fecha: List[int]) -> float:
        """
        Método para calcular el precio extra en función de la temporada y la cantidad de clientes.
        :param fecha: Fecha de la reserva en formato [día, mes, año].
        :return: Porcentaje del precio extra a aplicar.
        """
        porcentaje_precio_extra = 0.0
        mes = fecha[1]

        if mes in [12, 1, 6, 7]:
            porcentaje_precio_extra = 1.4
        elif mes in [2, 3, 11]:
            porcentaje_precio_extra = 0.8
        else:
            porcentaje_precio_extra = 1.0

        cantidad_clientes = Grupo.cantidad_clientes_destino(self, fecha)
        if cantidad_clientes > len(self.guias) * 10:
            porcentaje_precio_extra += 0.3
        elif cantidad_clientes < len(self.guias) * 4:
            porcentaje_precio_extra -= 0.3

        return porcentaje_precio_extra

    def precio_extra_por_destino(self) -> float:
        """
        Método para calcular el precio extra basado en la popularidad y las actividades del destino.
        :return: Porcentaje del precio extra a aplicar.
        """
        porcentaje_extra = 1

        destinos_con_mas_actividades = 0
        destinos_con_menos_actividades = 0
        destinos_con_mas_clientes = 0
        destinos_con_menos_clientes = 0

        for destino in Destino.destinos:
            if len(destino.actividades) > len(self.actividades):
                destinos_con_mas_actividades += 1
            else:
                destinos_con_menos_actividades += 1

            if Grupo.cantidad_clientes_destino(destino, None) > Grupo.cantidad_clientes_destino(self, None):
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
    def lista_nombres() -> List[str]:
        """
        Método para obtener una lista de nombres de todos los destinos registrados.
        :return: Lista de nombres de los destinos.
        """
        return [destino.nombre for destino in Destino.destinos]

    @staticmethod
    def buscar_nombre(nombre: str) -> Optional['Destino']:
        """
        Método para buscar un destino por su nombre.
        :param nombre: Nombre del destino a buscar.
        :return: Objeto Destino si se encuentra, de lo contrario None.
        """
        for destino in Destino.destinos:
            if nombre == destino.nombre:
                return destino
        return None

    def mostrar_planeacion_fecha(self, opc_busqueda: str, busqueda: str) -> List[Reserva]:
        """
        Método para mostrar las reservas planificadas en una fecha específica para el destino.
        :param opc_busqueda: Opción de búsqueda (ej. "destino", "guía").
        :param busqueda: Valor de búsqueda (ej. nombre del destino o guía).
        :return: Lista de reservas que coinciden con la búsqueda.
        """
        lista_reservas = []
        for reserva in Reserva.reservas:
            if busqueda == reserva.get_destino().nombre and reserva.get_destino() == self:
                if opc_busqueda == "Hotel" and reserva.get_hospedaje() is None:
                    lista_reservas.append(reserva)
                elif opc_busqueda == reserva.get_hospedaje().nombre:
                    lista_reservas.append(reserva)
        return lista_reservas
