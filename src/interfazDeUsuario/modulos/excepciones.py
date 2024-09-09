import tkinter as tk
import re
from tkinter import messagebox

"""EXCEPCIONES PERSONALIZADAS"""
# Clase base para todos los errores de la aplicación
class ErrorAplicacion(Exception):
    """Excepción base para todos los errores de la aplicación."""
    def __init__(self, mensaje=""):
        self.mensaje_base = "               Manejo de errores de la Aplicación               "
        mensaje_completo = f"{self.mensaje_base}\n{mensaje}"
        super().__init__(mensaje_completo)

# Rama entrada de texto
class ErrorEntrada(ErrorAplicacion):
    """Errores relacionados con la entrada de datos"""
    def __init__(self, mensaje="No especificado"):
        self.mensaje_base = "Error en la entrada de datos"
        mensaje_completo = f"{self.mensaje_base}: {mensaje}"
        super().__init__(mensaje_completo)

class NombreInvalidoError(ErrorEntrada):
    """Error cuando no se ingresa un nombre valido"""
    def __init__(self,nombre):
        """:param  nombre : El nombre ingresado por el usuario"""

        self.nombre=nombre
        self.mensaje_base = "El nombre ingresado no es válido, asegurese de ingresar solo letras."
        super().__init__(f"{self.mensaje_base}\nValor ingresado: {nombre}")

class NumeroInvalidoError(ErrorEntrada):
    """Error cuando no se ingresa un número valido"""
    def __init__(self,numero):
        """:param  numero: El número ingresado por el usuario"""

        self.numero=numero
        self.mensaje_base = "El número ingresado no es válido, asegurese de ingresar un entero mayor a 0."
        super().__init__(f"{self.mensaje_base}\nValor ingresado: {numero}")

class FechaInvalidaError(ErrorEntrada):
    """Error cuando no se ingresa una fecha valida"""
    def __init__(self,tipo_error,fecha):
        """
        :param tipo_error: el componente de la fecha invalido y su sugerencia de mejora
        :parm fecha: la fecha ingresada por el usuario
        """
        self.tipo_error=tipo_error
        self.fecha=fecha
        self.mensaje_base = "La fecha ingresada no es válida."
        super().__init__(f"{self.mensaje_base}\n{tipo_error}. Valor ingresado: {fecha}")

class ExistenciaErorr(ErrorEntrada):
    """Error cuando no se ingresa un objeto existente"""
    def __init__(self,objeto,valor):
        """
        :param objeto: el objeto que se esta buscando
        :param valor: el valor ingresado por el usuario
        """
        self.objeto=objeto
        self.valor=valor
        self.mensaje_base = " ingresado no se encuenta registrado en la base de datos. Asegurese de ingresas un valor exixtente"
        super().__init__(f"{objeto}{self.mensaje_base}.\nValor ingresado: {valor}")

# Rama formulario
class ErrorFormulario(ErrorAplicacion):
    """Errores relacionados con la gestión del formulario"""
    def __init__(self, mensaje="No especificado"):
        self.mensaje_base = "Error en el manejo del formulario"
        super().__init__(f"{self.mensaje_base}: {mensaje}")

class OpcionNoSeleccionadaError(ErrorFormulario):
    """Error cuando no se selecciona ninguna opción válida"""
    def __init__(self):
        self.mensaje_base = "No se ha seleccionado ninguna opción válida."
        super().__init__(self.mensaje_base)

class MaximoDosOpcionesError(ErrorFormulario):
    """Error cuando se seleccionan más de las dos opciones permitidas"""
    def __init__(self, opciones_seleccionadas):
        """:param  opciones_seleccionadas: las opciones seleccionadas por el usuario"""

        self.mensaje_base = "Se han seleccionado más de dos opciones, pero solo se permiten dos."
        self.opciones_seleccionadas = opciones_seleccionadas
        super().__init__(f"{self.mensaje_base}\nSeleccionadas: {opciones_seleccionadas}.")

class CamposIncompletosError(ErrorFormulario):
    """Error cuando hay campos incompletos en el formulario"""
    def __init__(self, campos_faltantes):
        """:param  campos_faltantes: los campos que no fueron ingresados"""

        self.mensaje_base = "No se han completado todos los campos del formulario."
        self.campos_faltantes = campos_faltantes
        campos = ', '.join(campos_faltantes)
        super().__init__(f"{self.mensaje_base}\nCampos faltantes: {campos}.")

class FormatoInvalidoError(ErrorFormulario):
    """Error cuando un campo tiene un formato inválido"""
    def __init__(self,formato,campo, valor):
        """
        :param formato: el formato que se esta pidiendo
        :param campo: el campo que tiene el formato invalido
        :param valor: el valor ingresado por el usuario
        """
        self.mensaje_base = "El formato del campo es inválido, asegurese de ingresar el valor de la forma:"
        self.formato=formato
        self.campo = campo
        self.valor = valor
        super().__init__(f"{self.mensaje_base} '{formato}'\nCampo: '{campo}', Valor: '{valor}'.")
        
#Rama validacion de parametros
class ErrorParametros(ErrorAplicacion):
    """Errores relacionados con el cumplimiento de parametros"""
    def __init__(self, mensaje="No especificado"):
        self.mensaje_base="Error incumplimiento de parametros"
        super().__init__(f"{self.mensaje_base}: {mensaje}")

class CancelacionError(ErrorParametros):
    """Error cuando se modifica una reserva y no cumple con los parametros anteriores"""
    def __init__(self,tipo):
        """:param tipo: el tipo de cancelacion (plan de actividades, hotel, ambas)"""
        self.tipo=tipo
        self.mensaje_base = ["Las modificaciones no cumplen con los parametros","Por lo tanto se ha cancelado lo planeado anteriormente."]
        super().__init__(f"{self.mensaje_base[0]} {tipo}.\n{self.mensaje_base[1]} ")

