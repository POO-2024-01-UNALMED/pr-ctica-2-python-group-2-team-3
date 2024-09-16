from gestorAplicacion.persona import Persona

class Cliente(Persona):
    def __init__(self, nombre=None, destino=None, edad=18):
        super().__init__(nombre, destino, edad)
        self._restaurantes = []
        self._grupos = []
        self._suscripcion = None
        self._hotel = None
        self._habitacion = None
        self._mesa_restaurante = None

    def toString(self):
        return [
            ("Nombre:", str(self._nombre)),
            ("Edad:", str(self._edad)),
            ("Destino:", str(self._destino.getNombre())),
            ("Idiomas",', '.join(str(idioma.getNombre()) for idioma in self._idiomas)),
            ("Suscripcion",self._suscripcion.getTipo()if self._suscripcion is not None else "No aplica")
        ]

    def mayorDeEdad(self):
        return self.getEdad() >= 18

    # Métodos de acceso
    def setSuscripcion(self, suscripcion):
        self._suscripcion = suscripcion

    def getSuscripcion(self):
        return self._suscripcion

    def setHotel(self, hotel):
        self._hotel = hotel

    def getHotel(self):
        return self._hotel

    def setHabitacion(self, habitacion):
        self._habitacion = habitacion

    def getHabitacion(self):
        return self._habitacion

    def addGrupo(self, grupo):
        self._grupos.append(grupo)

    def getGrupos(self):
        return self._grupos

    def setRestaurantes(self, restaurante):
        self._restaurantes.append(restaurante)

    def getRestaurantes(self):
        return self._restaurantes

    def setGrupos(self, grupo):
        self._grupos.append(grupo)

    def setMesaRestaurante(self, mesa_restaurante):
        self._mesa_restaurante = mesa_restaurante

    def getMesaRestaurante(self):
        return self._mesa_restaurante
