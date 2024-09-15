import sys
import os
import tkinter as tk
from tkinter import messagebox

#importar la ventana principal
#from ventanaPrincipalDeUsuario import VentanaPrincipalDeUsuario


class VentanaInicio(tk.Tk):
    """
    Clase que representa la ventana de inicio de la aplicación de gestión de actividades turísticas.
    Donde se maneja la información relacionada brindar la información del sistema y saludo de bienvenida.
    Hereda de tk.Tk para crear una interfaz gráfica de usuario utilizando Tkinter.
    """

    # Atributos de la clase

    #Ruta fotos desarrolladores
    """
    Realizamos este paso extra para evitar problemas con la importación de las fotos
    """
    ruta_lau1 = os.path.join(os.path.dirname(__file__), 'archivos', 'lau1.jpg')
    ruta_lau2 = os.path.join(os.path.dirname(__file__), 'archivos', 'lau2.jpg')
    ruta_lau3 = os.path.join(os.path.dirname(__file__), 'archivos', 'lau3.jpg')
    ruta_lau4 = os.path.join(os.path.dirname(__file__), 'archivos', 'lau4.jpg')

    ruta_pupo1 = os.path.join(os.path.dirname(__file__), 'archivos', 'pupo1.jpg')
    ruta_pupo2 = os.path.join(os.path.dirname(__file__), 'archivos', 'pupo2.jpg')
    ruta_pupo3 = os.path.join(os.path.dirname(__file__), 'archivos', 'pupo3.jpg')
    ruta_pupo4 = os.path.join(os.path.dirname(__file__), 'archivos', 'pupo4.jpg')

    ruta_petro1 = os.path.join(os.path.dirname(__file__), 'archivos', 'petro1.jpg')
    ruta_petro2 = os.path.join(os.path.dirname(__file__), 'archivos', 'petro2.jpg')
    ruta_petro3 = os.path.join(os.path.dirname(__file__), 'archivos', 'petro3.jpg')
    ruta_petro4 = os.path.join(os.path.dirname(__file__), 'archivos', 'petro4.jpg')


    ruta_fotos_desarrolladores = [(ruta_lau1, ruta_lau2, ruta_lau3, ruta_lau4), (ruta_pupo1, ruta_pupo2, ruta_pupo3, ruta_pupo4), (ruta_petro1, ruta_petro2, ruta_petro3, ruta_petro4)]

    #Ruta fotos sistema
    ruta_sistema1 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema1.jpg')
    ruta_sistema2 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema2.jpg')
    ruta_sistema3 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema3.jpg')
    ruta_sistema4 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema4.jpg')
    ruta_sistema5 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema5.jpg')

    ruta_fotos_sistema = [ruta_sistema1, ruta_sistema2, ruta_sistema3, ruta_sistema4, ruta_sistema5]

    #Hojas de vida de los desarrolladores

    hojas_vida = ["""Soy aries y tengo 18 años.
        De pequeña quería ser princesa pero la vida es cruel y me tocó conformarme con ser ingeniera,
        adoro los animales lo que es curioso por que soy super alérgica a ellos,
        tengo una mini yo en mi casa que dice ser mi hermana y de chiquita me disfraze de un pollo""",
                  "Pupo", "Petro"]

    def __init__(self):
        """
        Constructor de la clase ventanaInicio.
        """
        super().__init__()
        self.title("Ventana de Inicio")
        self.resizable(True, True)
        self.config(bg="white smoke")   #Color de fondo, hablar con el equipo para proponer más colores

        #Variables de control de texto (Saludo-Descripción y HDV)
        self.variable_HDV = tk.StringVar()
        self.variable_HDV.set("   Conoce a nuestros desarrolladores   ")

        self.variable_Saludo = tk.StringVar()
        self.variable_Saludo.set("""Bienvenido a la aplicación de gestión\nde actividades turísticas y hospedaje""")

        #Contadores para las imágenes
        self.indice_HDV = 0
        self.indice_fotos = 0

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
        self.frame_p1 = tk.Frame(self, bg="light gray")
        self.frame_p1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #Frame derecho
        self.frame_p2 = tk.Frame(self, bg="light gray")
        self.frame_p2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        #Configurar las filas y columnas para que se expandan
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="column")
        self.grid_columnconfigure(1, weight=1, uniform="column")

        #Subframes del frame izquierdo
        self.frame_p3 = tk.Frame(self.frame_p1, bg="white")
        self.frame_p3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.frame_p4 = tk.Frame(self.frame_p1, bg="white")
        self.frame_p4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Configurar las filas y columnas para que se expandan
        self.frame_p1.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p1.grid_rowconfigure(1, weight=3, uniform="row")
        self.frame_p1.grid_columnconfigure(0, weight=1, uniform="column")

        #Subframes del frame derecho
        self.frame_p5 = tk.Frame(self.frame_p2, bg="white")
        self.frame_p5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.frame_p6 = tk.Frame(self.frame_p2, bg="white")
        self.frame_p6.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        #Configurar las filas y columnas para que se expandan
        self.frame_p2.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p2.grid_rowconfigure(1, weight=3, uniform="row")
        self.frame_p2.grid_columnconfigure(0, weight=1, uniform="column")

        #Creación de los widgets de cada frame

        # Elementos de frame_p6
        self.label_foto1 = tk.Label(self.frame_p6, bg="light gray")
        self.label_foto1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.label_foto2 = tk.Label(self.frame_p6, bg="light gray")
        self.label_foto2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.label_foto3 = tk.Label(self.frame_p6, bg="light gray")
        self.label_foto3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.label_foto4 = tk.Label(self.frame_p6, bg="light gray")
        self.label_foto4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.frame_p6.grid_rowconfigure(0, weight=1)
        self.frame_p6.grid_rowconfigure(1, weight=1)
        self.frame_p6.grid_columnconfigure(0, weight=1)
        self.frame_p6.grid_columnconfigure(1, weight=1)

        #Elementos de frame_p4
        self.label_fotos_sistema = tk.Label(self.frame_p4, bg="light gray")
        self.label_fotos_sistema.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.boton_ventana_principal = tk.Button(self.frame_p4, text="Abrir la Ventana Principal", bg="white smoke", font=("Candara", 12), activebackground="light gray", command=self.abrirVentanaPrincipal)
        self.boton_ventana_principal.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.frame_p4.grid_rowconfigure(0, weight=15)
        self.frame_p4.grid_rowconfigure(1, weight=1)
        self.frame_p4.grid_columnconfigure(0, weight=1)

        #Elementos de frame_p3
        self.label_saludo = tk.Label(self.frame_p3, textvariable=self.variable_Saludo, bg="white", fg="black", font=("Candara", 15))
        self.label_saludo.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.frame_p3.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p3.grid_columnconfigure(0, weight=1, uniform="column")

        #Elementos de frame_p5
        self.label_HDV = tk.Label(self.frame_p5, textvariable=self.variable_HDV, bg="white", fg="black", font=("Candara", 12))
        self.label_HDV.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.frame_p5.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p5.grid_columnconfigure(0, weight=1, uniform="column")







    def crearMenu(self):
        """
        Método que crea el menú de la ventana de inicio.
        """
        # Creación de la barra de menú
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu_opciones = tk.Menu(self.menu_bar, tearoff=0, bg="white smoke", activebackground="light gray", activeforeground="black",font=("Candara Light", 12))
        self.menu_bar.add_cascade(label="Inicio", menu=self.menu_opciones)

        # Creación de las opciones del menú
        self.menu_opciones.add_command(label="Salir", command=self.salir, font=("Candara", 12))
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label="Descripción", command=self.descripcionSistema, font=("Candara", 12))

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

    def abrirVentanaPrincipal(self):
        """
        Método que abre la ventana principal del usuario.
        """
        self.withdraw()
        """"ventana_principal = VentanaPrincipalDeUsuario(self)
        ventana_principal.deiconify()"""






if __name__ == "__main__":
    app = VentanaInicio()
    app.mainloop()