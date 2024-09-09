import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from modulos.excepciones import *
import re

class FieldFrame(tk.Frame):
    """
    FieldFrame es una clase que extiende tk.Frame y permite crear un frame personalizable
    para diferentes tipos de selección: única (Radiobutton), múltiple (Checkbutton) o 
    entrada de texto (Entry).
    """
    
    def __init__(self, parent, tipo_formulario, on_accept,frame_resultado=False, tituloCriterios=None, tituloValores=None, criterios=None, valores=None, habilitado=None,verificaciones=None):
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
        self.on_accept=on_accept
        self.criterios = criterios or []
        self.valores = valores if valores is not None else ["" for _ in self.criterios]  # Inicializar habilitado si es None
        self.habilitado = habilitado if habilitado is not None else [True for _ in self.valores]  # Inicializar habilitado si es None
        self.verificaciones=verificaciones
        self.config(bg="white smoke")
        
        if frame_resultado:
            self.habilitado=[False for _ in self.valores]
            
        # Crea el frame adecuado según el tipo de opción
        if self.tipo_formulario == 0:
            self.crearUnicaOpcionFrame(tituloValores)
        elif self.tipo_formulario in [1, 2]:
            self.crearMultipleOpcionFrame(tituloValores)
        elif self.tipo_formulario == 3:
            self.crearFieldFrame(tituloCriterios, tituloValores)
        
        # Creación de los botones Aceptar y Borrar
        if not frame_resultado:
            self.crearBotones(len(self.valores))

    def crearUnicaOpcionFrame(self, titulo):
        """
        Crea un frame con opciones de selección única usando Radiobuttons.
        
        :param titulo (str): Texto para el título del grupo de opciones.
        """
        tk.Label(self, text=titulo,bg="white smoke", font=("Candara Light", 13)).grid(row=0, column=0, columnspan=2)
        self.selected_value = tk.StringVar()
        self.selected_value.set(None)  

        self.widgets = {}
        
        # Creación de los Radiobuttons
        for i, opcion in enumerate(self.valores):
            widget = tk.Radiobutton(self, text=opcion,bg="white smoke", font=("Candara Light", 13), variable=self.selected_value, value=opcion)
            widget.grid(row=i+1, column=0, sticky="w")
            widget.config(state="disabled" if not self.habilitado[i] else "normal")
            self.widgets[opcion] = widget

    def crearMultipleOpcionFrame(self, titulo):
        """
        Crea un frame con opciones de selección múltiple usando Checkbuttons.
        
        :param titulo (str): Texto para el título del grupo de opciones.
        """
        tk.Label(self, text=titulo,bg="white smoke",font=("Candara Light", 13)).grid(row=0, column=0, columnspan=2)
        self.widgets = {}
        
        # Creación de los Checkbuttons
        for i, opcion in enumerate(self.valores):
            var = tk.StringVar(value=None)
            widget = tk.Checkbutton(self, text=opcion, bg="white smoke",font=("Candara Light", 13), variable=var, onvalue=opcion, offvalue="")
            widget.var = var
            widget.grid(row=i+1, column=0, sticky="w")
            widget.config(state="disabled" if not self.habilitado[i] else "normal")
            self.widgets[opcion] = widget

    def crearFieldFrame(self, titulo_criterios, titulo_valores):
        """
        Crea un frame con campos de entrada de texto usando Entry.
        
        :param titulo_criterios (str): Texto para el título de los criterios.
        :param titulo_valores (str): Texto para el título de los valores.
        """
        tk.Label(self, text=titulo_criterios, bg="white smoke", font=("Candara Light", 13)).grid(row=0, column=0,pady=10,padx=10)
        tk.Label(self, text=titulo_valores, bg="white smoke", font=("Candara Light", 13)).grid(row=0, column=1,pady=10,padx=10)
        
        self.entries = {}
        
        # Creación de los campos Entry
        for i, criterio in enumerate(self.criterios):
            tk.Label(self, text=criterio, bg="white smoke", font=("Candara Light", 13)).grid(row=i+1, column=0, sticky="w")
            entry = tk.Entry(self, font=("Candara Light", 13))
            entry.grid(row=i+1, column=1, sticky="ew")
            entry.insert(0, self.valores[i] if self.valores and self.valores[i] is not None else "")
            entry.config(state="disabled" if not self.habilitado[i] else "normal")
            self.entries[criterio] = entry

    def crearBotones(self, total_filas):
        """
        Crea los botones de Aceptar y Borrar en el frame con un tamaño fijo.
        
        :param total_filas (int): Cantidad de filas que ocupan las opciones o criterios.
        """
        # Crear el botón de "Aceptar" con un tamaño fijo
        aceptar_btn = tk.Button(self, text="Aceptar", bg="white smoke",font=("Candara Light", 13), command=self.aceptar, width=10)
        aceptar_btn.grid(row=total_filas + 1, column=0, pady=10,sticky="e") 
        
        # Crear el botón de "Borrar" con un tamaño fijo
        borrar_btn = tk.Button(self, text="Borrar", bg="white smoke",font=("Candara Light", 13), command=self.borrar, width=10)
        borrar_btn.grid(row=total_filas + 1, column=1, pady=10,sticky="w") 
    
    def aceptar(self):
        """
        Función que maneja la acción del botón Aceptar, mostrando un mensaje
        con las opciones seleccionadas o los valores ingresados.
        """
        seleccion = None
        
        try:
            if self.tipo_formulario in [0,1,2]:  # Selección única o múltiple
                seleccion = self.getValuesOpciones()
                if seleccion is None or not seleccion:  # No se seleccionó ninguna opción
                    raise OpcionNoSeleccionadaError()
                if self.tipo_formulario == 2 and len(seleccion) > 2:
                    raise MaximoDosOpcionesError(seleccion)


            elif self.tipo_formulario == 3:  # Entradas de texto
                seleccion = {criterio: self.getValueEntrada(criterio) for criterio in self.entries.keys()}
                campos_incompletos = [criterio for criterio in self.criterios if seleccion[criterio] == ""]
                if campos_incompletos:
                    raise CamposIncompletosError(campos_incompletos)

                # Validación de parametros
                if self.verificaciones is not None:
                    self.excepciones=self.lanzarExcepcionesEntradaTexto(seleccion) 
                    if self.excepciones==False:
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
        elif self.tipo_formulario in[1,2]:
            for widget in self.widgets.values():
                widget.var.set(None)
        elif self.tipo_formulario == 3:
            for entry in self.entries.values():
                entry.delete(0, tk.END)

    def getValuesOpciones(self):
        """
        Obtiene los valores seleccionados en los Radiobuttons o Checkbuttons.
        
        :return str: Para tipo_opcion 0: El valor seleccionado.
        :return list[str]: Para tipo_opcion 1 y 2: Una lista de valores seleccionados.
        :return None: Para otros tipos o sin seleccion
        """
        if self.tipo_formulario == 0:
            return "" if self.selected_value.get()=="None" or not self.selected_value.get() else self.selected_value.get()
        elif self.tipo_formulario in[1,2]:
            seleccion = [opcion for opcion, widget in self.widgets.items() if widget.var.get()]
            return seleccion if len(seleccion) > 0 else []
        return None
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
       
    
    def añadirCriterioValor(self,criterio,valor):
        """
        Añade un criterio y su respectivo valor al fieldFrame de resultados
        
        :param  criterio: nombre del criterio
        :param  valor: valor del criterio
        """
        _,numFilas=self.grid_size()
        tk.Label(self, text=criterio, bg="white smoke", font=("Candara Light", 13)).grid(row=numFilas+1, column=0, sticky="w")
        entry = tk.Entry(self, font=("Candara Light", 13))
        entry.grid(row=numFilas+1, column=1, sticky="ew")
        entry.insert(0, valor)
        entry.config(state="disabled")
        
    def lanzarExcepcionesEntradaTexto(self,seleccion):
        """
        Verifica si se cumplen con todas los parametros requeridos y si no es asi se lanza una excepcion
        
        :param seleccion: valor ingresado en el entry, de la forma ["Criterio","Valor"]
        """
        # self.verificaciones es de la forma [("Criterio",funcion),...]
        for tupla in self.verificaciones:
            excepciones=True
            criterio=tupla[0]
            self.funcion=tupla[1]
            try:
                self.funcion(seleccion[criterio])
                excepciones=False
            except ErrorAplicacion as e:
                messagebox.showerror("Error", str(e))
            finally:
                return excepciones

