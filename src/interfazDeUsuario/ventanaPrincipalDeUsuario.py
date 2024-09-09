import sys
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Ajustar las rutas para las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'clases')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modulos')))

# Importar clases 
from clases.menu import Menu
from clases.pdfViewer import PdfViewer

# Importar modulos
from modulos.verOpcionesDeAdministrador import opcionesAdministrador
from modulos.reservarActividades import reservarActividades
from modulos.reservarHospedaje import reservarHospedaje
from modulos.planearViaje import planearViaje
from modulos.modificarReserva import modificarReserva

class VentanaPrincipalDeUsuario(tk.Tk):
    """
    Clase que representa la ventana principal de la aplicación de gestión de actividades turísticas.
    Hereda de tk.Tk para crear una interfaz gráfica de usuario utilizando Tkinter.
    """

    def __init__(self):
        """
        Inicializa la ventana principal, configura el título, icono, fondo, y crea los frames necesarios.
        """
        super().__init__()
        self.title("Ventana principal de usuario")
        self.iconbitmap("archivos\\perroLogo.ico")
        self.config(bg="white smoke")
        self.resizable(width=False, height=True)

        # Configuración del layout de la ventana principal
        self.columnconfigure(0, weight=1)  # Permite que la columna 0 se expanda
        self.rowconfigure(2, weight=1)  # Fila para el frame de contenido

        # Inicializar atributos
        self.opciones_menu = ["Archivo", "Procesos y consultas", "Ayuda"]
        self.submenus = [
            ["Aplicación", "Salir"],
            ["Reservar actividades turísticas", "Reservar hospedaje", "Planear tu viaje", 
             "Modificar reserva", "Ver opciones de administrador"],
            ["Acerca de"]
        ]
        self.interfaz = True
        
        # Crear frames anidados
        self.crearFrames()
        
    def crearFrames(self):
        """
        Crea los frames necesarios para la interfaz gráfica, incluyendo el frame del título, el menú y el frame de interacción del usuario.
        """
        # Zona 0: Frame para el título
        self.titulo_frame = tk.Frame(self, bg="white smoke", height=50, padx=10)
        self.titulo_frame.grid(row=0, column=0, sticky="nsew", padx=10)

        # Titulo
        self.logo_image = tk.PhotoImage(file="archivos\\logoMontaña.png")  # Añadir la imagen al título_frame
        self.logo_label = tk.Label(self.titulo_frame, image=self.logo_image, bg="white smoke", padx=5)
        self.logo_label.grid(row=0, column=0, padx=5, sticky="w")

        self.titulo_label = tk.Label(self.titulo_frame, bg="white smoke", text="Gestión de actividades turísticas", font=("Candara Light", 12))
        self.titulo_label.grid(row=0, column=1, pady=10)  # Añadir un título dentro del titulo_frame
        
        # Zona 1: Frame para los menús
        self.menu_frame = tk.Frame(self, height=30, bg="white", padx=10)
        self.menu_frame.grid(row=1, column=0, sticky="ew", padx=10)
        self.menu_frame.grid_rowconfigure(0, weight=1)
        
        menu = Menu(self.menu_frame, self, self.opciones_menu, self.submenus)  # Crear menú
        menu.grid(row=0, column=0, sticky="new", padx=0, pady=10)

        # Zona 2: Frame para la interacción del usuario
        self.interaccion_usuario_frame = tk.Frame(self, bg="white", padx=10, pady=15)
        self.interaccion_usuario_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=15)
        self.interaccion_usuario_frame.grid_rowconfigure(0, weight=1)
        self.interaccion_usuario_frame.grid_columnconfigure(0, weight=1)
        self.interfazInicio(False)  # Interfaz de inicio

    def interfazInicio(self, opcion):
        """
        Configura la interfaz de inicio o destruye la interfaz de inicio actual.
        
        :param opcion (boolean): Si es False, crea la interfaz de inicio; si es True, destruye la interfaz de inicio.
        """
        if not opcion:  # Crear interfaz de inicio
            # Destruir widgets de funcionalidades
            for widget in ['interaccion_label', 'interaccion_texto', 'procesosYConsultas_frame', 'resultados_frame', 'resultados_texto']:
                if hasattr(self, widget) and getattr(self, widget).winfo_exists():
                    getattr(self, widget).destroy()
                    
            self.imagen_fondo = tk.PhotoImage(file="archivos\\fondo.png")  # Cargar la imagen de fondo
            self.canvas = tk.Canvas(self.interaccion_usuario_frame, width=800, height=459, bg="white", highlightthickness=0)
            self.canvas.grid(row=0, column=0, sticky="nsew")  # Hacer que el canvas se expanda
            self.canvas.update_idletasks()  # Ajustar el tamaño del canvas según la ventana
            self.canvas.create_image(0, 0, anchor="nw", image=self.imagen_fondo)  # Añadir la imagen al canvas
            
            self.text_frame = tk.Frame(self.canvas, bg="white")  # Crear un Frame sobre el canvas para las etiquetas
            self.canvas.create_window(800 // 2, 459 // 2, window=self.text_frame, anchor="center")
            self.text_frame.grid_columnconfigure(0, weight=1)
                
            self.interaccion_bienvenida = tk.Label(self.text_frame, text="WELCOME TO", bg="white", fg="black", font=("Eras Light ITC", 25))
            self.interaccion_bienvenida.grid(row=0, column=0, padx=10, sticky="nsew")  # Etiqueta de título
            self.interaccion_titulo = tk.Label(self.text_frame, text="INTERFAZ DE INICIO", bg="white", fg="black", font=("Eras Light ITC", 10))
            self.interaccion_titulo.grid(row=1, column=0, padx=10, sticky="nsew")  # Etiqueta de título
            self.interaccion_text = tk.Label(self.text_frame, bg="white", text="Bienvenido a nuestra plataforma de turismo y recreación.\n\nA través de nuestra aplicación, podrás disfrutar de experiencias únicas y personalizadas en el destino de tus sueños.\nNos encargamos de organizar todo: desde tu registro y hospedaje hasta la planificación y reserva de actividades.\nAdemás, ofrecemos descuentos exclusivos y te conectamos con guías altamente capacitados para que vivas cada aventura al máximo.\n\nRelájate en los mejores restaurantes y hospedajes, mientras nosotros nos ocupamos de los detalles.", fg="black", font=("Candara Light", 12), wraplength=500)
            self.interaccion_text.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")  # Etiqueta de texto
            
        else:  # Destruir interfaz de inicio
            self.canvas.destroy()
            self.interfaz = False
            self.text_frame.destroy()
            self.interaccion_usuario_frame.grid_rowconfigure(0, weight=0)
            self.interaccion_label = tk.Label(self.interaccion_usuario_frame, width=80, bg="white smoke", fg="black", font=("Candara Light", 15))
            self.interaccion_label.grid(row=0, column=0, sticky="new", padx=0, pady=0)  # Etiqueta de título
            self.interaccion_texto = tk.Label(self.interaccion_usuario_frame, bg="white", fg="black", font=("Candara Light", 11))
            self.interaccion_texto.grid(row=1, column=0, sticky="new", padx=0, pady=5)  # Etiqueta de texto
            
            self.procesosYConsultas_frame = tk.Frame(self.interaccion_usuario_frame, bg="white smoke", padx=10, pady=15)
            self.procesosYConsultas_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
            self.procesosYConsultas_frame.grid_columnconfigure(0, weight=1)
            
            self.resultados_texto = tk.Label(self.interaccion_usuario_frame, bg="white", fg="black", font=("Candara Light", 14))
            self.resultados_texto.grid(row=4, column=0, sticky="new", padx=0, pady=0)
            self.resultados_frame = tk.Frame(self.interaccion_usuario_frame, bg="white", padx=10, pady=15)
            self.resultados_frame.grid(row=5, column=0, sticky="nsew", padx=10, pady=0)
            self.resultados_frame.grid_columnconfigure(0, weight=1)
             
    def handleSubmenu(self, option):
        """
        Maneja la selección de opciones del submenú y llama a la función correspondiente.
        
        :param   option (str): Opción seleccionada del submenú.
        """
        # Funciones para manejar las opciones de los submenús
        if option == "Aplicación":
            self.aplicacion()
        elif option == "Salir":
            self.salir()
        elif option == "Reservar actividades turísticas":
            reservarActividades(self)
        elif option == "Reservar hospedaje":
            reservarHospedaje(self)
        elif option == "Planear tu viaje":
            planearViaje(self)
        elif option == "Modificar reserva":
            modificarReserva(self)
        elif option == "Ver opciones de administrador":
            opcionesAdministrador(self)
        elif option == "Acerca de":
            self.acerca_de()
            
    def destruirInterfazProcesos(self):
        """
        Destruye los widgets de la interfaz de procesos si está activa.
        """
        if self.interfaz:
            self.interfazInicio(True)
        else:
            self.borrarFrame(self.procesosYConsultas_frame)
            self.borrarFrame(self.resultados_frame)
   
    def terminarFuncionalidad(self, opcion, metodo):
        """
        Termina la funcionalidad actual y puede volver al inicio de la funcionalidad o destruir la interfaz de procesos.
        
        :param    opcion (str): Opción seleccionada para volver al inicio o destruir la interfaz de procesos.
        :param    metodo (function): Método para volver al inicio de la funcionalidad.
        """
        if opcion == "Volver al inicio de la funcionalidad":
            metodo(self)
        else:
            self.destruirInterfazProcesos()
            self.interfazInicio(False)
                
    def borrarFrame(self, frame):
        """
        Destruye todos los widgets dentro de un frame.
        
        :param  frame (tk.Frame): Frame cuyo contenido debe ser destruido.
        """
        for widget in frame.winfo_children():
            widget.destroy()
               
    def aplicacion(self):
        """
        Muestra la información de la aplicación desde un archivo de texto en un cuadro de mensaje.
        """
        with open("archivos\\informacion_aplicacion.txt", "r", encoding="utf-8") as file:
            texto_informacion = file.read()
        messagebox.showinfo("Información de la aplicación", texto_informacion)

    def salir(self):
        """
        Cierra la ventana principal de usuario después de confirmar con el usuario.
        """
        valor_salida = messagebox.askokcancel("Salir", "¿Deseas volver a la ventana de inicio?")
        
        if valor_salida:
            self.destroy()

    def acerca_de(self):
        """
        Muestra el manual de usuario de la aplicación en un visor de PDF.
        """
        PdfViewer(self, "archivos\\manualDeUsuario.pdf", "Manual de usuario de la aplicación")

# Ejecución de la aplicación
if __name__ == "__main__":
    app = VentanaPrincipalDeUsuario()
    app.mainloop()
