class Suscripcion:
    _lista_clientes = []
    _lista_tipos = ["Básica", "General", "Premium", "VIP"]

    def __init__(self, tipo=None, vencimiento=None, capacidad=0, precio=0, desc_restaurante_gratis=0, desc_tour=0.0, desc_hotel=0.0, titular=None, fechas=None):
        self._tipo = tipo
        self._fecha_vencimiento = vencimiento
        self._capacidad = capacidad
        self._precio = precio
        self._desc_restaurante_gratis = desc_restaurante_gratis
        self._desc_tour = desc_tour
        self._desc_hotel = desc_hotel
        
        if titular:
            Suscripcion._lista_clientes.append(titular)
            if fechas:
                self.asignar_precio()
                self.asignar_descuentos()
                self.asignar_capacidad()
                self.asignar_fecha_vencimiento(fechas)
                titular.set_suscripcion(self)

    @staticmethod
    def ultima_fecha_reserva(fechas):
        return fechas[-1]

    @staticmethod
    def verificar_suscripcion(nombre, edad, lista_fechas):
        for i, cliente in enumerate(Suscripcion._lista_clientes):
            if cliente.get_nombre() == nombre:
                if cliente.get_suscripcion().verificar_fecha_vencimiento(Suscripcion.ultima_fecha_reserva(lista_fechas)):
                    cliente.set_edad(edad)
                    return cliente
                else:
                    Suscripcion._lista_clientes.pop(i)
                    return None
        return None

    def asignar_precio(self):
        if self._tipo == "Básica":
            self._precio = 100000
        elif self._tipo == "General":
            self._precio = 200000
        elif self._tipo == "Premium":
            self._precio = 300000
        elif self._tipo == "VIP":
            self._precio = 400000

    @staticmethod
    def precio_por_tipo(tipo):
        if tipo == "Básica":
            return 100000
        elif tipo == "General":
            return 200000
        elif tipo == "Premium":
            return 300000
        elif tipo == "VIP":
            return 400000
        return 0

    def asignar_descuentos(self):
        if self._tipo == "Básica":
            self._desc_restaurante_gratis = 0
            self._desc_tour = 0.15
            self._desc_hotel = 0.15
        elif self._tipo == "General":
            self._desc_restaurante_gratis = 0
            self._desc_tour = 0.2
            self._desc_hotel = 0.2
        elif self._tipo == "Premium":
            self._desc_restaurante_gratis = 1
            self._desc_tour = 0.35
            self._desc_hotel = 0.35
        elif self._tipo == "VIP":
            self._desc_restaurante_gratis = 2
            self._desc_tour = 0.5
            self._desc_hotel = 0.5

    @staticmethod
    def descuentos_por_tipo(tipo):
        if tipo == "Básica":
            return [0, 0.15, 0.15]
        elif tipo == "General":
            return [0, 0.2, 0.2]
        elif tipo == "Premium":
            return [1, 0.35, 0.35]
        elif tipo == "VIP":
            return [2, 0.5, 0.5]
        return [0, 0, 0]

    def asignar_capacidad(self):
        if self._tipo == "Básica":
            self._capacidad = 1
        elif self._tipo == "General":
            self._capacidad = 2
        elif self._tipo == "Premium":
            self._capacidad = 4
        elif self._tipo == "VIP":
            self._capacidad = 8

    @staticmethod
    def capacidad_por_tipo(tipo):
        if tipo == "Básica":
            return 1
        elif tipo == "General":
            return 2
        elif tipo == "Premium":
            return 4
        elif tipo == "VIP":
            return 8
        return 0

    def asignar_fecha_vencimiento(self, fechas):
        ultima_fecha = Suscripcion.ultima_fecha_reserva(fechas)
        self._fecha_vencimiento = [ultima_fecha[0], ultima_fecha[1], ultima_fecha[2] + 2]

    @staticmethod
    def mostrar_posibles_suscripciones():
        posibles_suscripciones = []
        for tipo in Suscripcion._lista_tipos:
            texto = f"Tipo: {tipo}\nPrecio: {Suscripcion.precio_por_tipo(tipo)}\nDescuentos: {Suscripcion.descuentos_por_tipo(tipo)}\nCapacidad: {Suscripcion.capacidad_por_tipo(tipo)}"
            posibles_suscripciones.append(texto)
        return posibles_suscripciones

    def verificar_fecha_vencimiento(self, ultima_fecha):
        if self._fecha_vencimiento[2] < ultima_fecha[2]:
            return False
        elif self._fecha_vencimiento[1] < ultima_fecha[1]:
            return False
        elif self._fecha_vencimiento[0] < ultima_fecha[0]:
            return False
        return True

    # Métodos de acceso (getters y setters)
    @staticmethod
    def set_lista_clientes(lista_clientes):
        Suscripcion._lista_clientes = lista_clientes

    def set_tipo(self, tipo):
        self._tipo = tipo

    def set_vencimiento(self, vencimiento):
        self._fecha_vencimiento = vencimiento

    def set_capacidad(self, capacidad):
        self._capacidad = capacidad

    def set_precio(self, precio):
        self._precio = precio

    def set_desc_restaurante_gratis(self, desc_restaurante_gratis):
        self._desc_restaurante_gratis = desc_restaurante_gratis

    def set_desc_tour(self, desc_tour):
        self._desc_tour = desc_tour

    def set_desc_hotel(self, desc_hotel):
        self._desc_hotel = desc_hotel

    @staticmethod
    def get_lista_clientes():
        return Suscripcion._lista_clientes

    @staticmethod
    def get_lista_tipos():
        return Suscripcion._lista_tipos

    def get_tipo(self):
        return self._tipo

    def get_vencimiento(self):
        return self._fecha_vencimiento

    def get_capacidad(self):
        return self._capacidad

    def get_precio(self):
        return self._precio

    def get_desc_restaurante_gratis(self):
        return self._desc_restaurante_gratis

    def get_desc_tour(self):
        return self._desc_tour

    def get_desc_hotel(self):
        return self._desc_hotel
