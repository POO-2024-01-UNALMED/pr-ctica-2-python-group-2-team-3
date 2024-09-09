import tkinter as tk

class Menu(tk.Frame):
    """
    Clase para crear un menú con submenús en una interfaz gráfica usando Tkinter.
    """
    def __init__(self, parent, window, opciones_menu, submenus):
        """
        :param parent (tk.Frame): Ventana o frame en el que se colocará el menú.
        :param window (tk.root): Referencia a la ventana principal para manejar eventos de submenú.
        :param opciones_menu (list[str]): Lista de opciones del menú principal.
        :param submenus (list[str]): Lista de listas, donde cada lista contiene las opciones de submenú correspondientes.
        """
        super().__init__(parent)
        self.parent = parent
        self.window = window
        self.opciones_menu = opciones_menu
        self.submenus = submenus

        self.buttons = {}  # Diccionario para almacenar los botones del menú principal
        self.selected_button = None  # Botón actualmente seleccionado

        # Frame para el menú principal
        self.frameMenu = tk.Frame(self, height=30, bg="white")
        self.frameMenu.grid(row=0, column=0, sticky="ew")
        self.frameMenu.grid_rowconfigure(0, weight=1)

        # Frame para los submenús
        self.frameSubMenu = tk.Frame(self, height=30, bg="white")
        self.frameSubMenu.grid(row=1, column=0, sticky="ew")
        self.frameSubMenu.grid_rowconfigure(0, weight=1)
        self.frameSubMenu.grid_remove()  # Ocultar inicialmente

        self.createMenu()  # Crear los botones del menú

    def createMenu(self):
        """
        Crea los botones del menú principal.
        """
        for i, opcion in enumerate(self.opciones_menu):
            boton = tk.Button(self.frameMenu, text=opcion, bg="white", relief="flat", font=("Candara", 11),
                              command=lambda opt=opcion: self.menuButtonClick(opt))
            boton.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            self.buttons[opcion] = boton  # Almacenar el botón en el diccionario
            
    def menuButtonClick(self, option):
        """
        Maneja el clic en un botón del menú principal.

        :param option (str): Opción del menú principal que fue seleccionada.
        """
        if self.selected_button:
            self.selected_button.config(bg="white", relief="flat", underline=-1)  # Restablecer la apariencia del botón anterior

        self.selected_button = self.buttons[option]
        self.selected_button.config(bg="white", relief="flat", underline=0)  # Cambiar la apariencia del botón seleccionado

        index = self.opciones_menu.index(option)
        self.mostrarSubmenu(index)  # Mostrar el submenú correspondiente

    def mostrarSubmenu(self, index):
        """
        Muestra el submenú correspondiente a la opción seleccionada.

        :param index (int): Índice del submenú a mostrar.
        """
        # Limpiar el submenu_frame antes de agregar nuevos botones
        for widget in self.frameSubMenu.winfo_children():
            widget.destroy()

       # Verificar si ya se está mostrando el submenu seleccionado y si el frame está visible
        if hasattr(self, 'current_submenu') and self.current_submenu == index:
            if self.frameSubMenu.winfo_ismapped():  # Verifica si el submenu_frame está visible
                self.frameSubMenu.grid_remove()
                self.current_submenu = None
            return

        submenu = self.submenus[index]
        for row, opcion in enumerate(submenu):
            boton_sub = tk.Button(self.frameSubMenu, text=opcion, bg="white", relief="flat", font=("Candara Light", 10),
                                 command=lambda opt=opcion: self.handleSubmenu(opt))
            boton_sub.grid(row=row, column=0, padx=5, pady=2, sticky="w")

        self.frameSubMenu.grid(row=1, column=0, sticky="nsew")  # Mostrar el frame del submenú
        self.current_submenu = index

    def handleSubmenu(self, option):
        """
        Maneja el clic en una opción del submenú.

        :param option (str): Opción del submenú que fue seleccionada.
        """
        self.frameSubMenu.grid_forget()  # Ocultar el submenú
        for widget in self.frameSubMenu.winfo_children():
            widget.destroy()  # Eliminar los widgets existentes
        self.current_submenu = None
        self.window.handleSubmenu(option)  # Delegar el manejo al objeto window

def main():
    """
    Función principal para ejecutar una prueba del menú con submenús.
    """
    def handleSubmenu(option):
        """
        Maneja la selección de una opción del submenú.

        :param option (str): Opción seleccionada del submenú.
        """
        print(f"Submenu option selected: {option}")

    root = tk.Tk()
    root.title("Menu Test")
    root.config(bg="white")

    # Opciones del menú principal y submenús asociados
    opciones_menu = ["File", "Edit", "View"]
    submenus = [["New", "Open", "Save"], ["Cut", "Copy", "Paste"], ["Zoom In", "Zoom Out", "Reset"]]

    # Crear una instancia del menú y agregarlo a la ventana principal
    menu = Menu(root, window=type('obj', (object,), {'handle_submenu': handleSubmenu}),
                opciones_menu=opciones_menu, submenus=submenus)
    menu.pack(fill="both", expand=True)

    root.mainloop()  # Ejecutar el bucle principal de la interfaz gráfica

if __name__ == "__main__":
    main()