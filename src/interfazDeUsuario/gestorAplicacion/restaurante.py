from multimethod import multimethod

class Restaurante:
    def __init__(self, nombre, destino,reservas=[], mesas=[], precio=0.0, permite_suscripcion=False):
        self._nombre = nombre
        self._reservas = reservas
        self._precio = precio
        self._permite_suscripcion = permite_suscripcion
        self._destino=destino
        self._mesas=mesas


    @staticmethod
    def mostrar_nombres(restaurantes_lista):
        return [restaurante.get_nombre() for restaurante in restaurantes_lista]

    @staticmethod
    def promedio_precio(restaurantes_lista):
        if not restaurantes_lista:
            return 0.0
        return sum(restaurante.get_precio() for restaurante in restaurantes_lista) / len(restaurantes_lista)

    @staticmethod
    def asignar_restaurante(reserva, indice_restaurante_escogido):
        hotel = reserva.get_clientes()[0].get_hotel()
        restaurantes = hotel.get_restaurantes()

        restaurante_escogido = restaurantes[indice_restaurante_escogido - 1]

        for cliente in reserva.get_clientes():
            cliente.set_restaurantes(restaurante_escogido)

        return restaurante_escogido

    @staticmethod
    def asignar_mesa_restaurante(reserva, restaurante, mesas_escogidas):
        grupos = restaurante.get_grupos()

        capacidad_mesas_seleccionada = 2 * int(mesas_escogidas[0]) + 4 * int(mesas_escogidas[1]) + 12 * int(mesas_escogidas[2])

        for cliente in reserva.get_clientes():
            cliente.set_mesa_restaurante(grupos[int(mesas_escogidas[0]) - 1])

    def numero_de_mesas_disponibles(self, reserva):
        numero_de_mesas = 0
        for grupo in self._grupos:
            if grupo.get_tipo_mesa() == "Sencilla":
                numero_de_mesas += 2
            elif grupo.get_tipo_mesa() == "Doble":
                numero_de_mesas += 4
            elif grupo.get_tipo_mesa() == "Gran mesa":
                numero_de_mesas += 12
        return numero_de_mesas

    @staticmethod
    def calcular_precio(reserva):
        if reserva.get_clientes()[0].get_suscripcion() and reserva.get_clientes()[0].get_suscripcion().get_desc_restaurante_gratis() != 0.0:
            return 0.0
        return sum(reserva.get_clientes()[0].get_hotel().get_restaurantes()[0].get_precio() for _ in reserva.get_clientes())

     # Métodos de acceso
    def getPermiteSuscripcion(self):
        return self._permite_suscripcion

    def setPermiteSuscripcion(self, permite_suscripcion):
        self._permite_suscripcion = permite_suscripcion

    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def getReserservas(self):
        return self._reservas
    
    def setReservas(self,reservas):
        self._reservas=reservas

    def getPrecio(self):
        return self._precio

    def setPrecio(self, precio):
        self._precio = precio

    def getDestino(self):
        return self._destino
    
    def setDestino(self,destino):
        self._destino=destino
