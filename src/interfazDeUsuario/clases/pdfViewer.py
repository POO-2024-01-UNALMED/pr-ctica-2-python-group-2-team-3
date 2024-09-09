import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

class PdfViewer(tk.Toplevel):
    """
    PdfViewer es una clase que extiende tk.Toplevel y se utiliza para visualizar un archivo PDF
    en una ventana separada. Cada página del PDF se convierte en una imagen y se muestra
    dentro de un canvas con soporte para scroll.
   """
    def __init__(self, parent, pdf_path, titulo):
        """
        :param parent (tk.root): La ventana padre que crea esta ventana emergente.
        :param pdf_path (str): Ruta del archivo PDF que se va a visualizar.
        :param titulo (str): Título de la ventana emergente.
        """
        super().__init__(parent)
        self.title = titulo
        self.geometry("615x700")
        self.pdf_path = pdf_path

        # Crear un canvas con scroll
        canvas = tk.Canvas(self)
        scrollbar_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar_y.set)

        # Empacar scrollbar y canvas
        scrollbar_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Crear un frame dentro del canvas para contener las imágenes del PDF
        canvas_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        # Cargar y mostrar las páginas del PDF
        self.load_pdf(canvas_frame)

        # Actualizar el tamaño del canvas para que se ajuste al contenido
        canvas_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def load_pdf(self, canvas_frame):
        """
        Carga las páginas del archivo PDF y las convierte en imágenes que se mostrarán
        en el frame dentro del canvas.

        :param canvas_frame (tk.Frame): Frame donde se insertan las imágenes del PDF.
        """
        try:
            # Abrir el documento PDF
            pdf_document = fitz.open(self.pdf_path)
            
            # Convertir cada página en una imagen y mostrarla en un Label
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)  # Cargar la página
                pix = page.get_pixmap()  # Convertir la página a un Pixmap
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Crear una imagen de PIL
                tk_img = ImageTk.PhotoImage(img)  # Convertir la imagen de PIL a un formato compatible con Tkinter

                # Crear un Label para mostrar la imagen de la página PDF
                img_label = tk.Label(canvas_frame, image=tk_img)
                img_label.image = tk_img  # Mantener una referencia de la imagen para evitar que sea recolectada por el garbage collector
                img_label.pack()

        except Exception as e:
            # Mostrar un mensaje de error si no se puede cargar el PDF
            messagebox.showerror("Error al cargar el PDF", f"No se pudo cargar el PDF:\n{e}")

# Ejemplo de uso del FieldFrame dentro de la ventana principal
def main():
    root = tk.Tk()
    root.withdraw()
    base_path = os.path.dirname(__file__)
    pdf_path = os.path.join(base_path, "../archivos/manualDeUsuario.pdf")
    viewer = PdfViewer(root, pdf_path, titulo="Visor de PDF")
    root.mainloop()

if __name__ == "__main__":
    main()