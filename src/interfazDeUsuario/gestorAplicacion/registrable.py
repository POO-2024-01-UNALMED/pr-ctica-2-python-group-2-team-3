from abc import ABC, abstractmethod

class Registrable(ABC):
    @abstractmethod
    def ingresarGuia(self):
        pass

    @abstractmethod
    def ingresarTipoActividades(self, tipoActividad):
        pass

    @abstractmethod
    def asignarParametros(self):
        pass