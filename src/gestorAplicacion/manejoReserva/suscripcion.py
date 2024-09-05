from typing import List, Dict

class Suscripcion:
    lista_clientes: List[Cliente] = []
    LISTA_TIPOS: List[str] = ["Básica", "General", "Premium", "VIP"]

    def __init__(self, tipo: str, vencimiento: List[int], capacidad: int, precio: float, desc_restaurante_gratis: int, desc_tour: float, desc_hotel: float):
        self.tipo = tipo
        self.fecha_vencimiento = vencimiento
        self.capacidad = capacidad
        self.precio = precio
        self.desc_restaurante_gratis = desc_restaurante_gratis
        self.desc_tour = desc_tour
        self.desc_hotel = desc_hotel

    def __init__(self, tipo: str, vencimiento: List[int], capacidad: int, precio: float, titular: 'Cliente'):
        self.tipo = tipo
        self.fecha_vencimiento = vencimiento
        self.capacidad = capacidad
        self.precio = precio
        Suscripcion.lista_clientes.append(titular)
        # Falta asignar la suscripción al cliente

    def __init__(self, tipo: str, fechas: Dict[str, List[int]], titular: 'Cliente'):
        self.tipo = tipo
        self.asignar_precio()
        self.asignar_descuentos()
        self.asignar_capacidad()
        self.asignar_fecha_vencimiento(fechas)
        Suscripcion.lista_clientes.append(titular)
        titular.set_suscripcion(self)

    @staticmethod
    def ultima_fecha_reserva(fechas: Dict[str, List[int]]) -> List[int]:
        return list(fechas.values())[-1]

    @staticmethod
    def verificar_suscripcion(nombre: str, edad: int, lista_fechas: Dict[str, List[int]]) -> 'Cliente':
        for cliente in Suscripcion.lista_clientes:
            if cliente.get_nombre() == nombre:
                if cliente.get_suscripcion().verificar_fecha_vencimiento(Suscripcion.ultima_fecha_reserva(lista_fechas)):
                    cliente.set_edad(edad)
                    return cliente
                else:
                    Suscripcion.lista_clientes.remove(cliente)
                    return None
            else:
                return None
        return None

    def asignar_precio(self):
        if self.tipo == "Básica":
            self.precio = 100000
        elif self.tipo == "General":
            self.precio = 200000
        elif self.tipo == "Premium":
            self.precio = 300000
        elif self.tipo == "VIP":
            self.precio = 400000

    @staticmethod
    def precio_por_tipo(tipo: str) -> float:
        if tipo == "Básica":
            return 100000
        elif tipo == "General":
            return 200000
        elif tipo == "Premium":
            return 300000
        elif tipo == "VIP":
            return 400000
        else:
            return 0

    def asignar_descuentos(self):
        if self.tipo == "Básica":
            self.desc_restaurante_gratis = 0
            self.desc_tour = 0.15
            self.desc_hotel = 0.15
        elif self.tipo == "General":
            self.desc_restaurante_gratis = 0
            self.desc_tour = 0.2
            self.desc_hotel = 0.2
        elif self.tipo == "Premium":
            self.desc_restaurante_gratis = 1
            self.desc_tour = 0.35
            self.desc_hotel = 0.35
        elif self.tipo == "VIP":
            self.desc_restaurante_gratis = 2
            self.desc_tour = 0.5
            self.desc_hotel = 0.5

    @staticmethod
    def descuentos_por_tipo(tipo: str) -> List[float]:
        if tipo == "Básica":
            return [0.0, 0.15, 0.15]
        elif tipo == "General":
            return [0.0, 0.2, 0.2]
        elif tipo == "Premium":
            return [1.0, 0.35, 0.35]
        elif tipo == "VIP":
            return [2.0, 0.5, 0.5]
        else:
            return [0.0, 0.0, 0.0]

    def asignar_capacidad(self):
        if self.tipo == "Básica":
            self.capacidad = 1
        elif self.tipo == "General":
            self.capacidad = 2
        elif self.tipo == "Premium":
            self.capacidad = 4
        elif self.tipo == "VIP":
            self.capacidad = 8

    @staticmethod
    def capacidad_por_tipo(tipo: str) -> int:
        if tipo == "Básica":
            return 1
        elif tipo == "General":
            return 2
        elif tipo == "Premium":
            return 4
        elif tipo == "VIP":
            return 8
        else:
            return 0

    def asignar_fecha_vencimiento(self, fechas: Dict[str, List[int]]):
        ultima_fecha = Suscripcion.ultima_fecha_reserva(fechas)
        self.fecha_vencimiento = [ultima_fecha[0], ultima_fecha[1], ultima_fecha[2] + 2]

    @staticmethod
    def mostrar_posibles_suscripciones() -> List[str]:
        posibles_suscripciones = []
        for tipo in Suscripcion.LISTA_TIPOS:
            texto = f"Tipo: {tipo}\n Precio: {Suscripcion.precio_por_tipo(tipo)}\n Descuentos: {Suscripcion.descuentos_por_tipo(tipo)}\n Capacidad: {Suscripcion.capacidad_por_tipo(tipo)}"
            posibles_suscripciones.append(texto)
        return posibles_suscripciones

    def verificar_fecha_vencimiento(self, ultima_fecha: List[int]) -> bool:
        if self.fecha_vencimiento[2] < ultima_fecha[2]:
            return False
        elif self.fecha_vencimiento[1] < ultima_fecha[1]:
            return False
        elif self.fecha_vencimiento[0] < ultima_fecha[0]:
            return False
        else:
            return True

    # Métodos de acceso
    @staticmethod
    def set_lista_clientes(lista_clientes: List['Cliente']):
        Suscripcion.lista_clientes = lista_clientes

    def set_tipo(self, tipo: str):
        self.tipo = tipo

    def set_vencimiento(self, vencimiento: List[int]):
        self.fecha_vencimiento = vencimiento

    def set_capacidad(self, capacidad: int):
        self.capacidad = capacidad

    def set_precio(self, precio: float):
        self.precio = precio

    def set_desc_restaurante_gratis(self, desc_restaurante_gratis: int):
        self.desc_restaurante_gratis = desc_restaurante_gratis

    def set_desc_tour(self, desc_tour: float):
        self.desc_tour = desc_tour

    def set_desc_hotel(self, desc_hotel: float):
        self.desc_hotel = desc_hotel

    @staticmethod
    def get_lista_clientes() -> List['Cliente']:
        return Suscripcion.lista_clientes

    @staticmethod
    def get_lista_tipos() -> List[str]:
        return Suscripcion.LISTA_TIPOS

    def get_tipo(self) -> str:
        return self.tipo

    def get_vencimiento(self) -> List[int]:
        return self.fecha_vencimiento

    def get_capacidad(self) -> int:
        return self.capacidad

    def get_precio(self) -> float:
        return self.precio

    def get_desc_restaurante_gratis(self) -> int:
        return self.desc_restaurante_gratis

    def get_desc_tour(self) -> float:
        return self.desc_tour

    def get_desc_hotel(self) -> float:
        return self.desc_hotel