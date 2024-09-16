import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from modulos.excepciones import *  # Asegúrate de tener estas excepciones definidas

class Tabla(tk.Frame):
    def __init__(self, parent, encabezado, titulo_columnas, on_filtro, filtros, eleccion=None, on_eleccion=None):
        super().__init__(parent)
        self.encabezado = encabezado
        self.titulo_columnas = titulo_columnas
        self.on_filtro = on_filtro
        self.filtros = filtros
        self.eleccion = eleccion
        self.on_eleccion = on_eleccion
        self.config(bg="white smoke")
        self.color = False  # Controla el color de las filas alternas
        self.filtros_seleccionados = []  # Lista para almacenar filtros seleccionados
        
        self.crearFrames()
        self.crearMenuFiltros()
        self.crearEncabezado(self.encabezado)
        self.crearColumnas(self.titulo_columnas)
        self.crearBotones()  # Mueve los botones debajo de la tabla
        
    def crearFrames(self):
        
        self.frame = tk.Frame(self, bg="lightgray")
        self.frame.grid(row=1, column=0, sticky="nsew", padx=10)
        self.frame.grid_columnconfigure(0, weight=1)

        self.filtro_frame = tk.Frame(self, bg="white smoke")
        self.filtro_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.filtro_frame.grid_columnconfigure(0, weight=1)
        self.filtro_frame.grid_columnconfigure(1, weight=0)

        self.frameTabla = tk.Frame(self.frame,bg="lightgray")
        self.frameTabla.grid(row=1, column=0, sticky="nsew", pady=2, padx=2)
        self.frameTabla.grid_columnconfigure(0, weight=1)

        separador=tk.Frame(self.frameTabla,bg="lightgray")
        separador.grid(row=0, column=0, sticky="ew",pady=5)
        
        self.frameEncabezado = tk.Frame(self.frameTabla)
        self.frameEncabezado.grid(row=1, column=0, sticky="ew")
        self.frameEncabezado.grid_columnconfigure(0, weight=1)

        self.frameCuerpo = tk.Frame(self.frameTabla, bg="lightgray")
        self.frameCuerpo.grid(row=2, column=0, sticky="nsew", padx=1)
        self.frameCuerpo.grid_columnconfigure(0, weight=1)
        
        # Frame para los botones debajo de la tabla
        self.botones_frame = tk.Frame(self, bg="white smoke")
        self.botones_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.botones_frame.grid_columnconfigure(0, weight=1)
        self.botones_frame.grid_columnconfigure(1, weight=0)
        
    def crearMenuFiltros(self):
        style = ttk.Style()
        style.configure("TCombobox", font=("Candara Light", 18))
        tamano_mayor = max(len(valor) for valor in self.filtros)
        
        self.filtro_var = tk.StringVar(value="Filtros")
        self.filtro_combobox = ttk.Combobox(self.filtro_frame, state="readonly", textvariable=self.filtro_var, width=tamano_mayor, style="TCombobox", values=self.filtros)
        self.filtro_combobox.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.filtro_combobox.bind("<<ComboboxSelected>>", self._on_filtro)
    
    def crearBotones(self):
        """
        Crea los botones de 'Borrar filtros' y 'Elección' debajo de la tabla.
        """
        self.boton_borrar = tk.Button(self.botones_frame, text="Borrar filtros", bg="white", fg="black", font=("Candara light", 12), command=self.borrarFiltros)
        self.boton_borrar.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        if self.eleccion is not None:
            self.boton_escoger = tk.Button(self.botones_frame, text=self.eleccion, bg="lightgray", font=("Candara light", 12), command=self._on_eleccion)
            self.boton_escoger.grid(row=0, column=1, padx=5, pady=5, sticky="e")
    
    def borrarFiltros(self,mensaje=True):
        """
        Limpia la lista de filtros seleccionados y reinicia el combobox.
        """
        self.filtros_seleccionados.clear()
        self.filtro_combobox.set("Filtros")
        if mensaje:
            messagebox.showinfo("Filtros", "Filtros eliminados con éxito.")
        
    def _on_filtro(self, event=None):
        filtro_seleccionado = self.filtro_combobox.get()
        try:
            if filtro_seleccionado in self.filtros_seleccionados:
                raise FiltroSeleccionadoError(self.filtros_seleccionados)
        except ErrorFormulario as e:
            messagebox.showerror("Error", str(e))
        self.filtros_seleccionados.append(filtro_seleccionado)
        self.on_filtro(self.filtros_seleccionados)  # Pasa la lista de filtros seleccionados

    def _on_eleccion(self):
        if self.on_eleccion:
            self.on_eleccion()
        
    def crearEncabezado(self, lista_encabezado):
        for i, fila in enumerate(lista_encabezado):
            frame = tk.Frame(self.frameEncabezado, bg="lightgray")
            frame.grid(row=i, column=0, sticky='ew')
            
            for j, texto in enumerate(fila):
                label = tk.Label(frame, text=texto, bg="white", font=("Candara", 11))
                label.grid(row=0, column=j, sticky='ew', padx=1, pady=1)
            
            for j in range(len(fila)):
                frame.grid_columnconfigure(j, weight=1)
            self.frameEncabezado.grid_rowconfigure(i, weight=1)
            
    def crearColumnas(self, titulos):
        self.columnas = {}
        self.filas = 2
        
        frameFila = tk.Frame(self.frameCuerpo, bg="lightgray")
        frameFila.grid(row=0, column=0, sticky='ew')
        self.frameCuerpo.grid_rowconfigure(0, weight=1)
        
        separador = tk.Frame(self.frameCuerpo, bg="lightgray")
        separador.grid(row=1, column=0, sticky='ew', pady=1)
        self.frameCuerpo.grid_rowconfigure(1, weight=1)
        
        for t, titulo in enumerate(titulos):
            pad = (0, 1) if t == 0 else (1, 0) if t == len(titulos) - 1 else 1
            label = tk.Label(self.frameCuerpo, text=titulo, bg="white", font=("Candara", 11))
            label.grid(row=0, column=t, sticky='ew', pady=1, padx=pad)
            self.columnas[t] = len(titulo)
        self.configurarColumnas()
        
    def configurarColumnas(self):
        num_columnas = len(self.columnas)
        for col in range(num_columnas):
            self.frameCuerpo.grid_columnconfigure(col, weight=1, minsize=self.columnas[col] * 10)
            
    def añadirFila(self, valores):
        numero_fila = self.filas
        self.filas += 1
        
        frameFila = tk.Frame(self.frameCuerpo, bg="black")
        frameFila.grid(row=numero_fila, column=0, sticky='ew')
        self.frameCuerpo.grid_rowconfigure(numero_fila, weight=1)
        
        for j, texto in enumerate(valores):
            color = "white" if self.color else "white smoke"
            self.color = not self.color
            label = tk.Label(self.frameCuerpo, text=texto, bg=color, font=("Candara Light", 13))
            label.grid(row=numero_fila, column=j, sticky='ew')
            
            texto_largo = len(texto)
            if texto_largo > self.columnas[j]:
                self.columnas[j] = texto_largo

        self.configurarColumnas()
        
    def borrarFilas(self):
        """
        Borra todas las filas del frame del cuerpo, excepto las filas 1 y 2.
        """
        # Obtén todas las filas dentro del frameCuerpo
        for widget in self.frameCuerpo.grid_slaves():
            # grid_slaves devuelve los widgets en orden inverso, así que aseguramos que solo borremos filas mayores a 2
            fila = widget.grid_info()["row"]
            if fila > 2:
                widget.destroy()

        # Resetea el contador de filas al valor correcto después de eliminar las filas
        self.filas = 2
        
        
def filtro_seleccionado(filtro):
    print(f"Filtro seleccionado: {filtro}")

def eleccion_realizada():
    print("Elección realizada.")

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tabla")
    root.config(bg="white")

    # Encabezado de la tabla como lista de tuplas
    encabezado = [
        ["Tabla destinos"],
        ["Cantidad: 560", "Guias: 20"],
    ]
    tituloColumnas = ["Nombre", "Disponibilidad", "Precio", "Temporada"]
    filtros = ["disponibles", "ocupados", "todos"]
    
    # Crear instancia de la tabla y agregarla a la ventana principal
    tabla = Tabla(root, encabezado=encabezado, titulo_columnas=tituloColumnas, filtros=filtros,
                  on_filtro=lambda filtro: filtro_seleccionado(filtro),
                  eleccion="Elegir destino", on_eleccion=eleccion_realizada)

    tabla.pack(fill="both", expand=True)

    # Añadir algunas filas de ejemplo
    tabla.añadirFila(["Laura", "Disponible", "$100", "Verano"])
    tabla.añadirFila(["Carlos", "No Disponible", "$150", "Invierno"])
    tabla.añadirFila(["Ana", "Disponible", "$120", "Primavera"])

    root.mainloop()