from typing import List
from enums import Idiomas  # Assuming enums.py contains the Idiomas enum

class Persona:
    def __init__(self, nombre: str = None, destino: 'Destino' = None, edad: int = 0):
        self.idiomas: List[Idiomas] = []
        self.nombre = nombre
        self.destino = destino
        self.edad = edad

    def __str__(self):
        return f"Nombre: {self.nombre}\nEdad: {self.edad}\nDestino: {self.destino}\nIdiomas: {self.idiomas}"

    def ingresar_idiomas(self, idiomas: str):
        for idioma in idiomas.split(","):
            self.idiomas.append(Idiomas[idioma.strip().upper()])

    # Métodos de acceso
    def set_nombre(self, nombre: str):
        self.nombre = nombre

    def set_destino(self, destino: 'Destino'):
        self.destino = destino

    def set_idiomas(self, idiomas: List[Idiomas]):
        self.idiomas = idiomas

    def get_nombre(self) -> str:
        return self.nombre

    def get_destino(self) -> 'Destino':
        return self.destino

    def get_idiomas(self) -> List[Idiomas]:
        return self.idiomas

    def get_edad(self) -> int:
        return self.edad

    def set_edad(self, edad: int):
        self.edad = edad

    def add_idioma(self, idioma: Idiomas):
        self.idiomas.append(idioma)  