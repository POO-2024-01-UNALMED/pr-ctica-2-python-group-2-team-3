import sys
import os
import pickle


# Ajustar las rutas para las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'clases')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modulos')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gestorAplicacion')))



from gestorAplicacion.cliente import Cliente
from gestorAplicacion.grupo import Grupo
from gestorAplicacion.plan import Plan
from serializador import Serializador
from gestorAplicacion.idioma import Idioma


# Importar clases 
from clases.menu import Menu
from clases.pdfViewer import PdfViewer
from clases.fieldFrame import FieldFrame
from clases.tabla import Tabla

# Importar modulos
from modulos.verOpcionesDeAdministrador import *
from modulos.reservarActividades import reservarActividades
from modulos.reservarHospedaje import reservarHospedaje
from modulos.planearViaje import planearViaje
from modulos.modificarReserva import modificarReserva
def main():
    # Crear listas para todo lo que se quiere guardar
    destinos = []
    actividades = []
    guias = []
    reservas = []
    grupos = []
    planes = []

    # Crear destinos
    cartagena = Destino("Cartagena")
    destinos.append(cartagena)
    bogota = Destino("Bogotá")
    destinos.append(bogota)
    medellin = Destino("Medellin")
    destinos.append(medellin)

    # Crear actividades
    actividades_list = [
        ("Tour por la ciudad", cartagena, TipoActividad.CULTURALES),
        ("Tour por la ciudad", bogota, TipoActividad.CULTURALES),
        ("Tour por la ciudad", medellin, TipoActividad.CULTURALES),
        ("Visita a museos", bogota, TipoActividad.CULTURALES),
        ("Visita a museos", medellin, TipoActividad.CULTURALES),
        ("Excursión a la playa", cartagena, TipoActividad.ACUATICAS),
        ("Gastronomía local", cartagena, TipoActividad.FAMILIARES),
        ("Gastronomía local", bogota, TipoActividad.FAMILIARES),
        ("Gastronomía local", cartagena, TipoActividad.FAMILIARES),
        ("Senderismo", cartagena, TipoActividad.ECOLOGICAS),
        ("Senderismo", bogota, TipoActividad.ECOLOGICAS),
        ("Senderismo", medellin, TipoActividad.ECOLOGICAS),
        ("Parapente", bogota, TipoActividad.EXTREMAS),
        ("Parapente", medellin, TipoActividad.EXTREMAS),
        ("Fútbol", bogota, TipoActividad.DEPORTIVAS),
        ("Fútbol", medellin, TipoActividad.DEPORTIVAS),
        ("Fútbol", cartagena, TipoActividad.DEPORTIVAS)
    ]
    
    for nombre, destino, tipo in actividades_list:
        actividades.append(Actividad(nombre, destino, tipo))

# Crear guías y asignarles Idioma
    guias_data = [
        ("Juan", [Idioma.ESPANOL, Idioma.INGLES]),
        ("Maria", [Idioma.ESPANOL, Idioma.FRANCES]),
        ("Carlos", [Idioma.ESPANOL, Idioma.PORTUGUES]),
        ("Pedro", [Idioma.ESPANOL, Idioma.INGLES]),
        ("Luis", [Idioma.ESPANOL, Idioma.FRANCES]),
        ("Ana", [Idioma.ESPANOL, Idioma.PORTUGUES]),
        ("Sofia", [Idioma.ESPANOL, Idioma.INGLES]),
        ("Lucia", [Idioma.ESPANOL, Idioma.FRANCES]),
        ("Marta", [Idioma.ESPANOL]),
        ("Laura", [Idioma.ESPANOL])
        ]

    for nombre, idiomas in guias_data:  
        guia = Guia(nombre,20)
        for idioma in idiomas:  
            guia.addIdioma(idioma)
        guias.append(guia)

    # Crear grupos
    grupos = [Grupo(guia) for guia in guias]

    # Crear reservas
    reservas = [Reserva(Cliente(nombre)) for nombre in ["Carlos", "Juan", "Maria", "Pedro", "Luis", "Ana", "Sofia", "Lucia", "Marta", "Laura"]]

    # Asignar guías a destinos
    cartagena._guias += [guias[0], guias[1], guias[6], guias[9]]
    bogota._guias += [guias[2], guias[3], guias[7]]
    medellin._guias += [guias[4], guias[5], guias[8]]

    # Serializar datos
    destinos = Destino.getDestinos()
    for destino in destinos:
        actividades += destino.getActividades()
    guias = Guia.getGuias()
    reservas = Reserva.get_reservas_existentes()
    grupos = Grupo.get_grupos()
    planes = Plan.getPaquetes()

    Serializador.serializar_grupos(grupos)
    Serializador.serializar_reservas(reservas)
    Serializador.serializar_actividades(actividades)
    Serializador.serializar_destinos(destinos)
    Serializador.serializar_guias(guias)
    Serializador.serializar_planes(planes)

if __name__ == "__main__":
    main()
