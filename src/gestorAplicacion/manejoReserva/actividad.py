from typing import List, Optional
from datetime import datetime
from gestorAplicacion.enums import idiomas, tiposActividad
from gestorAplicacion.interfaces import registrable
from gestorAplicacion.manejoReserva import destino
from gestorAplicacion.actividades import plan
from gestorAplicacion.gestionHum import guia,cliente
class Actividad:
    def __init__(self, nombre: str, destino: 'Destino', tipo1: Optional['TiposActividad'] = None,
                 tipo2: Optional['TiposActividad'] = None, capacidad: int = 0, clasificacion: int = 0,
                 precio: float = 0.0):
        """
        Constructor para la clase Actividad.
        
        :param nombre: Nombre de la actividad.
        :param destino: Destino asociado con la actividad.
        :param tipo1: Primer tipo de actividad.
        :param tipo2: Segundo tipo de actividad.
        :param capacidad: Capacidad máxima del grupo.
        :param clasificacion: Clasificación por edad de la actividad.
        :param precio: Precio por persona para la actividad.
        """
        self.nombre = nombre
        self.destino = destino
        self.tipo = [tipo1, tipo2] if tipo1 and tipo2 else []
        self.guias = []
        self.capacidad = capacidad
        self.clasificacion = clasificacion
        self.precio = precio
        if destino:
            destino.get_actividades().append(self)

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena de la actividad.
        
        :return: Información detallada de la actividad.
        """
        return (f"Nombre de la actividad: {self.nombre},\nSe encuentra en: {self.destino.get_nombre()},\n"
                f"Tipo de actividad: {self.tipo},\nCapacidad por grupo: {self.capacidad},\n"
                f"Clasificacion por edad: +{self.clasificacion},\nPrecio por persona: {self.precio}")

    def ingresar_guia(self):
        """
        Asigna guías a la actividad según el tipo de actividad y destino.
        """
        for tipo in self.tipo:
            for guia in Guia.get_guias():
                if tipo in guia.get_tipo_actividades() and guia.get_destino() == self.destino and guia not in self.guias:
                    self.guias.append(guia)

    def ingresar_tipo_actividades(self, tipo_actividades: str):
        """
        Asigna tipos de actividad a la instancia a partir de una cadena de texto.
        
        :param tipo_actividades: Cadena con los tipos de actividad, separados por espacios.
        """
        lista_string = tipo_actividades.split(" ")
        for numero in lista_string:
            indice = int(numero) - 1
            self.tipo.append(TiposActividad.values()[indice])
        if len(self.tipo) == 1:
            self.tipo.append(self.tipo[0])

    def asignar_parametros(self):
        """
        Ajusta los parámetros de capacidad, clasificación y precio según los tipos de actividad y otros factores.
        """
        capacidad = 0
        clasificacion = 0
        precio_b = 0
        for tipo in self.tipo:
            if tipo.get_dificultad() == "Baja":
                capacidad += 15
                clasificacion += 30
            elif tipo.get_dificultad() == "Media":
                capacidad += 10
                clasificacion += 15
                precio_b += 10
            elif tipo.get_dificultad() == "Alta":
                capacidad += 8
                clasificacion += 10
                precio_b += 100
            elif tipo.get_dificultad() == "Extrema":
                capacidad += 5
                clasificacion += 5
                precio_b += 1000

        actividades_con_mas_guias = 0
        actividades_con_menos_guias = 0
        cantidad_actividades_con_mismo_tipo = 0
        for actividad in self.destino.get_actividades():
            if len(actividad.guias) > len(self.guias):
                actividades_con_mas_guias += 1
            else:
                actividades_con_menos_guias += 1
            for tipo in self.tipo:
                if tipo in actividad.tipo:
                    cantidad_actividades_con_mismo_tipo += 1
            if (len(self.destino.get_actividades()) / 4) > cantidad_actividades_con_mismo_tipo:
                capacidad += 3
            elif (len(self.destino.get_actividades()) / 2) > cantidad_actividades_con_mismo_tipo:
                capacidad += 2
            elif (len(self.destino.get_actividades()) * 0.75) < cantidad_actividades_con_mismo_tipo:
                capacidad -= 1

        if (((actividades_con_mas_guias + actividades_con_menos_guias) / 4) > actividades_con_mas_guias):
            capacidad -= 5
        elif (((actividades_con_mas_guias + actividades_con_menos_guias) / 2) > actividades_con_mas_guias):
            capacidad -= 3
        elif (((actividades_con_mas_guias + actividades_con_menos_guias) / 4) > actividades_con_menos_guias):
            capacidad += 3

        self.capacidad = capacidad

        if clasificacion <= 10:
            self.clasificacion = 4
        elif clasificacion <= 20:
            self.clasificacion = 3
        elif clasificacion <= 30:
            self.clasificacion = 2
        else:
            self.clasificacion = 1

        if precio_b > 1000:
            self.precio = (60000 * capacidad + 930000) / capacidad
        elif precio_b > 100:
            self.precio = (30000 * capacidad + 1150000) / capacidad
        elif precio_b > 10:
            self.precio = (4000 * capacidad + 1400000) / capacidad
        else:
            self.precio = 1200000 / capacidad

        self.precio = round(self.precio / 100) * 100

    def verificar_filtros_actividad(self, clasificacion_filtro: int, tipo_filtro: Optional['TiposActividad'],
                                    fecha_filtro: List[List[int]], idioma_filtro: Optional['Idiomas']) -> bool:
        """
        Verifica si la actividad cumple con los filtros proporcionados.
        
        :param clasificacion_filtro: Clasificación por edad deseada.
        :param tipo_filtro: Tipo de actividad requerido.
        :param fecha_filtro: Fechas disponibles para la actividad.
        :param idioma_filtro: Idioma requerido para la actividad.
        :return: Verdadero si la actividad cumple con todos los filtros, falso en caso contrario.
        """
        is_clasificacion_match = (clasificacion_filtro == 0) or (self.clasificacion == clasificacion_filtro)
        is_tipo_match = (tipo_filtro is None) or self.verificar_tipo_actividad(tipo_filtro)
        is_idioma_match = (idioma_filtro is None) or len(self.buscar_guia(idioma_filtro)) != 0
        is_fecha_disponible = False

        for fecha in fecha_filtro:
            if self.verifica_actividad_disponible(fecha, idioma_filtro):
                is_fecha_disponible = True

        is_fecha_match = (fecha_filtro is None) or is_fecha_disponible

        return is_clasificacion_match and is_tipo_match and is_idioma_match and is_fecha_match

    def verificar_tipo_actividad(self, tipo_filtro: 'TiposActividad') -> bool:
        """
        Verifica si la actividad corresponde al tipo proporcionado.
        
        :param tipo_filtro: Tipo de actividad requerido.
        :return: Verdadero si el tipo de actividad es uno de los tipos asignados, falso en caso contrario.
        """
        return tipo_filtro in self.tipo

    @staticmethod
    def mostrar_nombres(actividades_lista: List['Actividad']) -> Optional[List[str]]:
        """
        Muestra los nombres de las actividades en una lista.
        
        :param actividades_lista: Lista de actividades.
        :return: Lista de nombres de actividades o None si la lista está vacía.
        """
        if not actividades_lista:
            return None
        return [actividad.nombre for actividad in actividades_lista]

    def verifica_actividad_disponible(self, fecha: List[int], idioma: Optional['Idiomas']) -> bool:
        """
        Verifica si hay disponibilidad para la actividad en una fecha y idioma específicos.
        
        :param fecha: Fecha para la actividad.
        :param idioma: Idioma requerido para la actividad.
        :return: Verdadero si la actividad está disponible, falso en caso contrario.
        """
        existen_grupos = Grupo.buscar_grupo(fecha, self) if idioma is None else Grupo.buscar_grupo(fecha, self, idioma)
        if existen_grupos:
            return True
        elif not existen_grupos:
            guias_capacitados = self.destino.get_guias()
            guias_con_disponibilidad = Guia.buscar_disponibilidad(guias_capacitados, fecha)
            return len(guias_con_disponibilidad) > 0
        return False

    def mostrar_planeacion_actividades(self, opc_busqueda: str, clasificacion: int, tipo: Optional['TiposActividad'],
                                        fecha: List[List[int]], idioma: Optional['Idiomas']) -> List:
        """
        Muestra la planificación de actividades según los filtros proporcionados.
        
        :param opc_busqueda: Opción de búsqueda para la planificación.
        :param clasificacion: Clasificación por edad para las actividades.
        :param tipo: Tipo de actividad para filtrar.
        :param fecha: Fechas para filtrar la disponibilidad de actividades.
        :param idioma: Idioma para filtrar la disponibilidad de guías.
        :return: Lista de actividades que cumplen con los filtros.
        """
        lista_actividades = []
        actividades_filtradas = []

        if opc_busqueda == "0":
            lista_actividades = Actividad.buscar_actividad_por_clasificacion(Actividad.get_actividades(), clasificacion)
        elif opc_busqueda == "1":
            lista_actividades = Actividad.buscar_actividad_por_tipo(Actividad.get_actividades(), tipo)
        elif opc_busqueda == "2":
            lista_actividades = Actividad.buscar_actividad_por_fecha(Actividad.get_actividades(), fecha, idioma)
        elif opc_busqueda == "3":
            lista_actividades = Actividad.buscar_actividad_por_destino(Actividad.get_actividades(), self.destino)

        if opc_busqueda == "0" or opc_busqueda == "2":
            actividades_filtradas = [actividad for actividad in lista_actividades if actividad.verificar_filtros_actividad(
                clasificacion, tipo, fecha, idioma)]

        return actividades_filtradas

    @staticmethod
    def cantidad_guias_lista(actividades_lista: List['Actividad'], idioma: Optional['Idiomas']) -> int:
        """
        Calcula la cantidad total de guías disponibles para una lista de actividades y un idioma específico.
        
        :param actividades_lista: Lista de actividades.
        :param idioma: Idioma requerido para los guías.
        :return: Cantidad total de guías disponibles.
        """
        cantidad_guias = 0
        for actividad in actividades_lista:
            if idioma:
                cantidad_guias += len(actividad.buscar_guia(idioma))
            else:
                cantidad_guias += len(actividad.guias)
        return cantidad_guias

    @staticmethod
    def cantidad_guias_disponibles_lista(actividades_lista: List['Actividad'], idioma: Optional['Idiomas']) -> int:
        """
        Calcula la cantidad total de guías disponibles para una lista de actividades y un idioma específico.
        
        :param actividades_lista: Lista de actividades.
        :param idioma: Idioma requerido para los guías.
        :return: Cantidad total de guías disponibles.
        """
        cantidad_guias = 0
        for actividad in actividades_lista:
            if idioma:
                cantidad_guias += len(actividad.buscar_guia(idioma))
            else:
                cantidad_guias += len(actividad.guias)
        return cantidad_guias

    @staticmethod
    def buscar_actividad_por_tipo(actividades_lista: List['Actividad'], tipo_filtro: 'TiposActividad') -> List['Actividad']:
        """
        Busca actividades en una lista que coincidan con un tipo específico.
        
        :param actividades_lista: Lista de actividades.
        :param tipo_filtro: Tipo de actividad a buscar.
        :return: Lista de actividades que coinciden con el tipo.
        """
        return [actividad for actividad in actividades_lista if tipo_filtro in actividad.tipo]

    @staticmethod
    def buscar_actividad_por_fecha(actividades_lista: List['Actividad'], fecha: List[int], idioma: Optional['Idiomas']) -> List['Actividad']:
        """
        Busca actividades en una lista que estén disponibles en una fecha y idioma específicos.
        
        :param actividades_lista: Lista de actividades.
        :param fecha: Fecha a buscar.
        :param idioma: Idioma requerido para la actividad.
        :return: Lista de actividades disponibles en la fecha y idioma.
        """
        return [actividad for actividad in actividades_lista if actividad.verifica_actividad_disponible(fecha, idioma)]

    @staticmethod
    def buscar_actividad_por_clasificacion(actividades_lista: List['Actividad'], clasificacion_filtro: int) -> List['Actividad']:
        """
        Busca actividades en una lista que coincidan con una clasificación por edad específica.
        
        :param actividades_lista: Lista de actividades.
        :param clasificacion_filtro: Clasificación por edad a buscar.
        :return: Lista de actividades que coinciden con la clasificación.
        """
        return [actividad for actividad in actividades_lista if actividad.clasificacion == clasificacion_filtro]

    @staticmethod
    def buscar_actividad_por_destino(actividades_lista: List['Actividad'], destino_filtro: 'Destino') -> List['Actividad']:
        """
        Busca actividades en una lista que correspondan a un destino específico.
        
        :param actividades_lista: Lista de actividades.
        :param destino_filtro: Destino a buscar.
        :return: Lista de actividades que coinciden con el destino.
        """
        return [actividad for actividad in actividades_lista if actividad.destino == destino_filtro]
