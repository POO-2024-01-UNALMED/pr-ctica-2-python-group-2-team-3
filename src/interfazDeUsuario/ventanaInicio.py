import sys
import os
import tkinter as tk
from tkinter.ttk import Treeview


class VentanaInicio(tk.Tk):
    """
    Clase que representa la ventana de inicio de la aplicación de gestión de actividades turísticas.
    Donde se maneja la información relacionada brindar la información del sistema y saludo de bienvenida.
    Hereda de tk.Tk para crear una interfaz gráfica de usuario utilizando Tkinter.
    """

    def __init__(self):
        """
        Constructor de la clase ventanaInicio.
        """
        super().__init__()
        self.title("Ventana de Inicio")
        self.resizable(True, True)
        self.config(bg="white smoke")

        # Creación de los widgets

        self.crearFrames()


    def crearFrames(self):
        """
        Método que crea los frames necesarios para la ventana de inicio. Es decir, los 2 frames a la izquierda y derecha
        más los subframes de cada uno.
        """

        #Frame izquierdo
        self.frame_left = tk.Frame(self, bg="light gray")
        self.frame_left.pack(side="left", anchor= "w", fill= "both", expand=True, padx=5, pady=5)

        #Frame derecho
        self.frame_right = tk.Frame(self, bg="light gray")
        self.frame_right.pack(side="right", anchor= "e", fill= "both", expand=True, padx=5, pady=5)

        #Subframes del frame izquierdo
        self.frame_left_down = tk.Frame(self.frame_left, bg="white")
        self.frame_left_down.pack(side="bottom", fill="both", expand=True, pady=5, padx=10)

        self.frame_left_up = tk.Frame(self.frame_left, bg="white")
        self.frame_left_up.pack(side="top", fill="both", expand=True, pady=5, padx=10)

        #Subframes del frame derecho
        self.frame_right_down = tk.Frame(self.frame_right, bg="white")
        self.frame_right_down.pack(side="bottom", fill="both", expand=True, pady=5, padx=10)

        self.frame_right_up = tk.Frame(self.frame_right, bg="white")
        self.frame_right_up.pack(side="top", fill="both", expand=True, pady=5, padx=10)

        #Creación de los widgets de cada frame

        #Fotos derecha
        self.label_foto1 = tk.Label(self.frame_right_down)
        self.label_foto1.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.label_foto2 = tk.Label(self.frame_right_down)
        self.label_foto2.grid(row=0, column=5, padx=5, pady=5, sticky="ne")

        self.label_foto3 = tk.Label(self.frame_right_down)
        self.label_foto3.grid(row=5, column=0, padx=5, pady=5, sticky="sw")

        self.label_foto4 = tk.Label(self.frame_right_down)
        self.label_foto4.grid(row=5, column=5, padx=5, pady=5, sticky="se")



if __name__ == "__main__":
    app = VentanaInicio()
    app.mainloop()