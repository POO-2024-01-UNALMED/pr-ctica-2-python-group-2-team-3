
from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre=None, destino=None, edad=0,idiomas=[]):
        self._idiomas = idiomas
        self._nombre = nombre
        self._destino = destino
        self._edad = edad

    @abstractmethod
    def toString(self):
        pass

    def ingresarIdiomas(self, listaIdiomas):
        from gestorAplicacion.idioma import Idioma
        for idioma in listaIdiomas:
            obj=Idioma.buscarNombre(idioma)
            self._idiomas.append(obj)

    # Métodos de acceso
    def setNombre(self, nombre):
        self._nombre = nombre

    def setDestino(self, destino):
        self._destino = destino

    def setIdiomas(self, idiomas):
        self._idiomas = idiomas

    def getNombre(self):
        return self._nombre

    def getDestino(self):
        return self._destino

    def getIdiomas(self):
        return self._idiomas

    def getEdad(self):
        return self._edad

    def setEdad(self, edad):
        self._edad = edad

    def addIdioma(self, idioma):
        self._idiomas.append(idioma)
