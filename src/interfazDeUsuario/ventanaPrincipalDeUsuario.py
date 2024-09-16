import sys
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Ajustar las rutas para las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'clases')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modulos')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gestorAplicacion')))

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

class VentanaPrincipalDeUsuario(tk.Toplevel):
    """
    Clase que representa la ventana principal de la aplicación de gestión de actividades turísticas.
    Hereda de tk.Tk para crear una interfaz gráfica de usuario utilizando Tkinter.
    """
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# -------------------------------------CREAR LA VENTANA DE USUARIO------------------------------------
# ----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
    def __init__(self, parent):
        """
        Inicializa la ventana principal, configura el título, icono, fondo, y crea los frames necesarios.
        """
        super().__init__(parent)
        self.title("Ventana principal de usuario")
        self.iconbitmap("archivos\\perroLogo.ico")
        self.config(bg="white smoke")
        self.resizable(width=False, height=False)
        self.geometry("1450x800+35+0")

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
            self.borrarFrame(self.interaccion_usuario_frame)
                    
            self.imagen_fondo = tk.PhotoImage(file="archivos\\fondo.png")  # Cargar la imagen de fondo
            self.canvas = tk.Canvas(self.interaccion_usuario_frame,width=1450,height=635, bg="white", highlightthickness=0)
            self.canvas.grid(row=0, column=0, sticky="nsew")  # Hacer que el canvas se expanda
            self.canvas.update_idletasks()  # Ajustar el tamaño del canvas según la ventana
            self.canvas.create_image(0, 0, anchor="nw", image=self.imagen_fondo)  # Añadir la imagen al canvas
            
            self.text_frame = tk.Frame(self.canvas, bg="white")  # Crear un Frame sobre el canvas para las etiquetas
            self.canvas.create_window(700, 300, window=self.text_frame, anchor="center")
            self.text_frame.grid_columnconfigure(0, weight=1)
                
            self.interaccion_bienvenida = tk.Label(self.text_frame, text="WELCOME TO", bg="white", fg="black", font=("Eras Light ITC", 25))
            self.interaccion_bienvenida.grid(row=0, column=0, padx=20, sticky="nsew")  # Etiqueta de título
            self.interaccion_titulo = tk.Label(self.text_frame, text="INTERFAZ DE INICIO", bg="white", fg="black", font=("Eras Light ITC", 10))
            self.interaccion_titulo.grid(row=1, column=0, padx=20, sticky="nsew")  # Etiqueta de título
            self.interaccion_text = tk.Label(self.text_frame, bg="white", text="Bienvenido a nuestra plataforma de turismo y recreación.\n\nA través de nuestra aplicación, podrás disfrutar de experiencias únicas y personalizadas en el destino de tus sueños.\nNos encargamos de organizar todo: desde tu registro y hospedaje hasta la planificación y reserva de actividades.\nAdemás, ofrecemos descuentos exclusivos y te conectamos con guías altamente capacitados para que vivas cada aventura al máximo.\n\nRelájate en los mejores restaurantes y hospedajes, mientras nosotros nos ocupamos de los detalles.", fg="black", font=("Candara Light", 12), wraplength=500)
            self.interaccion_text.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")  # Etiqueta de texto
            
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
            self.resultados_texto.grid(row=4, column=0, sticky="new")
            self.resultados_frame = tk.Frame(self.interaccion_usuario_frame, bg="white", padx=10, pady=15)
            self.resultados_frame.grid(row=5, column=0, sticky="nsew", padx=10)
            self.resultados_frame.grid_columnconfigure(0, weight=1)

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# -------------------------------GESTIONAR FUNCIONALIDADES DEL MENU-----------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
            
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
            self.abrirVentanaInicio()

    def abrirVentanaInicio(self):
        """
        Método para abrir nuevamente la VentanaInicio.
        """
        self.master.deiconify()
        self.destroy()

    def acerca_de(self):
        """
        Muestra el manual de usuario de la aplicación en un visor de PDF.
        """
        PdfViewer(self, "archivos\\manualDeUsuario.pdf", "Manual de usuario de la aplicación")

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# -------------------------------------------METODOS EXTRA--------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

    def destruirInterfazProcesos(self):
        """
        Destruye los widgets de la interfaz de procesos si está activa.
        """
        if self.interfaz:
            self.interfazInicio(True)
        else:
            self.borrarFrame(self.procesosYConsultas_frame)
            self.borrarFrame(self.resultados_frame)
            self.resultados_frame.grid_forget()
            self.resultados_texto.grid_forget()
            

    def terminarFuncionalidad(self, opcion, metodo):
        """
        Termina la funcionalidad actual y permite volver al inicio o destruir la interfaz de procesos.

        :param opcion(str): Opción seleccionada para volver al inicio o destruir la interfaz.
        :param metodo(function): Método que se ejecutará para volver al inicio de la funcionalidad.
        """
        if opcion == "Volver al inicio de la funcionalidad":
            metodo()
        else:
            self.destruirInterfazProcesos()
            self.interfazInicio(False)

    def borrarFrame(self, frame):
        """
        Destruye todos los widgets dentro de un frame.

        :param frame(tk.Frame): Frame cuyo contenido debe ser destruido.
        """
        for widget in frame.winfo_children():
            widget.destroy()

    def modificarTitulo(self, texto):
        """
        Modifica el título de la sección de interacción.

        :param texto(str): El nuevo texto para el título.
        """
        self.interaccion_label.config(text=texto)

    def modificarTexto(self, texto):
        """
        Modifica el texto de la sección de interacción.

        :param texto(str): El nuevo texto para la interacción.
        """
        self.interaccion_texto.config(text=texto)

    def crearFormulario(self, tipo_formulario, on_accept, tituloCriterios=None, tituloValores=None, criterios=None, valores=None, habilitado=None, verificaciones=None):
        """
        Crea un formulario basado en los parámetros proporcionados y lo agrega a la interfaz.

        :param tipo_formulario(int): Tipo de formulario que se creará (0, 1, 3, etc.).
        :param on_accept(function): Función que se ejecuta al aceptar el formulario.
        :param tituloCriterios(str): Título para la columna de criterios.
        :param tituloValores(str): Título para la columna de valores.
        :param criterios(list): Lista de criterios a mostrar en el formulario.
        :param valores(list): Lista de valores que se mostrarán en el formulario.
        :param habilitado(list): Lista de booleanos indicando si los campos están habilitados o no.
        :param verificaciones(list): Lista de tuplas para verificar los datos ingresados.
        """
        if tipo_formulario == 3:
            tituloCriterios = "Criterios"
            tituloValores = "Valores"
        
        formulario_frame = FieldFrame(self.procesosYConsultas_frame, tipo_formulario=tipo_formulario, on_accept=on_accept, tituloCriterios=tituloCriterios, tituloValores=tituloValores, criterios=criterios, valores=valores, habilitado=habilitado, verificaciones=verificaciones)
        formulario_frame.pack(padx=10, pady=5)

    def tituloResultados(self):
        """
        Cambia el texto para indicar que se mostrarán los resultados.
        """
        self.resultados_texto.grid(row=4, column=0, sticky="new")
        self.resultados_texto.config(text="Resumen de la información ingresada:")
        
    def frameResultados(self, criterios, valores):
        """
        Muestra los resultados en un frame.

        :param criterios(list): Lista de criterios que se mostrarán.
        :param valores(list): Lista de valores correspondientes a los criterios.
        """
        habilitado = [False for _ in valores]
        self.resultados_frame.grid(row=5, column=0, sticky="nsew", padx=10)
        self.fieldResultado_frame = FieldFrame(self.resultados_frame, tipo_formulario=3, frame_resultado=True, criterios=criterios, tituloCriterios="Criterios", tituloValores="Valores:",  valores=valores, habilitado=habilitado )
        self.fieldResultado_frame.pack(padx=10, pady=5)
        self.fieldResultado_frame.config(bd=5, relief="ridge", highlightbackground="lightGray")

    def añadirResultado(self, criterio, valor):
        """
        Añade un criterio y valor al frame de resultados.

        :param criterio(str): El criterio a añadir.
        :param valor(str): El valor correspondiente al criterio.
        """
        self.fieldResultado_frame.añadirCriterioValor(criterio, valor)

    def borrarResultados(self, texto):
        """
        Borra los resultados actuales y muestra un texto de confirmación.

        :param texto(str): Texto que se mostrará tras borrar los resultados.
        """
        self.borrarFrame(self.resultados_frame)
        self.text_procesosYConsultas = tk.Label( self.procesosYConsultas_frame, text=texto, width=80, bg="white smoke",  fg="black", font=("Candara Light", 15) )
        self.text_procesosYConsultas.pack()

    def frameResumen(self, lista, metodoSalida):
        """
        Crea un frame que muestra un resumen de los datos ingresados y opciones para salir o reiniciar.

        :param lista(list): Lista de tuplas con los criterios y valores que se mostrarán.
        :param metodoSalida(function): Método que se ejecutará cuando el usuario elija salir o reiniciar.
        """
        criterios = [tupla[0] for tupla in lista]
        valores = [tupla[1] for tupla in lista]
        habilitado = [False for _ in valores]
        
        resumen_frame = FieldFrame(self.procesosYConsultas_frame, tipo_formulario=3, frame_resultado=True, criterios=criterios, valores=valores,habilitado=habilitado)
        resumen_frame.pack(padx=10)
        
        self.frameSalida(metodoSalida)
    
    def frameSalida(self,metodoSalida):
        salida_frame = FieldFrame(self.resultados_frame, tipo_formulario=0, on_accept=lambda seleccion: self.terminarFuncionalidad(opcion=seleccion, metodo=metodoSalida), tituloValores="¿Que desea hacer?", valores=["Volver al inicio de la funcionalidad", "Salir"])
        salida_frame.pack(padx=10) 
        self.resultados_texto.grid(row=4, column=0, sticky="new")
        self.resultados_frame.grid(row=5, column=0, sticky="nsew", padx=10)
        self.resultados_frame.config(bg="white smoke")
        self.resultados_texto.config(text="¡Gracias por utilizar la aplicación, vuelva pronto!") 
        
    def crearTabla(self, encabezado, titulo_columnas, filtros, on_filtro, eleccion=None, on_eleccion=None):
        self.tabla_frame=Tabla(self.procesosYConsultas_frame, encabezado=encabezado, titulo_columnas=titulo_columnas, filtros=filtros, on_filtro=on_filtro,eleccion=eleccion, on_eleccion=on_eleccion)
        self.tabla_frame.pack(padx=10, pady=5)
        
    def añadirFila(self,valores):
        self.tabla_frame.añadirFila(valores)
    
    def borrarFilas(self):
        self.tabla_frame.borrarFilas()
    
    def frameImagen(self):
        self.imagen_frame = tk.Frame(self.procesosYConsultas_frame, bg="white smoke")
        self.image = tk.PhotoImage(file="archivos\\imagenGuia.png") 
        self.logo_label = tk.Label(self.procesosYConsultas_frame, image=self.image, bg="white smoke", padx=5)
        self.logo_label.grid(row=0, column=0, padx=5, sticky="ew")
  
# Ejecución de la aplicación
if __name__ == "__main__":
    app = VentanaPrincipalDeUsuario()
    app.mainloop()
