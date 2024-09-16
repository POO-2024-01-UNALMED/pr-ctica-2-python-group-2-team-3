
class Reserva:
    _ultimo_codigo = 0
    _reservas_existentes = []

    def __init__(self, cliente=None, fechas=None, idioma=None, destino=None, clasificacion=0, tipo_plan='', existe_suscripcion=False, plan=None, its_planeacion=True):
        self._codigo = self._incrementar_codigo()
        self._clientes = [cliente] if cliente else []
        self._idiomas = [idioma] if idioma else []
        self._fechas = fechas if fechas else []
        self._clasificacion = clasificacion
        self._tipo_plan = tipo_plan
        self._existe_suscripcion = existe_suscripcion
        self._plan = plan
        self._its_planeacion = its_planeacion
        self._descuento_por_cancelacion = ''
        self._descuento = 0
        Reserva._reservas_existentes.append(self)

    @staticmethod
    def _incrementar_codigo():
        Reserva._ultimo_codigo += 1
        return Reserva._ultimo_codigo

    @staticmethod
    def mostrarDias(cantidad_dias, fecha_inicio_str):
        from datetime import datetime, timedelta
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        lista_fechas = [(fecha_inicio + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(cantidad_dias)]
        return lista_fechas
    
    @staticmethod
    def generar_lista_fechas_aleatorias():
        import random
        cantidad_fechas = random.randint(1, 10)  # Número aleatorio de fechas a generar (entre 1 y 10)
        lista_fechas = [Reserva.generar_fecha_aleatoria() for _ in range(cantidad_fechas)]
        return lista_fechas
    
    @staticmethod
    def mostrar_mes(fecha):
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return meses[fecha - 1]

    @staticmethod
    def comprobar_es_mes(lista_fechas):
        mes = f"{lista_fechas[0][1]}/{lista_fechas[0][2]}"
        lista_mes = Reserva.mostrar_lista_fechas("1", mes)
        return lista_fechas == lista_mes

    @staticmethod
    def mostrar_fecha_string(fecha):
        return f"[{fecha[0]}/{Reserva.mostrar_mes(fecha[1])}/{fecha[2]}]"

    @staticmethod
    def mostrar_clasificacion_comun(destino):
        clasificacion_comun = 1
        cantidad_mayor = 0
        for i in range(1, 5):
            cantidad_clasificacion = sum(
                1 for reserva in Reserva._reservas_existentes
                if reserva._destino == destino and reserva._clasificacion == i
            )
            if cantidad_clasificacion > cantidad_mayor:
                cantidad_mayor = cantidad_clasificacion
                clasificacion_comun = i
        return clasificacion_comun

    @staticmethod
    def mostrar_cantidad_personas_destino(destino):
        return sum(len(reserva._clientes) for reserva in Reserva._reservas_existentes if reserva._destino == destino)

    @staticmethod
    def mostrar_cantidad_personas_destino_fechas(destino, fechas):
        return sum(
            len(reserva._clientes) for fecha in fechas for reserva in Reserva._reservas_existentes
            if reserva._destino == destino and fecha in reserva._fechas
        )

    @staticmethod
    def mostrar_cantidad_reservas_hotel(destino, fechas, hotel):
        return sum(
            1 for fecha in fechas for reserva in Reserva._reservas_existentes
            if reserva._destino == destino and fecha in reserva._fechas and reserva._clientes[0].get_hotel() == hotel
        )

    @staticmethod
    def actividad_principal_destino(destino):
        actividad_comun = None
        cantidad_mayor = 0
        for actividad in destino.get_actividades():
            cantidad_personas = sum(
                1 for reserva in Reserva._reservas_existentes
                if reserva._destino == destino and actividad in reserva._plan.get_actividades()
            )
            if cantidad_personas > cantidad_mayor:
                cantidad_mayor = cantidad_personas
                actividad_comun = actividad
        return actividad_comun

    def tiene_suscripcion(self):
        return self._clientes[0].get_suscripcion() is not None

    def agregar_idioma(self, idioma):
        self._idiomas.append(idioma)

    def añadir_cliente(self, nombre, edad):
        from gestorAplicacion.cliente import Cliente
        cliente = Cliente(nombre, edad)
        self._clientes.append(cliente)

    def aplicar_suscripcion(self, existe_suscripcion):
        if not existe_suscripcion:
            return "No se ha registrado una suscripción para los clientes de la reserva."
        suscripcion = self._clientes[0].get_suscripcion()
        capacidad_suscripcion = suscripcion.get_capacidad()
        max_aplicable = min(capacidad_suscripcion, len(self._clientes))
        
        for i in range(max_aplicable):
            self._clientes[i].set_suscripcion(suscripcion)
        
        if len(self._clientes) > capacidad_suscripcion:
            return f"El descuento se aplicará solo a las primeras {capacidad_suscripcion} personas."
        return "La suscripción se registró de manera exitosa para todos los integrantes de la reserva."

    def menor_edad(self):
        return min(cliente.get_edad() for cliente in self._clientes)

    def asignar_clasificacion(self):
        menor_edad = self.menor_edad()
        if menor_edad < 7:
            self._clasificacion = 1
        elif menor_edad < 15:
            self._clasificacion = 2
        elif menor_edad < 18:
            self._clasificacion = 3
        else:
            self._clasificacion = 4

    def eliminar_reserva(self):
        if self._plan is not None:
            self._plan.eliminar_plan()
            self._plan = None
        elif self._clientes[0].get_hotel() is not None:
            self._clientes[0].get_hotel().eliminar_reservacion(self._clientes)

    @staticmethod
    def buscar_reserva(grupo, clientes):
        for reserva in Reserva._reservas_existentes:
            if reserva._clientes == clientes and grupo in reserva._plan.get_grupos():
                return reserva
        return None

    def cancelar_actividad(self, actividad):
        self._plan.eliminar_actividad(actividad)
        self._descuento_por_cancelacion += f"Por inconvenientes externos no se puede realizar la actividad {actividad.get_nombre()}\nPor las molestias se le dará un descuento del 10% en su reserva"
        self._descuento += 0.1

    @staticmethod
    def generar_fecha_aleatoria():
        import random
        import calendar
        mes = random.randint(1, 12)  # Genera un mes aleatorio
        dia_maximo = calendar.monthrange(2024, mes)[1]  # Obtiene el último día válido del mes
        dia = random.randint(1, dia_maximo)  # Genera un día válido basado en el mes
        return f"{dia}/{mes}/2024"
    
    def verificar_eliminar_reservacion(self, idioma_vrf, fechas_vrf, clientes_vrf):
        from gestorAplicacion.hotel import Hotel
        vrf = None
        vrf_plan = False
        vrf_hospedaje = False

        if self._plan is not None:
            vrf_plan = self._plan.verificar_eliminar_plan(idioma_vrf, fechas_vrf, clientes_vrf)
            if vrf_plan:
                vrf = "Plan"

        if self._clientes[0].get_hotel() is not None:
            vrf_hospedaje = self._clientes[0].get_hotel().verificar_eliminar_hospedaje(
                Hotel.buscar_habitaciones(self._clientes), self._fechas, clientes_vrf)
            if vrf_hospedaje:
                vrf = "Hospedaje"

        if vrf_plan and vrf_hospedaje:
            vrf = "Todo"

        return vrf


# Métodos de acceso
    @staticmethod
    def get_reservas_existentes():
        return Reserva._reservas_existentes

    @staticmethod
    def set_reservas_existentes(reservas_existentes):
        Reserva._reservas_existentes = reservas_existentes

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):
        self._codigo = codigo

    def get_destino(self):
        return self._destino

    def set_destino(self, destino):
        self._destino = destino

    def get_idiomas(self):
        return self._idiomas

    def set_idiomas(self, idiomas):
        self._idiomas = idiomas

    def get_fechas(self):
        return self._fechas

    def set_fechas(self, fechas):
        self._fechas = fechas

    def get_clasificacion(self):
        return self._clasificacion

    def set_clasificacion(self, clasificacion):
        self._clasificacion = clasificacion

    def get_tipo_plan(self):
        return self._tipo_plan

    def set_tipo_plan(self, tipo_plan):
        self._tipo_plan = tipo_plan

    def get_existe_suscripcion(self):
        return self._existe_suscripcion

    def set_existe_suscripcion(self, existe_suscripcion):
        self._existe_suscripcion = existe_suscripcion

    def get_plan(self):
        return self._plan

    def set_plan(self, plan):
        self._plan = plan

    def get_clientes(self):
        return self._clientes

    def set_clientes(self, clientes):
        self._clientes = clientes

    def añadir_reserva(self):
        Reserva._reservas_existentes.append(self)

    