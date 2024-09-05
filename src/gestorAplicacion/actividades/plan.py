from typing import List, Dict, Any
import pickle

class Plan:
    paquetes: List['Plan'] = []

    def __init__(self, tipo: str = None, destino: 'Destino' = None, actividades: List['Actividad'] = None, clasificacion: int = None, reserva: 'Reserva' = None):
        self.tipo = tipo
        self.destino = destino
        self.actividades = actividades if actividades is not None else []
        self.precio = 0.0
        self.clasificacion = clasificacion
        self.grupos = []
        self.reserva = reserva
        self.cantidadDias = 0
        self.disponibilidadHabitaciones = {}

        if reserva:
            self.reserva.set_plan(self)
            self.tipo = reserva.get_tipo_plan()

    def mostrar_planeacion_plan(self, opc_busqueda: str, clasificacion: int, tipo: 'TiposActividad', fecha: List[List[int]], idioma: 'Idiomas') -> List[Any]:
        tabla = []

        posicion1 = []  # "1"=actividades familiares;"2"=disponibilidad de actividades
        posicion2 = []  # "1"=actividades ecologicas;"2"=promedio de precios actividades
        posicion3 = []  # "1"=actividades ecologicas;"2"=cantidad de personas
        posicion4 = []  # "1"=actividades extremas;"2"=cantidad de guias
        posicion5 = []  # "1"=actividades acuaticas;"2"= clasificacion mas solicitada

        actividades_filtradas = [actividad for actividad in self.actividades if actividad.verificar_filtros_actividad(clasificacion, tipo, fecha, idioma)]

        if opc_busqueda == "1":
            posicion1.append(str(self.cantidadDias))
            posicion2.append(str(len(self.actividades)))
            posicion3.extend(Actividad.mostrar_nombres(actividades_filtradas))
            posicion4.append(Actividad.mostrar_clasificacion(self.clasificacion))
            posicion5.append(f"{self.precio}$")
        else:
            posicion1.append(str(self.cantidadDias))
            posicion2.append(Actividad.mostrar_clasificacion(self.clasificacion))
            posicion3.append(str(len(self.actividades)))
            posicion4.append(self.mostrar_tipo_predominante().get_nombre())
            posicion5.append(self.mostrar_tipo_predominante().get_dificultad())

        tabla.append(self.destino)  # 0.tipo de plan
        tabla.append(posicion1)  # 1."1"=actividades familiares;"2"=disponibilidad de actividades
        tabla.append(posicion2)  # 2."1"=actividades ecologicas;"2"=promedio de precios actividades
        tabla.append(posicion3)  # 3."1"=actividades ecologicas;"2"=cantidad de personas
        tabla.append(posicion4)  # 4."1"=actividades extremas;"2"=cantidad de guias
        tabla.append(posicion5)  # 5."1"=actividades acuaticas;"2"= clasificacion mas solicitada

        return tabla

    @staticmethod
    def mostrar_paquetes_destino(destino: 'Destino') -> List['Plan']:
        return [paquete for paquete in Plan.paquetes if paquete.destino == destino]

    def añadir_actividad(self, actividad: 'Actividad'):
        self.actividades.append(actividad)

    @staticmethod
    def mostrar_nombre_actividad(actividades: List['Actividad']) -> List[str]:
        return [actividad.get_nombre() for actividad in actividades]

    def mostrar_tipo_predominante(self) -> 'TiposActividad':
        cantidad_mayor = 0
        tipo_predominante = None
        for tipo in TiposActividad:
            cantidad = sum(1 for actividad in self.actividades if tipo in actividad.get_tipo())
            if cantidad > cantidad_mayor:
                cantidad_mayor = cantidad
                tipo_predominante = tipo
        return tipo_predominante

    def mostrar_nombre_actividad(self) -> List[str]:
        return [actividad.get_nombre() for actividad in self.actividades]

    def escoger_actividades_iniciales(self, actividades_disponibles: List['Actividad'], seleccionadas: List[str]) -> List['Actividad']:
        return [actividad for actividad in actividades_disponibles if actividad.get_nombre() in seleccionadas]

    def actividades_disponibles_dia(self, fecha: List[int], seleccion_inicial: List['Actividad']) -> List['Actividad']:
        actividades_disponibles = []
        for actividad in seleccion_inicial:
            existen_grupos = Grupo.buscar_grupo(fecha, actividad, self.reserva.get_idiomas()[0], self.reserva.get_clientes())
            if existen_grupos:
                actividades_disponibles.append(actividad)
            else:
                guias_capacitados = actividad.buscar_guia(self.reserva.get_idiomas()[0])
                guias_con_disponibilidad = Guia.buscar_disponibilidad(guias_capacitados, fecha)
                if guias_con_disponibilidad:
                    actividades_disponibles.append(actividad)
        return actividades_disponibles

    def escoger_actividades_dia(self, actividades_posibles: List['Actividad'], actividad_escogida: List[str], fecha: List[int]):
        for nombre in actividad_escogida:
            for actividad in actividades_posibles:
                if actividad.get_nombre() == nombre:
                    self.actividades.append(actividad)
                    existen_grupos = Grupo.buscar_grupo(fecha, actividad, self.reserva.get_idiomas()[0], self.reserva.get_clientes())
                    if existen_grupos:
                        existen_grupos[0].get_lista_reservas().append(self.reserva.get_clientes())
                        self.grupos.append(existen_grupos[0])
                    else:
                        grupo = Grupo(actividad, self.reserva.get_clientes(), fecha, self.reserva.get_idiomas()[0])
                        self.grupos.append(grupo)
        self.asignar_precio()

    def escoger_actividades_dia_paquete(self, actividades_posibles: List['Actividad'], actividad_escogida: List[str], fecha: List[int]):
        for nombre in actividad_escogida:
            for actividad in actividades_posibles:
                if actividad.get_nombre() == nombre:
                    grupo = Grupo(actividad, self.reserva.get_clientes(), fecha, self.reserva.get_idiomas()[0])
                    self.grupos.append(grupo)
        self.asignar_precio()

    @staticmethod
    def paquetes_disponibles(cantidad_personas: int, destino: 'Destino', clasificacion: int, fechas: List[List[int]]) -> List['Plan']:
        paquetes_posibles = []
        for plan in Plan.paquetes:
            fechas_disponibles = []
            for fecha in fechas:
                if plan.get_destino() == destino and plan.get_clasificacion() <= clasificacion and len(plan.get_actividades()) >= len(fechas):
                    for actividad in plan.get_actividades():
                        existen_grupos = Grupo.buscar_grupo(fecha, actividad, plan.get_reserva().get_idiomas()[0], cantidad_personas)
                        if existen_grupos:
                            fechas_disponibles.append(fecha)
            if len(fechas_disponibles) == len(fechas):
                paquetes_posibles.append(plan)
        return paquetes_posibles

    @staticmethod
    def asignar_tipo(valor: int) -> str:
        if valor == 1:
            return "PP"
        elif valor == 2:
            return "PT"
        return ""

    def asignar_precio(self):
        self.precio = sum(actividad.get_precio() for actividad in self.get_actividades())

    @staticmethod
    def string_paquete_turistico(plan: 'Plan') -> str:
        paquete = f"Destino: {plan.get_destino().get_nombre()}\n"
        paquete += "Actividades: " + ", ".join(actividad.get_nombre() for actividad in plan.get_actividades()) + "\n"
        paquete += f"Precio por persona: {plan.get_precio()}\n"
        return paquete

    # Métodos de acceso
    @staticmethod
    def get_paquetes() -> List['Plan']:
        return Plan.paquetes

    @staticmethod
    def set_paquetes(paquetes: List['Plan']):
        Plan.paquetes = paquetes

    def get_tipo(self) -> str:
        return self.tipo

    def set_tipo(self, tipo: str):
        self.tipo = tipo

    def get_destino(self) -> 'Destino':
        return self.destino

    def set_destino(self, destino: 'Destino'):
        self.destino = destino

    def get_actividades(self) -> List['Actividad']:
        return self.actividades

    def set_actividades(self, actividades: List['Actividad']):
        self.actividades = actividades

    def get_precio(self) -> float:
        return self.precio

    def set_precio(self, precio: float):
        self.precio = precio

    def get_clasificacion(self) -> int:
        return self.clasificacion

    def set_clasificacion(self, clasificacion: int):
        self.clasificacion = clasificacion

    def get_grupos(self) -> List['Grupo']:
        return self.grupos

    def set_grupos(self, grupos: List['Grupo']):
        self.grupos = grupos

    def get_reserva(self) -> 'Reserva':
        return self.reserva

    def set_reserva(self, reserva: 'Reserva'):
        self.reserva = reserva 