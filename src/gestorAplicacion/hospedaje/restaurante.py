import pickle
from typing import List, Dict
from gestorAplicacion.gestionHum import Cliente
from gestorAplicacion.manejoReserva import Destino, Grupo, Reserva
import uiMain as Main


class Restaurante:

    def __init__(self, nombre: str, grupos: List[Grupo]):
        self.permiteSuscripcion = False
        self.nombre = nombre
        self.hotel = None
        self.precio = 0.0
        self.grupos = grupos
        self.numeroMesas: Dict[int, Grupo] = {}
        self.mesasDisponibles: Dict[int, Grupo] = {}

    @staticmethod
    def asignarRestaurante(reserva: Reserva):
        hotel = reserva.getClientes()[0].getHotel()
        restaurantes = hotel.getRestaurantes()

        listaOpcionesRestaurantes = [restaurante.getNombre() for restaurante in restaurantes]

        indiceRestauranteEscogido = Main.ingresarOpcion("Seleccione el restaurante que desea: ", 0, listaOpcionesRestaurantes)
        indiceRestauranteEscogidoInt = int(indiceRestauranteEscogido) - 1

        print("Hotel escogido: " + restaurantes[indiceRestauranteEscogidoInt].getNombre())

        for cliente in reserva.getClientes():
            cliente.setRestaurantes(restaurantes[indiceRestauranteEscogidoInt])

        return restaurantes[indiceRestauranteEscogidoInt]

    @staticmethod
    def asignarMesaRestaurante(reserva: Reserva, restaurante):
        grupos = restaurante.getGrupos()
        listaOpciones = [grupo.getTipoMesa() for grupo in grupos]

        mesasAsignadas = False
        mesasEscogidasArray = ["" for _ in range(3)]
        totalMesas = 0
        capacidadMesasSeleccionada = 0

        while not mesasAsignadas:
            mensaje = "Seleccione el número de mesas de cada tipo [Sencilla, Doble, Gran mesa]: "
            mesasEscogidas = Main.ingresarOpcion(mensaje, 3, listaOpciones)
            mesasEscogidasArray = mesasEscogidas.split(" ")
            totalMesas = int(mesasEscogidasArray[0]) + int(mesasEscogidasArray[1]) + int(mesasEscogidasArray[2])
            capacidadMesasSeleccionada = 2 * int(mesasEscogidasArray[0]) + 4 * int(mesasEscogidasArray[1]) + 12 * int(mesasEscogidasArray[2])

            if totalMesas > Hotel.numeroDeAdultos(reserva.getClientes()):
                totalMesas = 0
            elif totalMesas == 0:
                pass
            elif capacidadMesasSeleccionada < len(reserva.getClientes()):
                totalMesas = 0
            else:
                mesasAsignadas = True

        for cliente in reserva.getClientes():
            cliente.setMesaRestaurante(grupos[int(mesasEscogidasArray[0]) - 1])

    def numeroDeMesasDisponibles(self, reserva: Reserva):
        numeroDeMesas = 0
        for grupo in self.grupos:
            if grupo.getTipoMesa() == "Sencilla":
                numeroDeMesas += 2
            elif grupo.getTipoMesa() == "Doble":
                numeroDeMesas += 4
            elif grupo.getTipoMesa() == "Gran mesa":
                numeroDeMesas += 12
        return numeroDeMesas

    # Métodos de acceso
    def isPermiteSuscripcion(self):
        return self.permiteSuscripcion

    def setPermiteSuscripcion(self, permiteSuscripcion: bool):
        self.permiteSuscripcion = permiteSuscripcion

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getHotel(self):
        return self.hotel

    def setHotel(self, hotel: Destino):
        self.hotel = hotel

    def getPrecio(self):
        return self.precio

    def setPrecio(self, precio: float):
        self.precio = precio

    def getGrupos(self):
        return self.grupos

    def setGrupos(self, grupos: List[Grupo]):
        self.grupos = grupos

    def getNumeroMesas(self):
        return self.numeroMesas

    def setNumeroMesas(self, numeroMesas: Dict[int, Grupo]):
        self.numeroMesas = numeroMesas



if __name__ == "__main__":
    hoteles = Hotel.cargarHoteles()

    reserva = Reserva()

    cliente1 = Cliente("juan", 19)
    cliente2 = Cliente("pepe", 20)

    cliente1.setHotel(hoteles[0])

    reserva.setClientes([cliente1, cliente2])

    print("Clientes: " + str(reserva.getClientes()))
    reserva.getClientes()[0].setHotel(hoteles[0])

    hotel1 = reserva.getClientes()[0].getHotel()

    mesa1 = Grupo(2, "Sencilla")
    mesa2 = Grupo(4, "Doble")
    mesa3 = Grupo(12, "Gran mesa")

    grupos1 = [mesa1, mesa2, mesa3]

    restaurante = Restaurante("Asiatico", grupos1)
    restaurante.setGrupos(grupos1)
    restaurante2 = Restaurante("Italiano", grupos1)
    restaurante2.setGrupos(grupos1)

    hotel1.setRestaurantes([restaurante, restaurante2])

    print(reserva.getClientes()[0].getHotel().getNombre())
    print("Restaurantes: " + hotel1.getRestaurantes()[0].getNombre())

    Restaurante.asignarMesaRestaurante(reserva, restaurante)