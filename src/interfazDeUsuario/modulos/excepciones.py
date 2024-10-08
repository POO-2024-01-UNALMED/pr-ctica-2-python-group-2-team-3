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
        super().__init__(f"{self.mensaje_base}\n{tipo_error}\nValor ingresado: {fecha}")

class ExistenciaEror(ErrorEntrada):
    """Error cuando no se ingresa un objeto existente"""
    def __init__(self,objeto,valor):
        """
        :param objeto: el objeto que se esta buscando
        :param valor: el valor ingresado por el usuario
        """
        self.objeto=objeto
        self.valor=valor
        self.mensaje_base = " ingresado no se encuenta registrado en la base de datos. Asegurese de ingresar un valor existente"
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

class FiltroSeleccionadoError(ErrorFormulario):
    """Error cuando no se selecciona el mismo filtro dos veces"""
    def __init__(self, filtros,mensaje=None):
        self.mensaje_base = " No puedes elegir el mismo filtro dos veces." 
        mensajeCompleto=(f"{self.mensaje_base}\nFiltros seleccionados actualmente: {filtros}")if mensaje is None else mensaje
        super().__init__(mensajeCompleto)
        
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

class HabitacionesError(ErrorParametros):
    """Error cuando se ingreso incorrectamente la cantidad de habitaciones"""
    def __init__(self,seleccion, mensaje):
        """:param seleccion:habitaciones seleccionadas
        :param mensaje:mensaje de especificacion del error"""
        self.seleccion=seleccion
        self.mensaje_base = "Se ingreso un número incorrecto de habitaciones."
        super().__init__(f"{self.mensaje_base} {mensaje}\nHabiitaciones seleccionadas: {seleccion}")
        
        
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

def verificarNumero(numero,aplicaCer0=False):
    """
    Verifica que el número ingresado sea un entero mayor a 0.
    
    :param  numero: el número a verificar
    :param aplicaCer0: booleano True si aplica el cero
    """
    try:
        numero = int(numero)
    except ValueError:
        raise NumeroInvalidoError(numero)
    if aplicaCer0==False and numero <= 0:
        raise NumeroInvalidoError(numero)
    elif aplicaCer0==True and numero < 0:
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
        if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', fecha):
            dia, mes, año = map(int, fecha.split('/'))
            if not (1 <= mes <= 12):
                raise FechaInvalidaError("Mes inválido, asegurese de ingresar un numero entre 1-12.", fecha)
            
            # Días por mes (considerando febrero con 28 días)
            dias_en_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if not (1 <= dia <= dias_en_mes[mes - 1]):
                raise FechaInvalidaError(f"Día inválido para el mes, le recordamos que {meses[mes - 1]} tiene {dias_en_mes[mes - 1]} dias.", fecha)
            
            if año != 2024:
                raise FechaInvalidaError("Año inválido, asegurese de ingresar el año actual.", fecha)
        else:
            raise FormatoInvalidoError(formatos[formato], criterio, fecha)
        
    # Verifica el formato MM/AAAA
    elif formato == 2:
        if re.match(r'^\d{1,2}/\d{4}$', fecha):
            mes, año = map(int, fecha.split('/'))
            if not (1 <= mes <= 12):
                raise FechaInvalidaError("Mes inválido, asegurese de ingresar un numero entre 1-12.", fecha)
            if año != 2024:
                raise FechaInvalidaError("Año inválido,asegurese de ingresar el año actual.", fecha)
        else:
            raise FormatoInvalidoError(formatos[formato], criterio, fecha)

def verificarFormato(valor,criterio,formato,palabras=None):
        """
        Verifica si las entradas cumplen con el formato especificado.
        
        :param criterio: el criterio donde se require cumplir con el formato
        :param formato: el formato a verificar
        """
        if formato == 0:
                # Verifica que sea una palabra (sin espacios)
                if not re.fullmatch(r"^\w+$", valor):
                    raise FormatoInvalidoError(formatos[formato], criterio, valor)
                if palabras:
                    coincidencia=False
                    for palabra in palabras:
                        if palabra.lower()==valor.lower(): coincidencia=True
                    if not coincidencia:
                         raise FormatoInvalidoError(palabras, criterio, valor)
            
        elif formato in [1,2]:
            # Utiliza el método verificarFecha para validar las fechas
                verificarFecha(formato, criterio, valor)

