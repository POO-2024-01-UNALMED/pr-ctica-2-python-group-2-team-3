import sys
import os
import tkinter as tk
from logging import disable
from tkinter import messagebox
from PIL import Image, ImageTk

import sys
import os

# Ajustar las rutas para las importaciones

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'clases')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modulos')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gestorAplicacion')))



#importar la ventana principal
from ventanaPrincipalDeUsuario import VentanaPrincipalDeUsuario

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

directorio_actual = os.path.dirname(os.path.abspath(__file__))

class VentanaInicio(tk.Tk):
    """
    Clase que representa la ventana de inicio de la aplicación de gestión de actividades turísticas.
    Donde se maneja la información relacionada brindar la información del sistema y saludo de bienvenida.
    Hereda de tk.Tk para crear una interfaz gráfica de usuario utilizando Tkinter.
    """
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# -------------------------------------CREAR LA VENTANA DE USUARIO------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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
    fotos_HDV = []

    #Ruta fotos sistema
    ruta_sistema1 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema1.jpg')
    ruta_sistema2 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema2.jpg')
    ruta_sistema3 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema3.jpg')
    ruta_sistema4 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema4.jpg')
    ruta_sistema5 = os.path.join(os.path.dirname(__file__), 'archivos', 'sistema5.jpg')

    ruta_fotos_sistema = [ruta_sistema1, ruta_sistema2, ruta_sistema3, ruta_sistema4, ruta_sistema5]

    #Desarrolladores
    nombres = ["Laura Ladino Gallego", "Maria Paulina Pupo Marin", "Alejandro López Posada"]

    hojas_vida = ["""Soy aries y tengo 18 años. De pequeña quería ser princesa pero la vida es cruel y me tocó
conformarme con ser ingeniera, adoro los animales lo que es curioso por que soy super
alérgica a ellos, tengo una mini yo en mi casa que dice ser mi hermana y de chiquita me
disfrazé de un pollo.""",
        """Tengo 18 años y adoro la lectura, los videojuegos y las manualidades. Soy una persona
muy creativa y me encanta aprender cosas nuevas. Mi mayor sueño es viajar por el mundo
y conocer diferentes culturas. Además, me encanta la comida picante aunque no me caiga muy bien y tengo 4 hermanos menores que adoro molestar.""",
        """Tengo 19 años y nunca olvidaré estar jugando el el primer Halo en el portátil de mi padre
cuando tenía 5 o 6 años, probablemente fue mi primer acercamiento con una
computadora, desde entonces los sistemas han representado una parte importante de mi vida."""
        ]

    def __init__(self):
        """
        Constructor de la clase ventanaInicio.
        """
        super().__init__()
        self.title("Ventana de Inicio")
        self.resizable(True, True)
        self.config(bg="old lace")   #Color de fondo, hablar con el equipo para proponer más colores

        #Variables de control de texto (Nombres, Saludo-Descripción)
        self.variable_nombres = tk.StringVar()

        self.variable_Saludo = tk.StringVar()
        self.variable_Saludo.set("""Bienvenido a la aplicación de gestión\nde actividades turísticas y hospedaje""")

        #Contadores para las imágenes
        self.indice_HDV = 0
        self.indice_fotos = 0

        # Creación de la imagen del sistema
        self.foto_sistema = None

        # Creación de los widgets
        self.crearFrames()
        self.asignarMetodos()

        # Creación menú
        self.crearMenu()


    def crearFrames(self):
        """
        Método que crea los frames necesarios para la ventana de inicio. Es decir, los 2 frames a la izquierda y derecha
        más los subframes de cada uno.
        """

        #Frame izquierdo
        self.frame_p1 = tk.Frame(self, bg="#F5DEB3")
        self.frame_p1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #Frame derecho
        self.frame_p2 = tk.Frame(self, bg="#F5DEB3")
        self.frame_p2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        #Configurar las filas y columnas para que se expandan
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="column")
        self.grid_columnconfigure(1, weight=1, uniform="column")

        #Subframes del frame izquierdo
        self.frame_p3 = tk.Frame(self.frame_p1, bg="white smoke")
        self.frame_p3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.frame_p4 = tk.Frame(self.frame_p1, bg="white smoke")
        self.frame_p4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Configurar las filas y columnas para que se expandan
        self.frame_p1.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p1.grid_rowconfigure(1, weight=3, uniform="row")
        self.frame_p1.grid_columnconfigure(0, weight=1, uniform="column")

        #Subframes del frame derecho
        self.frame_p5 = tk.Frame(self.frame_p2, bg="white smoke")
        self.frame_p5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.frame_p6 = tk.Frame(self.frame_p2, bg="white smoke")
        self.frame_p6.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        #Configurar las filas y columnas para que se expandan
        self.frame_p2.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p2.grid_rowconfigure(1, weight=3, uniform="row")
        self.frame_p2.grid_columnconfigure(0, weight=1, uniform="column")

        #Creación de los widgets de cada frame

        #Elementos de frame_p3
        self.label_saludo = tk.Label(self.frame_p3, textvariable=self.variable_Saludo, bg="white smoke", fg="black", font=("Eras Light ITC", 18))
        self.label_saludo.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.frame_p3.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p3.grid_columnconfigure(0, weight=1, uniform="column")

        # Elementos de frame_p4
        self.label_fotos_sistema = tk.Label(self.frame_p4, bg="#F5DEB3")
        self.label_fotos_sistema.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.boton_ventana_principal = tk.Button(self.frame_p4, text="Abrir la Ventana Principal", bg="old lace",
                                                 font=("Candara", 12), activebackground="#FFDAB9",
                                                 command=self.abrirVentanaPrincipal,
                                                 cursor="hand2")
        self.boton_ventana_principal.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.frame_p4.grid_rowconfigure(0, weight=15)
        self.frame_p4.grid_rowconfigure(1, weight=1)
        self.frame_p4.grid_columnconfigure(0, weight=1)

        # Elementos de frame_p5
        self.label_nombre_desarrolladores = tk.Label(self.frame_p5, textvariable=self.variable_nombres, bg="white smoke",
                                                     fg="black",font=("Eras Light ITC", 18))
        self.label_nombre_desarrolladores.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

        self.label_HDV = tk.Text(self.frame_p5, bg="white smoke", fg="black",
                                  font=("Candara", 12), cursor="hand2")
        self.label_HDV.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.label_HDV.config(state='normal')
        self.label_HDV.insert(1.0, """Conoce a nuestros desarrolladores\nHaz clic aquí para ver sus hojas de vida""")
        self.label_HDV.config(state='disabled')

        # Configurar las filas y columnas para que se expandan
        self.frame_p5.grid_rowconfigure(0, weight=1, uniform="row")
        self.frame_p5.grid_rowconfigure(1, weight=5, uniform="row")
        self.frame_p5.grid_columnconfigure(0, weight=1, uniform="column")

        # Elementos de frame_p6
        self.label_foto1 = tk.Label(self.frame_p6, bg="#F5DEB3")
        self.label_foto1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.label_foto2 = tk.Label(self.frame_p6, bg="#F5DEB3")
        self.label_foto2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.label_foto3 = tk.Label(self.frame_p6, bg="#F5DEB3")
        self.label_foto3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.label_foto4 = tk.Label(self.frame_p6, bg="#F5DEB3")
        self.label_foto4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Configurar las filas y columnas para que se expandan
        self.frame_p6.grid_rowconfigure(0, weight=1)
        self.frame_p6.grid_rowconfigure(1, weight=1)
        self.frame_p6.grid_columnconfigure(0, weight=1)
        self.frame_p6.grid_columnconfigure(1, weight=1)

    def asignarMetodos(self):
        """
        Método que asigna los métodos a los eventos de los widgets.
        """
        self.label_HDV.bind("<Button-1>", self.cambiarHDV)
        self.label_fotos_sistema.bind("<Leave>", self.cambiarFotosSistema)

    def crearMenu(self):
        """
        Método que crea el menú de la ventana de inicio.
        """
        # Creación de la barra de menú
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu_opciones = tk.Menu(self.menu_bar, tearoff=0, bg="old lace", activebackground="#FFDAB9", activeforeground="black",font=("Candara Light", 12))
        self.menu_bar.add_cascade(label="Inicio", menu=self.menu_opciones, font=("Candara", 12))

        # Creación de las opciones del menú
        self.menu_opciones.add_command(label="Salir", command=self.salir, font=("Candara", 12))
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label="Descripción", command=self.descripcionSistema, font=("Candara", 12))

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# -------------------------------------------METODOS EXTRA--------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

    def cambiarHDV(self, evento):
        """
        Método que cambia la hoja de vida de los desarrolladores, asigna el nombre y muestra 4 fotos de cada uno.
        """
        self.indice_HDV += 1
        self.indice_HDV %= 3

        self.variable_nombres.set(self.nombres[self.indice_HDV - 1])

        self.label_HDV.config(state='normal')
        self.label_HDV.delete(1.0, tk.END)
        self.label_HDV.insert(tk.END, self.hojas_vida[self.indice_HDV - 1])
        self.label_HDV.config(state='disabled')

        grupo_fotos = self.ruta_fotos_desarrolladores[self.indice_HDV - 1]
        self.fotos_HDV = []

        for i, ruta in enumerate(grupo_fotos):
            imagen = Image.open(ruta)

            # Obtén las dimensiones del Label
            label = getattr(self, f'label_foto{i + 1}')
            label.update_idletasks()  # Asegurarse de que las dimensiones sean correctas
            width = label.winfo_width()
            height = label.winfo_height()

            # Redimensiona la imagen para que se ajuste al Label
            imagen.thumbnail((width, height), Image.LANCZOS)
            self.fotos_HDV.append(ImageTk.PhotoImage(imagen))

        self.label_foto1.config(image=self.fotos_HDV[0])
        self.label_foto2.config(image=self.fotos_HDV[1])
        self.label_foto3.config(image=self.fotos_HDV[2])
        self.label_foto4.config(image=self.fotos_HDV[3])

    def cambiarFotosSistema(self, evento):
        """
        Método que cambia las fotos relacionadas con el sistema.
        """
        self.indice_fotos += 1
        self.indice_fotos %= len(self.ruta_fotos_sistema)

        imagen = Image.open(self.ruta_fotos_sistema[self.indice_fotos])

        # Obtén las dimensiones del Label
        label = getattr(self, 'label_fotos_sistema')
        label.update_idletasks()  # Asegurarse de que las dimensiones sean correctas
        width = label.winfo_width()
        height = label.winfo_height()

        # Redimensiona la imagen para que se ajuste al Label
        imagen = imagen.resize((width, height), Image.LANCZOS)

        self.foto_sistema = ImageTk.PhotoImage(imagen)
        self.label_fotos_sistema.config(image=self.foto_sistema)

    def abrirVentanaPrincipal(self):
        """
        Método que abre la ventana principal del usuario.
        """
        self.withdraw()  # O puedes usar self.iconify() para minimizar
        ventana_principal = VentanaPrincipalDeUsuario(self)

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# -------------------------------GESTIONAR FUNCIONALIDADES DEL MENU-----------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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
        self.variable_Saludo.set("""A través de esta aplicación podrás registrarte,\nplanear tu viaje, gestionar tus grupos y destinos,\nreservar actividades, y manejar tu hospedaje.\nAdemás, ofrecemos beneficios exclusivos\ncomo descuentos.""")

if __name__ == "__main__":
    app = VentanaInicio()
    app.mainloop()