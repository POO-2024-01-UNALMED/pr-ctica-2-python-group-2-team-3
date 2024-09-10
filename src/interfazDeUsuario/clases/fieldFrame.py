import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from modulos.excepciones import *  # Asegúrate de tener estas excepciones definidas

class FieldFrame(tk.Frame):
    """
    FieldFrame es una clase que extiende tk.Frame y permite crear un frame personalizable
    para diferentes tipos de selección: única (Radiobutton), múltiple (Checkbutton) o 
    entrada de texto (Entry).
    """
    
    def __init__(self, parent, tipo_formulario, on_accept, frame_resultado=False, tituloCriterios=None, tituloValores=None, criterios=None, valores=None, habilitado=None, verificaciones=None):
        """
        :param parent (tk.Frame): Frame padre donde se inserta FieldFrame.
        :param tipo_formulario (int): Tipo de formulario a crear (0: Unica opcion de respuesta, 1: Multiples opciones de respuesta, 2: Maximo dos opciones,  3: Entrada de texto)
        :param on_accept (function): Metodo event handler
        :param frame_resultado (boolean): True si es un frame de resultado o false si es un frame de formulario
        :param tituloCriterios (str): Texto para el título de los criterios (usado en tipo 2).
        :param tituloValores (str): Texto para el título de los valores o para la pregunta en (opcion 0 y 1)
        :param criterios (list[str]): Lista de criterios (usado en tipo 2).
        :param valores (list[str]): Lista de valores disponibles para selección o entrada.
        :param habilitado (list[boolean]): Lista de booleanos para habilitar o deshabilitar los campos.
        :param verificaciones (list[(str,funtion)]): arreglo de tuplas de la forma [("Critreio","funcion"),...] (criterio: es el criterio que debe cumplir con el parametro,
        funcion: es la funcion que se encarga de verificar si se cumple el parametro que recibe como parametro la seleccion)
        """
        super().__init__(parent)
        self.tipo_formulario = tipo_formulario
        self.on_accept = on_accept
        self.criterios = criterios or []
        self.valores = valores if valores is not None else ["" for _ in self.criterios]  # Inicializar valores si es None
        self.habilitado = habilitado if habilitado is not None else [True for _ in self.valores]  # Inicializar habilitado si es None
        self.verificaciones = verificaciones
        self.config(bg="white smoke")
        
        self.entriesResultados = []
        if frame_resultado:
            self.habilitado = [False for _ in self.valores]
            
        # Crea el frame adecuado según el tipo de opción
        if self.tipo_formulario == 0:
            self.crearUnicaOpcionFrame(tituloValores)
        elif self.tipo_formulario in [1, 2]:
            self.crearMultipleOpcionFrame(tituloValores)
        elif self.tipo_formulario == 3:
            self.crearFieldFrame(tituloCriterios, tituloValores)
        
        # Creación de los botones Aceptar y Borrar
        if not frame_resultado:
            self.crearBotones()

    def crearUnicaOpcionFrame(self, titulo):
        """
        Crea un formulario de selección única usando Combobox.
        
        :param titulo(str): Texto para el título del grupo de opciones.
        """
        tk.Label(self, text=titulo, bg="white smoke", font=("Candara Light", 13)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.selected_value = tk.StringVar()

        self.widgets = {}

        # Definir el estilo para el Combobox
        style = ttk.Style()
        style.configure("TCombobox", font=("Candara Light", 18))

        # Creación del Combobox en dos columnas
        self.combobox = ttk.Combobox(self, textvariable=self.selected_value, values=self.valores, state="readonly" if self.habilitado[0] else "disabled", style="TCombobox")
        self.combobox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.widgets["seleccion"] = self.combobox

    def crearMultipleOpcionFrame(self, titulo):
        """
        Crea un formulario de selección múltiple usando Combobox y utiliza un boton de añadir para seleccionar las opciones.
        
        :param titulo(str): Texto para el título del grupo de opciones.
        """
        tk.Label(self, text=titulo, bg="white smoke", font=("Candara Light", 13)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.widgets = {}
        self.seleccionados = []

        # Definir el estilo para el Combobox
        style = ttk.Style()
        style.configure("TCombobox", font=("Candara Light", 18))

        # Creación del Combobox en dos columnas
        self.combobox = ttk.Combobox(self, values=self.valores, state="readonly", style="TCombobox")
        self.combobox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        add_btn = tk.Button(self, text="Añadir",bg="white smoke", font=("Candara Light", 10), command=self.añadirSeleccion)
        add_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Etiqueta para mostrar opciones seleccionadas y los Entries debajo
        self.seleccion_label = tk.Label(self, text="Opciones seleccionadas: ", bg="white smoke", font=("Candara Light", 13))
        self.seleccion_label.grid(row=3, column=0, padx=5, pady=10, sticky="w")

    def añadirSeleccion(self):
        """
        Función que maneja la acción del botón de añadir, Añade la opción seleccionada al listado de opciones
        seleccionadas cuando se oprime el boton de añadir.
        """
        seleccion = self.combobox.get()
        if seleccion and seleccion not in self.seleccionados:
            try:
                if self.tipo_formulario == 2 and len(self.seleccionados) >= 2:
                    raise MaximoDosOpcionesError(self.seleccionados)
                self.seleccionados.append(seleccion)
                self.mostrarSeleccionAñadida()
            except ErrorFormulario as e:
                messagebox.showerror("Error", str(e))    

    def mostrarSeleccionAñadida(self):
        """
        Muestra las opciones añadidas mediante entries con los valores seleccionados desabilitados.
        """
        # Crear un entry para cada selección
        for idx, seleccion in enumerate(self.seleccionados):
            entry = tk.Entry(self, font=("Candara Light", 13))
            entry.grid(row=4 + idx, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            entry.insert(0, seleccion)
            entry.config(state="disabled")  # Deshabilitar edición
            # Añadir a la lista de entries creados
            self.entriesResultados.append(entry)

    def crearFieldFrame(self, titulo_criterios, titulo_valores):
        """
        Crea un frame con campos de entrada de texto usando Entry.
        
        :param titulo_criterios (str): Texto para el título de los criterios.
        :param titulo_valores (str): Texto para el título de los valores.
        """
        tk.Label(self, text=titulo_criterios, bg="white smoke", font=("Candara Light", 13)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self, text=titulo_valores, bg="white smoke", font=("Candara Light", 13)).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.entries = {}
        
        # Creación de los campos Entry
        for i, criterio in enumerate(self.criterios):
            tk.Label(self, text=criterio, bg="white smoke", font=("Candara Light", 13)).grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self, font=("Candara Light", 13))
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")
            entry.insert(0, self.valores[i] if self.valores and self.valores[i] is not None else "")
            entry.config(state="disabled" if not self.habilitado[i] else "normal")
            self.entries[criterio] = entry
            

    def crearBotones(self):
        """
        Crea los botones de Aceptar y Borrar en el frame con un tamaño fijo.
        """
        botones_frame = tk.Frame(self)
        botones_frame.grid(row=100, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Crear el botón de "Aceptar" con un tamaño fijo
        aceptar_btn = tk.Button(botones_frame, text="Aceptar", bg="white smoke", font=("Candara Light", 13), command=self.aceptar, width=10)
        aceptar_btn.grid(row=0, column=0, padx=5, pady=5)

        # Crear el botón de "Borrar" con un tamaño fijo
        borrar_btn = tk.Button(botones_frame, text="Borrar", bg="white smoke", font=("Candara Light", 13), command=self.borrar, width=10)
        borrar_btn.grid(row=0, column=1, padx=5, pady=5)
    
    def aceptar(self):
        """
        Función que maneja la acción del botón Aceptar, mostrando un mensaje
        con las opciones seleccionadas o los valores ingresados.
        """
        seleccion = None
        
        try:
            if self.tipo_formulario == 0:  # Unica opción
                seleccion = self.getValuesOpciones()
                if seleccion is None or not seleccion:
                    raise OpcionNoSeleccionadaError()
            
            elif self.tipo_formulario in [1, 2]:  # Múltiples opciones
                seleccion = self.getValuesOpciones()
                if seleccion is None or (self.tipo_formulario == 2 and len(seleccion) != 2):
                    raise OpcionNoSeleccionadaError()
            
            elif self.tipo_formulario == 3:  # Entradas de texto
                seleccion = {criterio: self.getValueEntrada(criterio) for criterio in self.entries.keys()}
                campos_incompletos = [criterio for criterio in self.criterios if seleccion[criterio] == ""]
                if campos_incompletos:
                    raise CamposIncompletosError(campos_incompletos)

                # Validación de parámetros
                if self.verificaciones is not None:
                    self.excepciones = self.lanzarExcepcionesEntradaTexto(seleccion) 
                    if self.excepciones:
                        return

            # Si se ha seleccionado o ingresado algo, llamamos al método `on_accept`
            self.on_accept(seleccion)

        except ErrorFormulario as e:
            messagebox.showerror("Error", str(e))
            
    
    def borrar(self):
        """
        Función que maneja la acción del botón Borrar, reseteando los campos
        de selección o entrada a su estado inicial.
        """
        if self.tipo_formulario == 0:
            self.selected_value.set(None)
            self.combobox.set("")
            self.focus()
        elif self.tipo_formulario in [1, 2]:
            self.seleccionados = []
            self.combobox.set("")
            self.focus()
            # Borrar los entries creados
            for entry in self.entriesResultados:
                entry.destroy()
            self.entriesResultados.clear()
        elif self.tipo_formulario == 3:
            for entry in self.entries.values():
                entry.delete(0, tk.END)

    def getValuesOpciones(self):
        """
        Obtiene los valores seleccionados en los Comboboxes.
        
        :return str: Para tipo_opcion 0: El valor seleccionado.
        :return list[str]: Para tipo_opcion 1 y 2: Una lista de valores seleccionados.
        :return None: Para otros tipos o sin selección.
        """
        if self.tipo_formulario == 0:
            return self.widgets["seleccion"].get()
        elif self.tipo_formulario in [1, 2]:
            return self.seleccionados if self.seleccionados else None
    
    def getValueEntrada(self, criterio):
        """
        Obtiene los valores ingresados en los campos de texto (Entry)
        
        :param criterio(str): El criterio del campo a buscar
        :return str: El valor del criterio cuyo nombre es 'criterio'.
        """
        entry = self.entries.get(criterio)
        if entry:
            return entry.get()
        return None

    def añadirCriterioValor(self, criterio, valor):
        """
        Añade un criterio y su respectivo valor al fieldFrame de resultados
        
        :param criterio: nombre del criterio
        :param valor: valor del criterio
        """
        _, numFilas = self.grid_size()
        tk.Label(self, text=criterio, bg="white smoke", font=("Candara Light", 13)).grid(row=numFilas, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(self, font=("Candara Light", 13))
        entry.grid(row=numFilas, column=1, padx=5, pady=5, sticky="ew")
        entry.insert(0, valor)
        entry.config(state="disabled")
        
    def lanzarExcepcionesEntradaTexto(self, seleccion):
        """
        Verifica si se cumplen con todas los parametros requeridos y si no es así se lanza una excepción
        
        :param seleccion (dict): valores ingresados en el entry, de la forma {"Criterio": "Valor"}
        :return boolean: True si se lanzó una excepción o False si no se lanzó ninguna excepción
        """
        # self.verificaciones es de la forma [("Criterio",funcion),...]
        for criterio, funcion in self.verificaciones:
            try:
                funcion(seleccion[criterio])
            except ErrorAplicacion as e:
                messagebox.showerror("Error", str(e))
                return True
        return False

def mostrar_seleccion(seleccion):
    """
    METODO SOLO PARA EJEMPLO
    """
    messagebox.showinfo("Seleccion", f"Selección: {seleccion}")

# Ejemplo de uso del FieldFrame dentro de la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    
    # Crear una instancia de FieldFrame para una única opción (Combobox)
    frame1 = FieldFrame(root, tipo_formulario=0, on_accept=mostrar_seleccion, tituloValores="Elige una opción:", valores=["Opción 1", "Opción 2", "Opción 3"])
    frame1.grid(row=0, column=0, padx=10, sticky="ew")
    
    # Crear una instancia de FieldFrame para múltiples opciones (Combobox)
    frame2 = FieldFrame(root, tipo_formulario=1, on_accept=mostrar_seleccion, tituloValores="Selecciona una o más opciones:", valores=["Opción A", "Opción B", "Opción C"])
    frame2.grid(row=1, column=0, padx=10, sticky="ew")
    
    # Crear una instancia de FieldFrame para SOLO dos opciones (Combobox)
    frame3 = FieldFrame(root, tipo_formulario=2, on_accept=mostrar_seleccion, tituloValores="Selecciona solo dos opciones:", valores=["Opción A", "Opción B", "Opción C"])
    frame3.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
    
    # Crear una instancia de FieldFrame para criterios y valores (Entry)
    frame4 = FieldFrame(root, tipo_formulario=3, on_accept=mostrar_seleccion, tituloCriterios="Criterios:", tituloValores="Valores:", criterios=["Criterio 1", "Criterio 2"], valores=["Valor 1", "Valor 2"], verificaciones=[("Criterio 1", lambda seleccion: verificarFormato(seleccion, "Criterio 1", 0))])
    frame4.grid(row=3, column=0, padx=10, sticky="ew")
 
    # Crear una instancia de FieldFrame para criterios y valores para resultados
    frame5 = FieldFrame(root, tipo_formulario=3, on_accept=mostrar_seleccion, frame_resultado=True, tituloCriterios="Criterios:", tituloValores="Valores:", criterios=["Criterio 1", "Criterio 2"], valores=["Valor 1", "Valor 2"])
    frame5.grid(row=4, column=0, padx=10, sticky="ew")
    frame5.añadirCriterioValor("Hola", "Adios")
    
    root.mainloop()
