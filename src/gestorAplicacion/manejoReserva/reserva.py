from typing import List, Dict
import pickle

class Reserva:
    reservas_existentes: List['Reserva'] = []
    ultimo_codigo: int = 0

    def __init__(self, titular: 'Cliente' = None, fechas_viaje: Dict[str, List[int]] = None, idioma: 'Idiomas' = None, destino: 'Destino' = None, clasificacion: int = 0, tipo_plan: str = '', existe_suscripcion: bool = False, plan: 'Plan' = None):
        self.codigo = Reserva.ultimo_codigo + 1
        Reserva.ultimo_codigo += 1
        self.clientes: List['Cliente'] = []
        self.idiomas: List['Idiomas'] = []
        self.fechas: Dict[str, List[int]] = {}
        self.clasificacion = clasificacion
        self.tipo_plan = tipo_plan
        self.existe_suscripcion = existe_suscripcion
        self.plan = plan
        self.its_planeacion = True

        if titular:
            self.clientes.append(titular)
            self.existe_suscripcion = self.tiene_suscripcion()
        if fechas_viaje:
            self.fechas = fechas_viaje
        if idioma:
            self.idiomas.append(idioma)
        if destino:
            self.destino = destino

        Reserva.reservas_existentes.append(self)

    def __str__(self):
        return (f"Estos son los datos de su reserva: \n"
                f"Guarde su código de reserva para poder buscarla después en el sistema. \n"
                f"codigo={self.codigo}\n"
                f"Titular={self.clientes[0]}\n"
                f"Destino={self.destino}\n"
                f"Idiomas={self.idiomas}\n"
                f"Fechas={self.fechas}\n"
                f"Clasificacion={self.clasificacion}\n"
                f"TipoPlan={self.tipo_plan}\n"
                f"Actividades={self.plan.get_actividades()}\n"
                f"Precio={(self.plan.get_precio() * len(self.clientes) - self.plan.get_precio() * self.clientes[0].get_suscripcion().get_desc_tour() * self.clientes[0].get_suscripcion().get_capacidad()) + Hotel.calcular_precio(self)}")

    @staticmethod
    def buscar_reserva(codigo: int) -> 'Reserva':
        for reserva in Reserva.reservas_existentes:
            if reserva.codigo == codigo:
                return reserva
        return None

    def escoger_plan(self, tipo_escogido: str) -> List['Actividad']:
        actividades_posibles = self.destino.actividades_disponibles_destino(self.clasificacion, len(self.clientes))
        if not actividades_posibles or len(self.fechas) >= len(actividades_posibles):
            return None
        self.plan = Plan(tipo_escogido, self)
        return actividades_posibles

    @staticmethod
    def mostrar_dias(cantidad_dias: int, fecha_inicio: List[int]) -> Dict[str, List[int]]:
        dia, mes, año = fecha_inicio
        lista_fechas = {}
        dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        while cantidad_dias > 0:
            dias_mes = dias_por_mes[mes - 1]
            cantidad_restante = cantidad_dias
            for i in range(1, cantidad_dias + 1):
                if dia > dias_mes:
                    break
                lista_fechas[f"{dia}/{mes}/{año}"] = [dia, mes, año]
                dia += 1
                cantidad_restante -= 1

            if cantidad_restante == 0:
                break

            cantidad_dias = cantidad_restante
            dia = 1
            mes += 1
            if mes > 12:
                mes = 1
                año += 1

        return lista_fechas

    @staticmethod
    def verificar_lista(i: int, entrada: str) -> bool:
        if not entrada:
            return False
        numeros = entrada.split()
        for str_num in numeros:
            try:
                num = int(str_num)
                if num < 1 or num > i:
                    return False
            except ValueError:
                return False
        return True

    @staticmethod
    def verificar_numero(max: int, str_num: str) -> bool:
        try:
            num = int(str_num)
            if max == 0:
                return num >= 0
            return 1 <= num <= max
        except ValueError:
            return False

    @staticmethod
    def lista_fecha(fecha_inicio: str) -> List[int]:
        return [int(x) for x in fecha_inicio.split("/")]

    @staticmethod
    def verificar_fecha(fecha: str) -> bool:
        if not fecha:
            return False
        lista_string = fecha.split("/")
        if len(lista_string) == 2:
            return Reserva.verificar_numero(12, lista_string[0])
        elif len(lista_string) == 3:
            return Reserva.verificar_numero(12, lista_string[1])
        return False

    @staticmethod
    def mostrar_lista_fechas(opc_fecha: str, fecha: str) -> Dict[str, List[int]]:
        lista_fechas = {}
        lista_string = fecha.split("/")

        if opc_fecha == "1":
            dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            mes = int(lista_string[0])
            año = int(lista_string[1])
            cantidad_dias = dias_por_mes[mes - 1]
            fecha_inicio = [1, mes, año]
            lista_fechas = Reserva.mostrar_dias(cantidad_dias, fecha_inicio)
        else:
            dia = int(lista_string[0])
            mes = int(lista_string[1])
            año = int(lista_string[2])
            lista_fechas[f"{dia}/{mes}/{año}"] = [dia, mes, año]

        return lista_fechas

    @staticmethod
    def convertir_tipo(lista: object) -> List[str]:
        if isinstance(lista, list) and all(isinstance(item, str) for item in lista):
            return lista
        return None

    @staticmethod
    def convertir_lista_fechas(obj: object) -> Dict[str, List[int]]:
        if isinstance(obj, dict) and all(isinstance(sublist, list) and all(isinstance(item, int) for item in sublist) for sublist in obj.values()):
            return obj
        return None

    @staticmethod
    def mostrar_mes(fecha: int) -> str:
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        return meses[fecha - 1]

    @staticmethod
    def comprobar_es_mes(lista_fechas: Dict[str, List[int]]) -> bool:
        mes = f"{lista_fechas[list(lista_fechas.keys())[0]][1]}/{lista_fechas[list(lista_fechas.keys())[0]][2]}"
        lista_mes = Reserva.mostrar_lista_fechas("1", mes)
        return lista_fechas == lista_mes

    @staticmethod
    def mostrar_fecha_string(fecha: List[int]) -> str:
        return f"[{fecha[0]}/{Reserva.mostrar_mes(fecha[1])}/{fecha[2]}]"

    @staticmethod
    def mostrar_clasificacion_comun(destino: 'Destino') -> int:
        clasificacion_comun = 1
        cantidad_mayor = 0
        for i in range(1, 5):
            cantidad_clasificacion = sum(1 for reserva in Reserva.reservas_existentes if reserva.destino == destino and reserva.clasificacion == i)
            if cantidad_clasificacion > cantidad_mayor:
                cantidad_mayor = cantidad_clasificacion
                clasificacion_comun = i
        return clasificacion_comun

    @staticmethod
    def mostrar_clasificacion_comun_con_fechas(destino: 'Destino', fechas: Dict[str, List[int]], idioma: 'Idiomas') -> int:
        clasificacion_comun = 1
        cantidad_mayor = 0
        for i in range(1, 5):
            cantidad_clasificacion = sum(1 for fecha in fechas.values() for reserva in Reserva.reservas_existentes if reserva.destino == destino and reserva.clasificacion == i and fecha in reserva.fechas.values())
            if cantidad_clasificacion > cantidad_mayor:
                cantidad_mayor = cantidad_clasificacion
                clasificacion_comun = i
        return clasificacion_comun

    @staticmethod
    def mostrar_cantidad_personas_destino(destino: 'Destino') -> int:
        return sum(len(reserva.clientes) for reserva in Reserva.reservas_existentes if reserva.destino == destino)

    @staticmethod
    def mostrar_cantidad_personas_destino_con_fechas(destino: 'Destino', fechas: Dict[str, List[int]]) -> int:
        return sum(len(reserva.clientes) for fecha in fechas.values() for reserva in Reserva.reservas_existentes if reserva.destino == destino and fecha in reserva.fechas.values())

    """ @staticmethod
    def mostrar_cantidad_personas_destino_con_idioma(destino: 'Destino', fechas: Dict[str, List[int]], idioma: 'Idiomas') -> int:
        return sum(len(reserva.clientes) for fecha in fechas.values() for reserva in Reserva.reservas_existentes if reserva.destino == destino and fecha in reserva.fechas.values() and idioma in reserva.idi
                   
                   ###Finalizar la traducción de la clase Reserva
                   """
    @staticmethod
    def mostrar_cantidad_personas_hotel(destino: 'Destino', fechas: Dict[str, List[int]], hotel: 'Hotel') -> int:
        cantidad = 0
        for fecha in fechas.values():
            for reserva in Reserva.reservas_existentes:
                if (reserva.destino == destino and
                        fecha in reserva.fechas.values() and
                        reserva.clientes[0].get_hotel() == hotel):
                    cantidad += len(reserva.clientes)
        return cantidad

    @staticmethod
    def mostrar_cantidad_reservas_hotel(destino: 'Destino', fechas: Dict[str, List[int]], hotel: 'Hotel') -> int:
        cantidad = 0
        for fecha in fechas.values():
            for reserva in Reserva.reservas_existentes:
                if (reserva.destino == destino and
                        fecha in reserva.fechas.values() and
                        reserva.clientes[0].get_hotel() == hotel):
                    cantidad += 1
        return cantidad

    @staticmethod
    def mostrar_cantidad_reservas_actividad(destino: 'Destino', fechas: Dict[str, List[int]], actividad: 'Actividad') -> int:
        cantidad = 0
        for fecha in fechas.values():
            for reserva in Reserva.reservas_existentes:
                if (reserva.destino == destino and
                        fecha in reserva.fechas.values() and
                        actividad in reserva.plan.get_actividades()):
                    cantidad += 1
        return cantidad

    @staticmethod
    def actividad_principal_destino(destino: 'Destino') -> 'Actividad':
        actividad_comun = None
        cantidad_mayor = 0
        for actividad in destino.get_actividades():
            cantidad_personas = 0
            for reserva in Reserva.reservas_existentes:
                if reserva.destino == destino and actividad in reserva.plan.get_actividades():
                    cantidad_personas += 1
            if cantidad_personas > cantidad_mayor:
                cantidad_mayor = cantidad_personas
                actividad_comun = actividad
        return actividad_comun

    def tiene_suscripcion(self) -> bool:
        suscripcion = self.clientes[0].get_suscripcion()
        return suscripcion is not None

    def agregar_idioma(self, idioma: 'Idiomas'):
        self.idiomas.append(idioma)

    def añadir_cliente(self, nombre: str, edad: int):
        cliente = Cliente(nombre, edad)
        self.clientes.append(cliente)

    def aplicar_suscripcion(self, existe_suscripcion: bool) -> str:
        suscripcion = self.clientes[0].get_suscripcion()
        capacidad_suscripcion = suscripcion.get_capacidad()
        for i in range(capacidad_suscripcion):
            self.clientes[i].set_suscripcion(suscripcion)
        if len(self.clientes) > capacidad_suscripcion:
            return f"La cantidad de personas excede la capacidad de la suscripción, por lo que el descuento se aplicará solo a las primeras {capacidad_suscripcion} personas."
        else:
            return "La suscripción se registró de manera exitosa para todos los integrantes de la reserva."

    def menor_edad(self) -> int:
        menor = self.clientes[0].get_edad()
        for cliente in self.clientes:
            if cliente.get_edad() < menor:
                menor = cliente.get_edad()
        return menor

    def asignar_clasificacion(self):
        menor_edad = self.menor_edad()
        if menor_edad < 7:
            self.clasificacion = 1
        elif menor_edad < 15:
            self.clasificacion = 2
        elif menor_edad < 18:
            self.clasificacion = 3
        else:
            self.clasificacion = 4

    # Métodos de acceso
    @staticmethod
    def get_reservas_existentes() -> List['Reserva']:
        return Reserva.reservas_existentes

    @staticmethod
    def set_reservas_existentes(reservas_existentes: List['Reserva']):
        Reserva.reservas_existentes = reservas_existentes

    def get_codigo(self) -> int:
        return self.codigo

    def set_codigo(self, codigo: int):
        self.codigo = codigo

    def get_destino(self) -> 'Destino':
        return self.destino

    def set_destino(self, destino: 'Destino'):
        self.destino = destino

    def get_idiomas(self) -> List['Idiomas']:
        return self.idiomas

    def set_idiomas(self, idiomas: List['Idiomas']):
        self.idiomas = idiomas

    def get_fechas(self) -> Dict[str, List[int]]:
        return self.fechas

    def set_fechas(self, fechas: Dict[str, List[int]]):
        self.fechas = fechas

    def get_clasificacion(self) -> int:
        return self.clasificacion

    def set_clasificacion(self, clasificacion: int):
        self.clasificacion = clasificacion

    def get_tipo_plan(self) -> str:
        return self.tipo_plan

    def set_tipo_plan(self, tipo_plan: str):
        self.tipo_plan = tipo_plan

    def get_existe_suscripcion(self) -> bool:
        return self.existe_suscripcion

    def set_existe_suscripcion(self, existe_suscripcion: bool):
        self.existe_suscripcion = existe_suscripcion

    def get_plan(self) -> 'Plan':
        return self.plan

    def set_plan(self, plan: 'Plan'):
        self.plan = plan

    def set_clientes(self, clientes: List['Cliente']):
        self.clientes = clientes

    def get_clientes(self) -> List['Cliente']:
        return self.clientes

    def añadir_reserva(self):
        Reserva.reservas_existentes.append(self)