def mostrar_seleccion(seleccion):
    """
    METODO SOLO PARA EJEMPLO
    """
    messagebox.showinfo("Seleccion",f"Selección: {seleccion}")


# Ejemplo de uso del FieldFrame dentro de la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    # Crear una instancia de FieldFrame para una única opción (RadioButton)
    frame1 = FieldFrame(root, tipo_formulario=0, on_accept=mostrar_seleccion, tituloValores="Elige una opción:", valores=["Opción 1", "Opción 2", "Opción 3"])
    frame1.pack(pady=10, padx=10, fill="x")
    
    # Crear una instancia de FieldFrame para múltiples opciones (Checkbutton)
    frame2 = FieldFrame(root, tipo_formulario=1, on_accept=mostrar_seleccion, tituloValores="Selecciona una o más opciones:", valores=["Opción A", "Opción B", "Opción C"])
    frame2.pack(pady=10, padx=10, fill="x")
    
    # Crear una instancia de FieldFrame para SOLO dos opciones (Checkbutton)
    frame3 = FieldFrame(root, tipo_formulario=2, on_accept=mostrar_seleccion, tituloValores="Selecciona solo dos opciones:", valores=["Opción A", "Opción B", "Opción C"])
    frame3.pack(pady=10, padx=10, fill="x")
    
    # Crear una instancia de FieldFrame para criterios y valores (Entry)
    frame4 = FieldFrame(root, tipo_formulario=3, on_accept=mostrar_seleccion, tituloCriterios="Criterios:", tituloValores="Valores:", criterios=["Criterio 1", "Criterio 2"],valores=["Valor 1","Valor 2"],verificaciones=[("Criterio 1",lambda seleccion:verificarFormato(seleccion,"Criterio 1",0))])
    frame4.pack(pady=10, padx=10, fill="x")


    #Ejemplo
"""  
    # Crear una instancia de FieldFrame para criterios y valores para resultados
    frame5 = FieldFrame(root, tipo_formulario=3, on_accept=mostrar_seleccion,frame_resultado=True, tituloCriterios="Criterios:", tituloValores="Valores:", criterios=["Criterio 1", "Criterio 2"],valores=["Valor 1","Valor 2"],)
    frame5.pack(pady=10, padx=10, fill="x")
    frame5.añadirCriterioValor("Hola","Adios")
    root.mainloop()
"""