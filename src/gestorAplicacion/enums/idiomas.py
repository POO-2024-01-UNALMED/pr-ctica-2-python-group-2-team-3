from enum import Enum

class Idiomas(Enum):
    INGLES = ("Inglés", 10000)
    PORTUGUES = ("Portugués", 10000)
    ESPANOL = ("Español", 5000)
    FRANCES = ("Francés", 15000)
    ITALIANO = ("Italiano", 15000)

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    @staticmethod
    def listaNombres():
        ListaTipos = []
        for idioma in Idiomas:
            ListaTipos.append(idioma.getNombre())
        return ListaTipos

    @staticmethod
    def buscarNombre(nombre):
        for idioma in Idiomas:
            if nombre == idioma.getNombre():
                return idioma
        return None

    def getNombre(self):
        return self.nombre

    def getPrecio(self):
        return self.precio