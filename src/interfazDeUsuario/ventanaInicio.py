import sys
import os
import tkinter as tk
from tkinter import messagebox


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

        # Creación menú

        self.crearMenu()


    def crearFrames(self):
        """
        Método que crea los frames necesarios para la ventana de inicio. Es decir, los 2 frames a la izquierda y derecha
        más los subframes de cada uno.
        """

        #Frame izquierdo
        self.p1 = tk.Frame(self, bg="light gray")
        self.p1.pack(side="left", anchor="w", fill="both", expand=True, padx=5, pady=5)

        #Frame derecho
        self.p2 = tk.Frame(self, bg="light gray")
        self.p2.pack(side="right", anchor="e", fill="both", expand=True, padx=5, pady=5)

        #Subframes del frame izquierdo
        self.p4 = tk.Frame(self.p1, bg="white")
        self.p4.pack(side="bottom", fill="both", expand=True, pady=5, padx=10)

        self.p3 = tk.Frame(self.p1, bg="white")
        self.p3.pack(side="top", fill="both", expand=True, pady=5, padx=10)

        #Subframes del frame derecho
        self.p6 = tk.Frame(self.p2, bg="white")
        self.p6.pack(side="bottom", fill="both", expand=True, pady=5, padx=10)

        self.p5 = tk.Frame(self.p2, bg="white")
        self.p5.pack(side="top", fill="both", expand=True, pady=5, padx=10)

        #Creación de los widgets de cada frame

        # Espacio fotos p6
        self.label_foto1 = tk.Label(self.p6, bg="light gray")
        self.label_foto1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.label_foto2 = tk.Label(self.p6, bg="light gray")
        self.label_foto2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.label_foto3 = tk.Label(self.p6, bg="light gray")
        self.label_foto3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.label_foto4 = tk.Label(self.p6, bg="light gray")
        self.label_foto4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.p6.grid_rowconfigure(0, weight=1)
        self.p6.grid_rowconfigure(1, weight=1)
        self.p6.grid_columnconfigure(0, weight=1)
        self.p6.grid_columnconfigure(1, weight=1)


    def crearMenu(self):
        """
        Método que crea el menú de la ventana de inicio.
        """
        # Creación de la barra de menú
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu_opciones = tk.Menu(self.menu_bar, tearoff=0, activebackground="black", activeforeground="white smoke")
        self.menu_bar.add_cascade(label="Inicio", menu=self.menu_opciones)

        # Creación de las opciones del menú
        self.menu_opciones.add_command(label="Salir", command=self.salir)
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label="Descripción", command=self.descripcionSistema)

    def salir(self):
        """
        Método que cierra la aplicación.
        """
        opcion = messagebox.askyesno("Salir", "¿Está seguro que desea salir de la aplicación?")
        if opcion:
            self.destroy()


    def descripcionSistema(self):
        """
        Método que muestra la descripción del sistema.
        """
        print("Sistema de gestión de actividades turísticas")






if __name__ == "__main__":
    app = VentanaInicio()
    app.mainloop()