import tkinter as tk

# Lista de tonos de cafés y beiges que combinan con White Smoke
colors = {
    "Beige": "#F5F5DC",
    "Ivory": "#FFFFF0",
    "Linen": "#FAF0E6",
    "Antique White": "#FAEBD7",
    "Blanched Almond": "#FFEBCD",
    "Wheat": "#F5DEB3",
    "Tan": "#D2B48C",
    "Burly Wood": "#DEB887",
    "Bisque": "#FFE4C4",
    "Navajo White": "#FFDEAD",
    "Sandy Brown": "#F4A460",
    "Light Goldenrod": "#EEDD82",
    "Peru": "#CD853F",
    "Chocolate": "#D2691E",
    "Saddle Brown": "#8B4513",
}

# Crear la ventana principal
root = tk.Tk()
root.title("Tonos de Cafés y Beiges")
root.config(bg="white smoke")

# Crear un contenedor para las etiquetas
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Función para crear las etiquetas de colores
def create_color_labels(colors):
    for color_name, color_hex in colors.items():
        label = tk.Label(frame, text=color_name, bg=color_hex, width=20, height=2)
        label.pack(pady=5)

# Crear las etiquetas con los tonos de café y beige
create_color_labels(colors)

# Iniciar el bucle principal de la interfaz
root.mainloop()
