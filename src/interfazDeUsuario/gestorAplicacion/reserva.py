
class Reserva:
    _ultimo_codigo = 0
    _reservas_existentes = []

    def __init__(self, cliente=None, fechas=None, idioma=None, destino=None,destinoNombre=None, clasificacion=0, tipo_plan='', existe_suscripcion=False, plan=None, its_planeacion=True):
        self._codigo = self._incrementar_codigo()
        self._clientes = [cliente] if cliente else []
        self._idiomas = [idioma] if idioma else []
        self._fechas = fechas if fechas else []
        self._clasificacion = clasificacion
        self._tipo_plan = tipo_plan
        self._destinoNombre=destinoNombre
        self._existe_suscripcion = existe_suscripcion
        self._plan = plan
        self._paquete_turistico=None
        self._its_planeacion = its_planeacion
        self._descuento_por_cancelacion = ''
        self._descuento = 0
        Reserva._reservas_existentes.append(self)

    def toString(self):
        from gestorAplicacion.hotel import Hotel
        precio = 0
        if self.clientes[0].get_hotel() is None:
            precio = self.plan.get_precio() * len(self.clientes) - self.plan.get_precio() * self.clientes[0].get_suscripcion().get_desc_tour() * self.clientes[0].get_suscripcion().get_capacidad()
            if self.descuento != 0:
                precio *= self.descuento
            return [
                ("Código", str(self.codigo)),
                ("Titular", str(self.clientes[0])),
                ("Destino", str(self.destino)),
                ("Idiomas", ', '.join(str(idioma) for idioma in self.idiomas)),
                ("Fechas", str(self.fechas)),
                ("Clasificación", str(self.clasificacion)),
                ("Tipo de Plan", str(self.tipo_plan)),
                ("Actividades", str(self.plan.get_actividades())),
                ("Precio", str(precio)),
                ("Descuento por Cancelación", str(self.descuento_por_cancelacion))
            ]

        if self.plan is None:
            precio = Hotel.calcular_precio(self)
            if self.descuento != 0:
                precio *= self.descuento
            return [
                ("Hotel", self.clientes[0].get_hotel().get_nombre()),
                ("Habitación", self.clientes[0].get_grupos()[0].get_tipo_habitacion()),
                ("Restaurante", self.clientes[0].get_restaurantes()[0].get_nombre()),
                ("Precio total del hospedaje", str(self.clientes[0].get_hotel().get_precio_final_hospedaje()))
            ]

        precio = (self.plan.get_precio() * len(self.clientes) - self.plan.get_precio() * self.clientes[0].get_suscripcion().get_desc_tour() * self.clientes[0].get_suscripcion().get_capacidad()) + Hotel.calcular_precio(self)
        if self.descuento != 0:
            precio *= self.descuento
        return [
            ("Código", str(self.codigo)),
            ("Titular", str(self.clientes[0])),
            ("Destino", str(self.destino)),
            ("Idiomas", ', '.join(str(idioma) for idioma in self.idiomas)),
            ("Fechas", str(self.fechas)),
            ("Clasificación", str(self.clasificacion)),
            ("Tipo de Plan", str(self.tipo_plan)),
            ("Actividades", str(self.plan.get_actividades())),
            ("Precio", str(precio)),
            ("Descuento por Cancelación", str(self.descuento_por_cancelacion)),
            ("Hotel", self.clientes[0].get_hotel().get_nombre()),
            ("Habitación", self.clientes[0].get_grupos()[0].get_tipo_habitacion()),
            ("Restaurante", self.clientes[0].get_restaurantes()[0].get_nombre()),
            ("Precio total del hospedaje", str(self.clientes[0].get_hotel().get_precio_final_hospedaje()))
        ]

    def mostrarPlan(self):
        precio = self.plan.get_precio() * len(self.clientes) - self.plan.get_precio() * self.clientes[0].get_suscripcion().get_desc_tour() * self.clientes[0].get_suscripcion().get_capacidad()
        if self.descuento != 0:
            precio *= self.descuento
        return [
            ("Clasificación", str(self.clasificacion)),
            ("Tipo de Plan", str(self.tipo_plan)),
            ("Actividades", str(self.plan.get_actividades())),
            ("Precio", str(precio)),
            ("Descuento por Cancelación", str(self.descuento_por_cancelacion))
        ]

    def mostrarDatosBasicos(self):
        nombres_clientes = [cliente.get_nombre() for cliente in self.clientes]
        return [
            ("Código", str(self.codigo)),
            ("Destino", str(self.destino)),
            ("Idiomas", ', '.join(str(idioma) for idioma in self.idiomas)),
            ("Fechas", str(self.fechas)),
            ("Lista de Clientes", ', '.join(nombres_clientes))
        ]

    @staticmethod
    def _incrementar_codigo():
        Reserva._ultimo_codigo += 1
        return Reserva._ultimo_codigo

    @staticmethod
    def mostrarDias(cantidad_dias, fecha_inicio_str):
        from datetime import datetime, timedelta
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        lista_fechas = [(fecha_inicio + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(int(cantidad_dias))]
        return lista_fechas
    
    @staticmethod
    def generar_lista_fechas_aleatorias():
        import random
        cantidad_fechas = random.randint(5, 15)  
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

    def listaMes(date_str):
        from datetime import datetime, timedelta
        date = datetime.strptime(date_str, "%d/%m/%Y")
        first_day = date.replace(day=1)
        next_month = first_day.replace(day=28) + timedelta(days=4)  
        last_day = next_month - timedelta(days=next_month.day)
        
        dates = []
        current_day = first_day
        while current_day <= last_day:
            dates.append(current_day.strftime("%d/%m/%Y"))
            current_day += timedelta(days=1)
        
        return dates
    
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

    def definirPrecio(self):
        from gestorAplicacion.hotel import Hotel
        lista_paquete = self._paquete_turistico.split('precio: $')
        precio_paquete=float(lista_paquete[1])
        cantidad_paquete=self._paquete_turistico.split('cantidad de personas: ')
        capacidad=int(cantidad_paquete[1].split(',')[0])
        hotel=Hotel.buscarHotelNombre(self._hotel)
        precioHotel=hotel.get_precio() if hotel is not None else 80000
        n=1
        cantidadClientes=self.get_cantidadClientes()
        while True:
            personas=capacidad-cantidadClientes
            if personas<=0:
                break
            else:
                capacidad=personas
                n+=1
        self._precio=(precio_paquete*n)+(precioHotel*cantidadClientes)

    def encontrarCodigo(codigo):
            import random
            from datetime import datetime, timedelta
            from gestorAplicacion.destino import Destino
            from gestorAplicacion.idioma import Idioma
            from gestorAplicacion.hotel import Hotel
            paquetes = [
                "Tour 5 Cascadas", "Expedición al Amazonas", "Tour por Cascadas", "Aventura en la Playa", "Recorrido artístico", "Naturaleza y Descanso",
                "Escapada Romántica", "Exploración Urbana", "Ruta del Café", "Safari Fotográfico", "Senderismo en Montañas", "Crucero de Lujo",
                "Tour Gastronómico", "Descubre las Islas", "Aventura Extrema"
                ]
            destino = random.choice(Destino.listaNombres())
            fecha_inicio = datetime.now()
            fecha_fin = fecha_inicio + timedelta(days=random.randint(1, 15))
            fechas = [fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")]
            idiomas = random.choice(Idioma.listaNombres())
            paquete_turistico = random.choice(paquetes)
            hotel = random.choice(Hotel.mostrarHoteles())
            cantidad_clientes = random.randint(1,64)
            precio = round(random.uniform(200000, 1000000), 2)
            codigo = random.randint(100, 999)

            return Reserva(destinoNombre=destino, fechas=fechas, idioma=idiomas, paquete_turistico=paquete_turistico, hotel=hotel, cantidad_clientes=cantidad_clientes, precio=precio, codigo=codigo)

    def resumenViaje(self):
        return[("Destino",self._destinoNombre),
               ("Fechas",self._fechas[0]+"-"+self._fechas[-1]),
               ("Idioma",self._idiomas),
               ("Paquete turistico",self._paquete_turistico.split("=")[0]),
               ("Hotel", self._hotel),
               ("Cantidad de clientes",str(self._cantidad_clientes)),
               ("Precio Final",str(self._precio)),
               ("Codigo",str(self._codigo))]
# Métodos de acceso
    @staticmethod
    def get_reservas_existentes():
        return Reserva._reservas_existentes
    
    def  set_cantidadClientes(self, cantidad):
        self._cantidad_clientes = cantidad
        
    def get_cantidadClientes(self):
        return self._cantidad_clientes

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

    def set_destinoNombre(self,nombre):
        self._destinoNombre = nombre
        
    def get_destinoNombre(self):
        return self._destinoNombre
    
    def set_clientes(self, clientes):
        self._clientes = clientes
        
    def get_paquete_turistico(self):
        return self._paquete_turistico
    
    def set_paquete_turistico(self,paquete):
        self._paquete_turistico=paquete

    def set_hotel(self,hotel):
        self._hotel=hotel
        
    def get_hotel(self):
        return  self._hotel

    def set_precio(self,precio):
        self._precio=precio
        
    def get_precio(self):
        return self._precio
    
    def añadir_reserva(self):
        Reserva._reservas_existentes.append(self)

    