from enum import Enum

class TipoActividad(Enum):
    CULTURALES = ("Cultural", "Baja")
    FAMILIARES = ("Familiar", "Baja")
    ECOLOGICAS = ("Ecológica", "Media")
    EXTREMAS = ("Extrema", "Extrema")
    ACUATICAS = ("Acuática", "Alta")
    DEPORTIVAS = ("Deportiva", "Alta")
    HOSPEDAJE = ("Hospedaje", "Baja")
    RESTAURANTE = ("Restaurante", "Baja")

    def __init__(self, nombre, dificultad):
        self.nombre = nombre
        self.dificultad = dificultad

    @staticmethod
    def listaNombres():
        ListaTipos = []
        for tipo in TipoActividad:
            ListaTipos.append(tipo.getNombre())
        return ListaTipos

    @staticmethod
    def buscarNombre(nombre):
        for tipo in TipoActividad:
            if nombre == tipo.getNombre():
                return tipo
        return None

    def getNombre(self):
        return self.nombre

    def getDificultad(self):
        return self.dificultad
