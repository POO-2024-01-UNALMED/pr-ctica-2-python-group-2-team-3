import os
import pickle

class Serializador:
    archivo = ""

    @staticmethod
    def serializar_reservas(reservas):
        try:
            with open(os.path.join(Serializador.archivo, "src", "baseDatos", "reservas"), 'wb') as f:
                pickle.dump(reservas, f)
                print("Serializando..........")
        except FileNotFoundError:
            print("Archivo no encontrado (Reservas)")
        except IOError:
            print("Error inicializando flujo de salida")

    @staticmethod
    def serializar_destinos(destinos):
        try:
            with open(os.path.join(Serializador.archivo, "src", "baseDatos","destinos"), 'wb') as f:
                pickle.dump(destinos, f)
        except FileNotFoundError:
            print("Archivo no encontrado (Destinos)")
        except IOError: 
            print("Error inicializando flujo de salida")

    @staticmethod
    def serializar_actividades(actividades):
        try:
            with open(os.path.join(Serializador.archivo, "src", "baseDatos","actividades"), 'wb') as f:
                pickle.dump(actividades, f)
        except FileNotFoundError:
            print("Archivo no encontrado (Actividades)")
        except IOError:
            print("Error inicializando flujo de salida")

    @staticmethod
    def serializar_grupos(grupos):
        try:
            with open(os.path.join(Serializador.archivo, "src", "baseDatos","grupos"), 'wb') as f:
                pickle.dump(grupos, f)
        except FileNotFoundError:
            print("Archivo no encontrado (Grupos)")
        except IOError:
            print("Error inicializando flujo de salida")

    @staticmethod
    def serializar_guias(guias):
        try:
            with open(os.path.join(Serializador.archivo, "src", "baseDatos","guias"), 'wb') as f:
                pickle.dump(guias, f)
        except FileNotFoundError:
            print("Archivo no encontrado (Guias)")
        except IOError:
            print("Error inicializando flujo de salida")

    @staticmethod
    def serializar_planes(planes):
        try:
            with open(os.path.join(Serializador.archivo, "src", "baseDatos","planes"), 'wb') as f:
                pickle.dump(planes, f)
        except FileNotFoundError:
            print("Archivo no encontrado (Planes)")
        except IOError:
            print("Error inicializando flujo de salida")
