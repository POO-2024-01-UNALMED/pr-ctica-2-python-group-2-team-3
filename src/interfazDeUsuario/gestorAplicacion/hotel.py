class Hotel:
    _hoteles_disponibles = []  # Simulación de base de datos en memoria

    def __init__(self):
        self._permite_suscripcion = False
        self._nombre = ""
        self._destino = None
        self._numero_habitaciones = 0
        self._precio = 0.0
        self._cuenta_con_suscripcion = False
        self._precio_final_hospedaje = 0.0
        self._grupos = []
        self._disponibilidad_habitaciones = {}
        self._restaurantes = []

    @staticmethod
    def asignar_habitacion(reserva, hotel, ingresar_opcion=None):
        from gestorAplicacion.grupo import Grupo
        lista_hoteles = Hotel._hoteles_disponibles
        if hotel._permite_suscripcion and reserva.get_existe_suscripcion():
            hotel._cuenta_con_suscripcion = True

        if reserva.get_fechas() is None:
            raise ValueError("Las fechas de la reserva no pueden ser nulas.")

        lista_string = []
        lista_habitaciones_clientes = []
        for habitacion in hotel.get_disponibilidad_habitaciones().get(reserva.get_fechas()[0]):
            tipo_habitacion = habitacion[0]
            disponibles = habitacion[1]
            capacidad = habitacion[2]
            lista_string.append(f"{tipo_habitacion} - Disponibles: {disponibles} - Capacidad: {capacidad}")
            lista_habitaciones_clientes.append([])

        total_habitaciones = 0
        habitaciones_escogidas_array = []
        habitaciones_asignadas = False

        while not habitaciones_asignadas:
            mensaje = "Por favor seleccione las habitaciones que desea de cada tipo, de la siguiente forma [Num sencilla, Num Doble, Num suites]"
            habitaciones_escogidas = ingresar_opcion(mensaje, 3, lista_string)
            habitaciones_escogidas_array = habitaciones_escogidas.split(" ")
            total_habitaciones = sum(map(int, habitaciones_escogidas_array))

            capacidad_habitaciones_seleccionada = (
                2 * int(habitaciones_escogidas_array[0]) +
                4 * int(habitaciones_escogidas_array[1]) +
                8 * int(habitaciones_escogidas_array[2])
            )

            capacidad_suficiente = all(
                int(habitaciones_escogidas_array[i]) <= int(lista_string[i].split(": ")[1].split(" ")[0])
                for i in range(len(lista_string))
            )

            if not capacidad_suficiente:
                continue

            if total_habitaciones > Hotel.numero_de_adultos(reserva.get_clientes()):
                total_habitaciones = 0
            elif total_habitaciones == 0:
                pass
            elif capacidad_habitaciones_seleccionada < len(reserva.get_clientes()):
                total_habitaciones = 0
            else:
                habitaciones_asignadas = True

        lista_habitaciones_individuales = []
        capacidad_habitaciones = []
        hay_adulto_en_habitacion = []

        num_sencillas = int(habitaciones_escogidas_array[0])
        num_dobles = int(habitaciones_escogidas_array[1])
        num_suites = int(habitaciones_escogidas_array[2])

        for _ in range(num_sencillas):
            lista_habitaciones_individuales.append("sencilla")
            capacidad_habitaciones.append(2)
            hay_adulto_en_habitacion.append(False)

        for _ in range(num_dobles):
            lista_habitaciones_individuales.append("doble")
            capacidad_habitaciones.append(4)
            hay_adulto_en_habitacion.append(False)

        for _ in range(num_suites):
            lista_habitaciones_individuales.append("suite")
            capacidad_habitaciones.append(8)
            hay_adulto_en_habitacion.append(False)

        for cliente in reserva.get_clientes():
            habitacion_asignada = False
            while not habitacion_asignada:
                menu = "\n".join([
                    f"{i + 1}. Habitación {i + 1}: {lista_habitaciones_individuales[i]} - capacidad {capacidad_habitaciones[i]}"
                    for i in range(len(lista_habitaciones_individuales))
                ])
                entrada1 = ingresar_opcion(
                    f"Seleccione en qué habitación desea alojar a {cliente.get_nombre()} (Digite el número de una única opción):\n{menu}",
                    0, []
                )

                try:
                    indice_habitacion = int(entrada1) - 1
                    if indice_habitacion < 0 or indice_habitacion >= len(lista_habitaciones_individuales):
                        continue
                except ValueError:
                    continue

                if cliente.get_edad() < 18 and not hay_adulto_en_habitacion[indice_habitacion]:
                    continue

                if capacidad_habitaciones[indice_habitacion] > 0:
                    capacidad_habitaciones[indice_habitacion] -= 1
                    lista_habitaciones_clientes[indice_habitacion].append(cliente)

                    if cliente.get_edad() >= 18:
                        hay_adulto_en_habitacion[indice_habitacion] = True

                    habitacion_asignada = True

        for i in range(len(lista_habitaciones_individuales)):
            tipo_habitacion = lista_habitaciones_individuales[i]
            habitaciones_disponibles = hotel.get_disponibilidad_habitaciones().get(reserva.get_fechas()[0])
            for habitacion in habitaciones_disponibles:
                if habitacion[0] == tipo_habitacion:
                    habitacion[1] -= [num_sencillas, num_dobles, num_suites][i]

        for i in range(len(lista_habitaciones_individuales)):
            clientes = lista_habitaciones_clientes[i]
            tipo_habitacion = lista_habitaciones_individuales[i]
            grupo = Grupo(tipo_habitacion, len(clientes))
            for cliente in clientes:
                cliente.add_grupo(grupo)
                hotel.agregar_grupo(grupo)

        hotel._precio_final_hospedaje = Hotel.calcular_precio(reserva)

        return hotel.get_grupos()


    @staticmethod
    def calcular_precio(reserva):
        from gestorAplicacion.restaurante import Restaurante
        hotel = reserva.get_clientes()[0].get_hotel()
        cliente = reserva.get_clientes()[0]
        cantidad_clientes = len(reserva.get_clientes())
        precio_base = hotel.get_precio()
        precio_total = precio_base * cantidad_clientes

        if hotel._cuenta_con_suscripcion:
            descuento = cliente.get_suscripcion().get_desc_hotel() * cliente.get_suscripcion().get_capacidad()
            precio_total -= precio_total * descuento
            precio_total += hotel.get_restaurantes()[0].get_precio()

        precio_total *= len(reserva.get_fechas())
        precio_total += Restaurante.calcular_precio(reserva) * len(reserva.get_fechas())

        hotel._precio_final_hospedaje = precio_total

        return precio_total

    @staticmethod
    def desplegar_habitaciones_reserva(reserva):
        hotel = reserva.get_clientes()[0].get_hotel()
        grupos = hotel.get_grupos()

        resultado = "Habitaciones asignadas para la reserva:\n"
        for grupo in grupos:
            clientes = grupo.get_clientes()
            if clientes and set(reserva.get_clientes()).issubset(set(clientes)):
                resultado += f"Tipo de habitación: {grupo.get_tipo_habitacion()}\n"
                resultado += "Clientes en esta habitación:\n"
                for cliente in clientes:
                    resultado += f" - {cliente.get_nombre()} (Edad: {cliente.get_edad()})\n"
                resultado += f"Capacidad de la habitación: {grupo.get_capacidad()}\n\n"
        return resultado

    @staticmethod
    def buscar_habitaciones(clientes):
        habitaciones_reservadas = []
        for cliente in clientes:
            if cliente.get_habitacion() not in habitaciones_reservadas:
                habitaciones_reservadas.append(cliente.get_habitacion())
        return habitaciones_reservadas

    def eliminar_reservacion(self, clientes):
        habitaciones_para_eliminar = Hotel.buscar_habitaciones(clientes)
        for habitacion in habitaciones_para_eliminar:
            habitacion = None

    def verificar_eliminar_hospedaje(self, habitaciones_para_verificar, fechas_verificables, clientes_verificables):
        for habitacion in habitaciones_para_verificar:
            if habitacion.get_fecha() not in fechas_verificables:
                return False
        return True

    def añadir_clientes_a_las_habitaciones(self, habitaciones, clientes_para_añadir):
        pass  # Implementar lógica

    def eliminar_clientes_de_las_habitaciones(self, habitaciones, clientes_para_eliminar):
        pass  # Implementar lógica

    # Getters y Setters
    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_destino(self):
        return self._destino

    def set_destino(self, destino):
        self._destino = destino

    def get_numero_habitaciones(self):
        return self._numero_habitaciones

    def set_numero_habitaciones(self, numero_habitaciones):
        self._numero_habitaciones = numero_habitaciones

    def get_precio(self):
        return self._precio

    def set_precio(self, precio):
        self._precio = precio

    def get_disponibilidad_habitaciones(self):
        return self._disponibilidad_habitaciones

    def set_disponibilidad_habitaciones(self, disponibilidad_habitaciones):
        self._disponibilidad_habitaciones = disponibilidad_habitaciones

    def get_grupos(self):
        return self._grupos

    def set_grupos(self, grupos):
        self._grupos = grupos

    def agregar_grupo(self, grupo):
        self._grupos.append(grupo)

    def get_restaurantes(self):
        return self._restaurantes

    def set_restaurantes(self, restaurantes):
        self._restaurantes = restaurantes

    def get_precio_final_hospedaje(self):
        return self._precio_final_hospedaje

    def set_precio_final_hospedaje(self, precio):
        self._precio_final_hospedaje = precio

    @staticmethod
    def numero_de_adultos(clientes):
        return sum(1 for cliente in clientes if cliente.get_edad() >= 18)
