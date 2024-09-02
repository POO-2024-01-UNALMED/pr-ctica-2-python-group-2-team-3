import pickle
import sys

class Hotel:
    def __init__(self):
        self.permiteSuscripcion = False
        self.nombre = ""
        self.destino = None
        self.numeroHabitaciones = 0
        self.precio = 0.0
        self.cuentaConSuscripcion = False
        self.precioFinalHospedaje = 0.0
        self.grupos = []
        self.disponibilidadHabitaciones = {}
        self.restaurantes = []

    @staticmethod
    def mostrarHotelesDisponibles(reserva):
        hotelesEnDestino = Hotel.hotelesEnDestino(reserva, Hotel.cargarHoteles())
        hotelesDisponibles = Hotel.verificarDisponibilidadHotel(reserva, hotelesEnDestino)

        hotelesADesplegar = []
        for hotel in hotelesDisponibles:
            info = (
                f"{hotel.nombre}\n"
                f" Habitaciones para fechas: {hotel.disponibilidadHabitaciones.get(reserva.fechas[0])}\n"
                f" Precio Base: {hotel.precio}\n"
                f" Cuenta con posibilidad de descuento: {'Sí' if Hotel.hotelConSuscripcion(hotel, reserva) else 'No'}"
            )
            hotelesADesplegar.append(info)
        return hotelesADesplegar
    
    @staticmethod
    def buscarHotelLista(reserva, opcElegida):
        hotelesEnDestino = Hotel.hotelesEnDestino(reserva, Hotel.cargarHoteles())
        hotelesDisponibles = Hotel.verificarDisponibilidadHotel(reserva, hotelesEnDestino)
        hotel = hotelesDisponibles[int(opcElegida) - 1]
        return hotel

    @staticmethod
    def cantidadHotelesDestino(destino):
        cantidadHoteles = 0
        for hotel in Hotel.cargarHoteles():
            if hotel.destino == destino:
                cantidadHoteles += 1
        return cantidadHoteles

    @staticmethod
    def promedioPreciosActividades(destino):
        promedio = 0
        cantidad = Hotel.cantidadHotelesDestino(destino)
        
        if cantidad == 0:
            return 0
        
        for hotel in Hotel.cargarHoteles():
            if hotel.destino == destino:
                promedio += hotel.precio

        return promedio // cantidad
    
    @staticmethod
    def cargarHoteles():
        hoteles = []
        try:
            with open("src/baseDatos/listaHoteles.pkl", "rb") as fileInputStream:
                hoteles = pickle.load(fileInputStream)
        except (IOError, pickle.PickleError) as e:
            print(e)
        return hoteles
    

    ########################## Asignar Habitacion ##########################


    Hoteles = cargarHoteles()

    @staticmethod
    def hotelesEnDestino(reserva, hoteles):
        reserva.getDestino()
        hotelesEnDestino = []

        for hotel in hoteles:
            if hotel.getDestino().getNombre().upper() == reserva.getDestino().getNombre().upper():
                hotelesEnDestino.append(hotel)

        return hotelesEnDestino

    @staticmethod
    def verificarDisponibilidadHotel(reserva, hotelesEnDestino):
        hotelesDisponibles = []
        totalClientes = len(reserva.getClientes())
        adultos = 0

        # Contar el número de adultos en la reserva
        for cliente in reserva.getClientes():
            if cliente.getEdad() >= 18:
                adultos += 1

        if adultos < 1:
            return hotelesDisponibles  # Retornar lista vacía si no hay adultos.

        fechasReserva = reserva.getFechas()

        for hotel in hotelesEnDestino:
            hotelDisponible = True

            for fecha in fechasReserva:
                habitacionesDisponibles = hotel.getDisponibilidadHabitaciones().get(tuple(fecha))

                if habitacionesDisponibles is None:
                    hotelDisponible = False  # Si no hay habitaciones disponibles para la fecha, el hotel no está disponible.
                    break

                capacidadTotal = 0

                # Calcular la capacidad total disponible para la fecha específica
                for habitacion in habitacionesDisponibles:
                    disponibles = habitacion[1]
                    capacidad = habitacion[2]

                    capacidadTotal += disponibles * capacidad

                if capacidadTotal < totalClientes:
                    hotelDisponible = False
                    break

            if hotelDisponible:
                hotelesDisponibles.append(hotel)

        return hotelesDisponibles
    

    @staticmethod
    def hotelConSuscripcion(hotel, reserva):
        hotelesConSuscripcion = []

        if reserva.getExisteSuscripcion():
            if hotel.permiteSuscripcion:
                hotelesConSuscripcion.append(hotel)
                return True

        return False

    @staticmethod
    def asignarHotel(reserva, listaHoteles):
        hotelesEnDestino = Hotel.hotelesEnDestino(reserva, listaHoteles)
        hotelesDisponibles = Hotel.verificarDisponibilidadHotel(reserva, hotelesEnDestino)

        if not hotelesDisponibles:
            return None

        hotelesADesplegar = []

        # Agrega los hoteles disponibles y su información para que el Cliente Decida
        for hotel in hotelesDisponibles:
            hotelesADesplegar.append(
                f"{hotel.getNombre()}"
                f"\n Habitaciones para fechas: {hotel.getDisponibilidadHabitaciones().get(tuple(reserva.getFechas()[0]))}"
                f"\n Precio Base: {hotel.getPrecio()}"
                f"\n Cuenta con posibilidad de descuento: {'Sí' if Hotel.hotelConSuscripcion(hotel, reserva) else 'No'}"
            )

        indiceHotelEscogido = Main.ingresarOpcion("Seleccione el hotel en el cual se desea hospedar", 0, hotelesADesplegar)
        indiceHotelEscogidoInt = int(indiceHotelEscogido) - 1

        for cliente in reserva.getClientes():
            cliente.setHotel(hotelesDisponibles[indiceHotelEscogidoInt])

        return hotelesDisponibles[indiceHotelEscogidoInt]
    

    @staticmethod
    def numeroDeAdultos(clientes):
        adultos = 0
        for cliente in clientes:
            if cliente.getEdad() >= 18:
                adultos += 1
        return adultos

    @staticmethod
    def asignarHabitacion(reserva, hotel):
        listaHoteles = Hotel.cargarHoteles()
        
        if hotel.permiteSuscripcion and reserva.getExisteSuscripcion():
            hotel.cuentaConSuscripcion = True

        listaString = []
        listaHabitacionesClientes = []

        # Verificar si las fechas de la reserva son nulas
        if reserva.getFechas() is None:
            raise ValueError("Las fechas de la reserva no pueden ser nulas.")

        # Mostrar la disponibilidad de habitaciones en el hotel
        for habitacion in hotel.getDisponibilidadHabitaciones().get(tuple(reserva.getFechas()[0]), []):
            tipoHabitacion = habitacion[0]
            disponibles = habitacion[1]
            capacidad = habitacion[2]
            listaString.append(f"{tipoHabitacion} - Disponibles: {disponibles} - Capacidad: {capacidad}")
            # Inicializar la lista de clientes para cada habitación
            listaHabitacionesClientes.append([])

        totalHabitaciones = 0
        habitacionesEscogidasArray = ["0", "0", "0"]
        habitacionesAsignadas = False

        while not habitacionesAsignadas:
            mensaje = "Por favor seleccione las habitaciones que desea de cada tipo, de la siguiente forma [Num sencilla, Num Doble, Num suites]"
            habitacionesEscogidas = Main.ingresarOpcion(mensaje, 3, listaString)
            habitacionesEscogidasArray = habitacionesEscogidas.split(" ")
            # [Número de sencillas, Número de dobles, Número de suites]
            totalHabitaciones = int(habitacionesEscogidasArray[0]) + \
                                 int(habitacionesEscogidasArray[1]) + \
                                 int(habitacionesEscogidasArray[2])
            capacidadHabitacionesSeleccionada = 2 * int(habitacionesEscogidasArray[0]) + \
                                                   4 * int(habitacionesEscogidasArray[1]) + \
                                                   8 * int(habitacionesEscogidasArray[2])

            # Verificar si hay suficiente capacidad para cada tipo de habitación
            capacidadSuficiente = True
            for i in range(len(listaString)):
                partes = listaString[i].split(" - ")
                tipoHabitacion = partes[0]
                disponibles = int(partes[1].split(": ")[1])
                seleccionadas = int(habitacionesEscogidasArray[i])

                if seleccionadas > disponibles:
                    capacidadSuficiente = False
                    break

            if not capacidadSuficiente:
                continue

            if totalHabitaciones > Hotel.numeroDeAdultos(reserva.getClientes()):
                totalHabitaciones = 0
            elif totalHabitaciones == 0:
                pass
            elif capacidadHabitacionesSeleccionada < len(reserva.getClientes()):
                totalHabitaciones = 0
            else:
                habitacionesAsignadas = True

        listaHabitacionesIndividuales = []
        capacidadHabitaciones = []
        hayAdultoEnHabitacion = []  # Para verificar si hay un adulto en cada habitación

        # Crear las habitaciones individuales basadas en la selección
        numSencillas = int(habitacionesEscogidasArray[0])
        numDobles = int(habitacionesEscogidasArray[1])
        numSuites = int(habitacionesEscogidasArray[2])

        for _ in range(numSencillas):
            listaHabitacionesIndividuales.append("sencilla")
            capacidadHabitaciones.append(2)
            hayAdultoEnHabitacion.append(False)  # Inicialmente no hay adultos en ninguna habitación
        for _ in range(numDobles):
            listaHabitacionesIndividuales.append("doble")
            capacidadHabitaciones.append(4)
            hayAdultoEnHabitacion.append(False)
        for _ in range(numSuites):
            listaHabitacionesIndividuales.append("suite")
            capacidadHabitaciones.append(8)
            hayAdultoEnHabitacion.append(False)

        # Asignar las habitaciones a los clientes
        for i, cliente in enumerate(reserva.getClientes()):
            for j, tipoHabitacion in enumerate(listaHabitacionesIndividuales):
                if tipoHabitacion in listaHabitacionesIndividuales and \
                   len(listaHabitacionesClientes[j]) < capacidadHabitaciones[j]:
                    listaHabitacionesClientes[j].append(cliente)
                    if cliente.getEdad() >= 18:
                        hayAdultoEnHabitacion[j] = True  # Marcar que hay al menos un adulto en esta habitación
                    break

        # Verificar que cada habitación tiene al menos un adulto
        for i in range(len(listaHabitacionesClientes)):
            if not hayAdultoEnHabitacion[i]:
                raise ValueError(f"La habitación de tipo '{listaHabitacionesIndividuales[i]}' necesita al menos un adulto.")

        return listaHabitacionesClientes
    
    @staticmethod
    def hotelesConSuscripcion(hotel, reserva):
        if reserva.getExisteSuscripcion():
            if hotel.permiteSuscripcion:
                return True
        return False

    @staticmethod
    def asignarHotel(reserva, listaHoteles):
        hotelesEnDestino = Hotel.hotelesEnDestino(reserva, listaHoteles)
        hotelesDisponibles = Hotel.verificarDisponibilidadHotel(reserva, hotelesEnDestino)

        if not hotelesDisponibles:
            return None

        hotelesADesplegar = []

        for hotel in hotelesDisponibles:
            hotelesADesplegar.append(
                f"{hotel.getNombre()}"
                f"\n Habitaciones para fechas: {hotel.getDisponibilidadHabitaciones().get(tuple(reserva.getFechas()[0]))}"
                f"\n Precio Base: {hotel.getPrecio()}"
                f"\n Cuenta con posibilidad de descuento: {'Sí' if Hotel.hotelesConSuscripcion(hotel, reserva) else 'No'}"
            )

        indiceHotelEscogido = Main.ingresarOpcion("Seleccione el hotel en el cual se desea hospedar", 0, hotelesADesplegar)
        indiceHotelEscogidoInt = int(indiceHotelEscogido) - 1

        for cliente in reserva.getClientes():
            cliente.setHotel(hotelesDisponibles[indiceHotelEscogidoInt])

        return hotelesDisponibles[indiceHotelEscogidoInt]
    
    @staticmethod
    def numeroDeAdultos(clientes):
        adultos = 0
        for cliente in clientes:
            if cliente.getEdad() >= 18:
                adultos += 1
        return adultos

    @staticmethod
    def asignarHabitacion(reserva, hotel):
        listaHoteles = Hotel.cargarHoteles()
        
        if hotel.permiteSuscripcion and reserva.getExisteSuscripcion():
            hotel.cuentaConSuscripcion = True

        listaString = []
        listaHabitacionesClientes = []

        if reserva.getFechas() is None:
            raise ValueError("Las fechas de la reserva no pueden ser nulas.")

        for habitacion in hotel.getDisponibilidadHabitaciones().get(tuple(reserva.getFechas()[0]), []):
            tipoHabitacion = habitacion[0]
            disponibles = habitacion[1]
            capacidad = habitacion[2]
            listaString.append(f"{tipoHabitacion} - Disponibles: {disponibles} - Capacidad: {capacidad}")
            listaHabitacionesClientes.append([])

        totalHabitaciones = 0
        habitacionesEscogidasArray = ["0", "0", "0"]
        habitacionesAsignadas = False

        while not habitacionesAsignadas:
            mensaje = "Por favor seleccione las habitaciones que desea de cada tipo, de la siguiente forma [Num sencilla, Num Doble, Num suites]"
            habitacionesEscogidas = Main.ingresarOpcion(mensaje, 3, listaString)
            habitacionesEscogidasArray = habitacionesEscogidas.split(" ")
            totalHabitaciones = int(habitacionesEscogidasArray[0]) + \
                                 int(habitacionesEscogidasArray[1]) + \
                                 int(habitacionesEscogidasArray[2])
            capacidadHabitacionesSeleccionada = 2 * int(habitacionesEscogidasArray[0]) + \
                                                   4 * int(habitacionesEscogidasArray[1]) + \
                                                   8 * int(habitacionesEscogidasArray[2])

            capacidadSuficiente = True
            for i in range(len(listaString)):
                partes = listaString[i].split(" - ")
                tipoHabitacion = partes[0]
                disponibles = int(partes[1].split(": ")[1])
                seleccionadas = int(habitacionesEscogidasArray[i])

                if seleccionadas > disponibles:
                    capacidadSuficiente = False
                    break

            if not capacidadSuficiente:
                continue

            if totalHabitaciones > Hotel.numeroDeAdultos(reserva.getClientes()):
                totalHabitaciones = 0
            elif totalHabitaciones == 0:
                pass
            elif capacidadHabitacionesSeleccionada < len(reserva.getClientes()):
                totalHabitaciones = 0
            else:
                habitacionesAsignadas = True

        listaHabitacionesIndividuales = []
        capacidadHabitaciones = []
        hayAdultoEnHabitacion = []

        numSencillas = int(habitacionesEscogidasArray[0])
        numDobles = int(habitacionesEscogidasArray[1])
        numSuites = int(habitacionesEscogidasArray[2])

        for _ in range(numSencillas):
            listaHabitacionesIndividuales.append("sencilla")
            capacidadHabitaciones.append(2)
            hayAdultoEnHabitacion.append(False)
        for _ in range(numDobles):
            listaHabitacionesIndividuales.append("doble")
            capacidadHabitaciones.append(4)
            hayAdultoEnHabitacion.append(False)
        for _ in range(numSuites):
            listaHabitacionesIndividuales.append("suite")
            capacidadHabitaciones.append(8)
            hayAdultoEnHabitacion.append(False)

        for cliente in reserva.getClientes():
            habitacionAsignada = False
            while not habitacionAsignada:
                menu = ""
                for i in range(len(listaHabitacionesIndividuales)):
                    menu += f"{i + 1}. Habitación {i + 1}: {listaHabitacionesIndividuales[i]} - capacidad {capacidadHabitaciones[i]}\n"

                entrada1 = Main.ingresarOpcion(
                    f"Seleccione en qué habitación desea alojar a {cliente.getNombre()} (Digite el número de una única opción):\n{menu}",
                    0, []
                )

                try:
                    indiceHabitacion = int(entrada1) - 1
                    if indiceHabitacion < 0 or indiceHabitacion >= len(listaHabitacionesIndividuales):
                        continue
                except ValueError:
                    continue

                if cliente.getEdad() < 18:
                    if not hayAdultoEnHabitacion[indiceHabitacion]:
                        continue

                if capacidadHabitaciones[indiceHabitacion] > 0:
                    capacidadHabitaciones[indiceHabitacion] -= 1

                    listaHabitacionesClientes[indiceHabitacion].append(cliente)

                    if cliente.getEdad() >= 18:
                        hayAdultoEnHabitacion[indiceHabitacion] = True

                    cliente.setNombre("")

                    habitacionAsignada = True

        for i in range(len(listaHabitacionesIndividuales)):
            tipoHabitacion = listaHabitacionesIndividuales[i]
            habitacionesSeleccionadas = 0
            if tipoHabitacion == "sencilla":
                habitacionesSeleccionadas = numSencillas
            elif tipoHabitacion == "doble":
                habitacionesSeleccionadas = numDobles
            elif tipoHabitacion == "suite":
                habitacionesSeleccionadas = numSuites

            habitacionesDisponibles = hotel.getDisponibilidadHabitaciones().get(tuple(reserva.getFechas()[0]), [])
            for habitacion in habitacionesDisponibles:
                if habitacion[0] == tipoHabitacion:
                    habitacion[1] -= habitacionesSeleccionadas

        for i in range(len(listaHabitacionesIndividuales)):
            clientes = listaHabitacionesClientes[i]
            tipoHabitacion = listaHabitacionesIndividuales[i]
            grupo = Grupo(tipoHabitacion, len(clientes))
            for cliente in clientes:
                cliente.addGrupo(grupo)
                hotel.agregarGrupo(grupo)

        listaHoteles = [h for h in listaHoteles if h.getNombre() != hotel.getNombre()]
        listaHoteles.append(hotel)

        with open("src/baseDatos/listaHoteles.txt", "wb") as fileOutputStream:
            pickle.dump(listaHoteles, fileOutputStream)

        return hotel.getGrupos()
    

    @staticmethod
    def calcularPrecio(reserva):
        hotel = reserva.getClientes()[0].getHotel()
        cliente = reserva.getClientes()[0]
        cantidadClientes = len(reserva.getClientes())
        precioBase = hotel.getPrecio()
        precioTotal = cantidadClientes * precioBase
        
        if hotel.cuentaConSuscripcion:
            precioTotal *= cliente.getSuscripcion().getDescHotel()
        
        precioTotal *= len(reserva.getFechas())
        
        hotel.precioFinalHospedaje = precioTotal
        
        return precioTotal


    ########################## Métodos de acceso ##########################

    def getPermiteSuscripcion(self):
        return self._permiteSuscripcion

    def setPermiteSuscripcion(self, value):
        self._permiteSuscripcion = value

    def getNombre(self):
        return self._nombre

    def setNombre(self, value):
        self._nombre = value

    def getDestino(self):
        return self._destino

    def setDestino(self, value):
        self._destino = value

    def getNumeroHabitaciones(self):
        return self._numeroHabitaciones

    def setNumeroHabitaciones(self, value):
        self._numeroHabitaciones = value

    def getPrecio(self):
        return self._precio

    def setPrecio(self, value):
        self._precio = value

    def getCuentaConSuscripcion(self):
       return self._cuentaConSuscripcion

    def setCuentaConSuscripcion(self, value):
      self._cuentaConSuscripcion = value

    def getPrecioFinalHospedaje(self):
      return self._precioFinalHospedaje

    def setPrecioFinalHospedaje(self, value):
     self._precioFinalHospedaje = value

    def getGrupos(self):
     return self._grupos

    def setGrupos(self, value):
        self._grupos = value

    def getDisponibilidadHabitaciones(self):
        return self._disponibilidadHabitaciones

    def setDisponibilidadHabitaciones(self, value):
     self._disponibilidadHabitaciones = value

    def getRestaurantes(self):
     return self._restaurantes

    def setRestaurantes(self, value):
       self._restaurantes = value

                    