def verificarGuia(datos_personales):
    """
        Verifica si se ingreso un objeto guia existente.
        :param datos_personales(list[(str,str)]): de la forma {("Nombre",nombreIngresado),("Edad",edadIngresada),("Destino",destinoIngresado)}
    """
    from gestorAplicacion.guia import Guia
    if Guia.verificarGuia(datos_personales["Nombre"],datos_personales["Edad"],datos_personales["Destino"])==False:
            raise  ExistenciaEror("El guia",datos_personales)

def verificarActividad(datos_actividad):
    """
        Verifica si se ingreso un objeto actividad existente.
        :param datos_actividad(list[(str,str)]): de la forma {("Nombre",nombreIngresado),("Destino",destinoIngresado)}
    """
    from gestorAplicacion.actividad import Actividad
    if Actividad.verificarActividad(datos_actividad["Nombre"],datos_actividad["Destino"])==False:
            raise  ExistenciaEror("La actividad",datos_actividad)
        
def verificarDestino(nombre):
    """
        Verifica si se ingreso un objeto destino existente.
        :param destino(str): el nombre del destino
    """
    from gestorAplicacion.destino import Destino
    if not any(n.lower() == nombre.lower() for n in Destino.listaNombres()):
        raise ExistenciaEror("El destino", nombre)


def verificarCodigoNone(codigo):
    """
        Verifica si se ingreso un objeto codigo existente.
        :param codigo: el numero del codigo
    """
    if codigo=="None":
            raise  ExistenciaEror("El codigo",codigo)

def verificarTitular(edad):
    try:
        verificarNumero(edad)
    except ErrorAplicacion as e:
        raise NumeroInvalidoError(edad)
    if int(edad)<18:
        raise EdadTitularError(edad)

def verificarHabitaciones(seleccion,clientes,habitacionesHotel):
    adultos=0
    for cliente in clientes:
        if cliente.getEdad()>=18:
            adultos+=1
    totalHabitaciones=int(seleccion["Individual (capacidad 1)"])+int(seleccion["Doble (capacidad 2)"])+int(seleccion["Familiar (capacidad 4)"])+int(seleccion["Suite (capacidad 6)"])
    if totalHabitaciones>adultos:
        raise HabitacionesError(seleccion=seleccion,mensaje="Hay mas habitaciones que adultos en la reserva, recuerde que debe haber minimo un adulto por habitación")
    totalClientes=int(seleccion["Individual (capacidad 1)"])+int(seleccion["Doble (capacidad 2)"])*2+int(seleccion["Familiar (capacidad 4)"])*4+int(seleccion["Suite (capacidad 6)"])*6
    if totalClientes<len(clientes):
        raise HabitacionesError(seleccion=seleccion,mensaje="No hay suficientes habitaciones para toda la reserva, verifique bien las capacidades de las habitaciones.")
    if habitacionesHotel["Individuales"]<int(seleccion["Individual (capacidad 1)"]) or habitacionesHotel["Dobles"]<int(seleccion["Doble (capacidad 2)"]) or  habitacionesHotel["Familiares"]<int(seleccion["Familiar (capacidad 4)"]) or  habitacionesHotel["Suite"]<int(seleccion["Suite (capacidad 6)"]):
        raise HabitacionesError(seleccion=seleccion,mensaje="No hay suficientes habitaciones en el hotel del tipo escogido")
                  
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
    try:
        verificarFecha(1,"fecha","5/2/2024")  
    except (FechaInvalidaError,FormatoInvalidoError) as e:
       messagebox.showerror("Error", str(e))

    try:
        verificarFecha(2,"Fecha","2/2024")  
    except (FechaInvalidaError,FormatoInvalidoError) as e:
        messagebox.showerror("Error", str(e))   
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

    