class MayorDeEdadError(ErrorParametros):
    """Error cuando no hay mayores de edad registrados"""
    def __init__(self):
        self.mensaje_base = "No se ingreso ningún adulto (mayor de 18 años), por favor vuelva a ingresar las personas asegurandose que hay un mayor de edad."
        super().__init__(self.mensaje_base)
        
class EdadTitularError(ErrorParametros):
    """Error cuando el titular ingresada no es mayor de edad"""
    def __init__(self,edad):
        """:param edad: la edad ingresada por el usuario"""
        self.edad=edad
        self.mensaje_base = f"El titular no cumple con la edad requerida, debe ser mayor de edad"
        super().__init__(f"{self.mensaje_base}.\nEdad ingresada: {edad} años")
        
        
"""METODOS PARA REALIZAR VERIFICACIONES"""
def verificarNombre(nombre):
    """
    Verifica que el nombre contenga solo letras y permita múltiples palabras.
    
    :param  nombre: el nombre a verificar
    """
    palabras = nombre.split()
    for palabra in palabras:
        if not palabra.isalpha():
            raise NombreInvalidoError(nombre)

def verificarNumero(numero):
    """
    Verifica que el número ingresado sea un entero mayor a 0.
    
    :param  numero: el número a verificar
    """
    try:
        numero = int(numero)
    except ValueError:
        raise NumeroInvalidoError(numero)
    if numero <= 0:
        raise NumeroInvalidoError(numero)

formatos=["Máximo una palabra","Fecha DD/MM/AAAA","Fecha MM/AAAA"]

def verificarFecha(formato,criterio,fecha):
    """
    Verifica que la fecha ingresada sea válida en los formatos DD/MM/AAAA o MM/AAAA.
    
    :param   formato: el formato de la fecha ingresada
    :param   criterio: el criterio donde se pide ingresar la fecha
    :param   fecha: la fecha a verificar
    """
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    # Verifica el formato DD/MM/AAAA
    if formato == 1:
        if re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
            dia, mes, año = map(int, fecha.split('/'))
            if not (1 <= mes <= 12):
                raise FechaInvalidaError("Mes inválido, asegurese de ingresar un numero entre 1-12.", fecha)
            
            # Días por mes (considerando febrero con 28 días)
            dias_en_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if año < 2024:
                raise FechaInvalidaError("Año inválido, asegurese de ingresar un año que no haya pasado.", fecha)
            if not (1 <= dia <= dias_en_mes[mes - 1]):
                raise FechaInvalidaError(f"Día inválido para el mes, le recordamos que {meses[mes - 1]} tiene {dias_en_mes[mes - 1]} dias.", fecha)
        
    # Verifica el formato MM/AAAA
    elif formato == 2:
        if re.match(r'^\d{2}/\d{4}$', fecha):
            mes, año = map(int, fecha.split('/'))
            if not (1 <= mes <= 12):
                raise FechaInvalidaError("Mes inválido, asegurese de ingresar un numero entre 1-12.", fecha)
            if año < 2024:
                raise FechaInvalidaError("Año inválido,asegurese de ingresar un año que no haya pasado", fecha)
    
    else:
        raise FormatoInvalidoError(formatos[formato], criterio, fecha)

def verificarFormato(valor,criterio,formato):
        """
        Verifica si las entradas cumplen con el formato especificado.
        
        :param criterio: el criterio donde se require cumplir con el formato
        :param formato: el formato a verificar
        """
        if formato == 0:
                # Verifica que sea una palabra (sin espacios)
                if not re.fullmatch(r"^\w+$", valor):
                    raise FormatoInvalidoError(formatos[formato], criterio, valor)
            
        elif formato in [1,2]:
            # Utiliza el método verificarFecha para validar las fechas
                verificarFecha(formato, criterio, valor)
                
"""EJEMPLO DE USO"""
# Ejemplo de cómo lanzar y manejar las excepciones
def probar_excepcion(excepcion):
    try:
        raise excepcion
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Configuración de la interfaz para lanzar las excepciones
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    """
    excepciones = [
        NombreInvalidoError("Juan123"),
        NumeroInvalidoError(-5),
        FechaInvalidaError("Año invalido", "30/02/2023"),
        ExistenciaErorr("El codigo", "XYZ123"),
        CancelacionError("Del hotel"),
        MayorDeEdadError(),
        EdadTitularError(17),
        OpcionNoSeleccionadaError(),
        MaximoDosOpcionesError(["Opción 1", "Opción 2", "Opción 3"]),
        CamposIncompletosError(["Nombre", "Apellido", "Correo"]),
        FormatoInvalidoError("DD/MM/AAAA", "Fecha de nacimiento", "30-02-2023")
    ]

    # Probar cada excepción
    for excepcion in excepciones:
        probar_excepcion(excepcion)
    """
#Ejemplo de uso de los metodos
"""
    try:
        verificarNumero("-5")  # Esto debería lanzar una excepción
    except NumeroInvalidoError as e:
        messagebox.showerror("Error", str(e))

    try:
        verificarNombre("Juan Pérez")  # Esto debería ser válido
        verificarNombre("Ana123 Lopez")  # Esto debería lanzar una excepción
    except NombreInvalidoError as e:
        messagebox.showerror("Error", str(e))
"""
""""
    try:
        verificarFecha("Fecha DD/MM/AAAA","fecha","31/02/2024")  # Esto debería lanzar una excepción por día inválido
    except FechaInvalidaError as e:
       messagebox.showerror("Error", str(e))

    try:
        verificarFecha("02/2024")  # Esto debería ser válido
    except FechaInvalidaError as e:
        messagebox.showerror("Error", str(e))
"""