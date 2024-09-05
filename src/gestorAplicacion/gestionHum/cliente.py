class Cliente(Persona):
    def __init__(self, nombre=None, destino=None, edad=18):
        super().__init__(nombre, destino, edad)
        self.restaurantes = []  # Inicia la lista de restaurantes
        self.grupos = []  # Inicia la lista de grupos
        self.suscripcion = None
        self.hotel = None
        self.habitacion = None
        self.mesa_restaurante = None

    def __str__(self):
        if self.suscripcion is not None:
            sus = self.suscripcion.tipo
            return f"{self.nombre} con {self.edad} años. Suscripción de tipo: {sus}"
        return f"{self.nombre} con {self.edad} años."

    @classmethod
    def from_nombre(cls, nombre):
        return cls(nombre, edad=18)

    @classmethod
    def from_nombre_edad(cls, nombre, edad):
        return cls(nombre, edad=edad)

    def mayor_de_edad(self):
        return self.edad >= 18

    def cancelar_actividad(self, actividad, fecha):
        # NO SE QUE HACEEEER
        pass

    def set_suscripcion(self, suscripcion):
        self.suscripcion = suscripcion

    def set_hotel(self, hotel):
        self.hotel = hotel

    def set_habitacion(self, habitacion):
        self.habitacion = habitacion

    def get_suscripcion(self):
        return self.suscripcion

    def get_hotel(self):
        return self.hotel

    def get_habitacion(self):
        return self.habitacion

    def add_grupo(self, grupo):
        self.grupos.append(grupo)

    def get_grupos(self):
        return self.grupos

    def set_restaurantes(self, restaurante):
        self.restaurantes.append(restaurante)

    def get_restaurantes(self):
        return self.restaurantes

    def set_grupos(self, grupo):
        self.grupos.append(grupo)

    def set_mesa_restaurante(self, mesa_restaurante):
        self.mesa_restaurante = mesa_restaurante

    def get_mesa_restaurante(self):
        return self.mesa_restaurante