"""
Este programa simplificado gestiona el préstamo de dos libros muestra los datos del cliente
y el estado de cada libro: si está prestado o si ha sido devuelto.
Toda la nomenclatura de variables y funciones sigue la convención snake_case.
"""

class Libro:
    """
    Representa un libro en la biblioteca con su codigo de identificacion.
    """
    def __init__(self, titulo_libro: str, autor_libro: str, id_libro: str):
        """
        Constructor de la clase Libro.

        Argumentos y tipo de datos
            titulo_libro (str): El título del libro.
            autor_libro (str): El autor del libro.
            id_libro (str): El ID único del libro (ej. CA001).
        """
        self.titulo_libro = titulo_libro
        self.autor_libro = autor_libro
        self.id_libro = id_libro
        self.esta_prestado = False # Booleano para saber si el libro está prestado o no
        self.prestado_a_cliente = None # Referencia al objeto Cliente

    def prestar_libro(self, cliente: 'Cliente'):
        """
        Marca el libro como prestado y registra a qué cliente.

        Args:
            cliente (Cliente): El objeto Cliente al que se le presta el libro.
        """
        if not self.esta_prestado:
            self.esta_prestado = True
            self.prestado_a_cliente = cliente
            print(f"'{self.titulo_libro}' (ID: {self.id_libro}) ha sido prestado a {cliente.nombre_cliente}.")
        else:
            print(f"'{self.titulo_libro}' (ID: {self.id_libro}) ya está prestado a {self.prestado_a_cliente.nombre_cliente}.")

    def devolver_libro(self):
        """
        Marca el libro como devuelto y limpia el registro del préstamo.
        """
        if self.esta_prestado:
            self.esta_prestado = False
            self.prestado_a_cliente = None
            print(f"'{self.titulo_libro}' (ID: {self.id_libro}) ha sido devuelto.")
        else:
            print(f"'{self.titulo_libro}' (ID: {self.id_libro}) no está prestado actualmente.")

    def obtener_estado_prestamo(self):
        """
        Retorna una cadena describiendo el estado actual del préstamo del libro.
        """
        if not self.esta_prestado:
            return f"'{self.titulo_libro}' (ID: {self.id_libro}): Disponible."
        else:
            return f"'{self.titulo_libro}' (ID: {self.id_libro}): Prestado a {self.prestado_a_cliente.nombre_cliente}."


class Cliente:
    """
    Representa un cliente de la biblioteca.
    """
    def __init__(self, nombre_cliente: str, edad_cliente: int, cedula_identidad: str):
        """
        Constructor de la clase Cliente.

        Argumentos y tipo de datos
            nombre_cliente (str): El nombre del cliente.
            edad_cliente (int): La edad del cliente.
            cedula_identidad (str): La cédula de identidad del cliente.
        """
        self.nombre_cliente = nombre_cliente
        self.edad_cliente = edad_cliente
        self.cedula_identidad = cedula_identidad

    def obtener_info_cliente(self):
        """
        Retorna una cadena con la información del cliente.
        """
        return f"Cliente: {self.nombre_cliente}, Edad: {self.edad_cliente} años, Cédula: {self.cedula_identidad}"

# Estructura principal del codigo

if __name__ == "__main__":
    print("Sistema de Gestión de Prestamo de libros Bibliotecarios")

    # Se crea dos objetos Libro con ID personalizado
    # Se utilizan diferentes tipos de datos: string para los atributos del libro
    libro_uno = Libro(titulo_libro="Libro 1 Cien Años de Soledad", autor_libro="Gabriel García Márquez", id_libro="CA001")
    libro_dos = Libro(titulo_libro="Libro 2 Don Quijote de la Mancha", autor_libro="Miguel de Cervantes", id_libro="CA002")

    # Se utilizan diferentes tipos de datos: string para nombre y cédula, int para edad
    cliente_carlos = Cliente(nombre_cliente="Carlos", edad_cliente=35, cedula_identidad="1710123456")
    cliente_juan = Cliente(nombre_cliente="Juan", edad_cliente=29, cedula_identidad="1003867429")

    print("\nInformación de Clientes")
    print(cliente_carlos.obtener_info_cliente())
    print(cliente_juan.obtener_info_cliente())

    print("\nEstado Inicial de los Libros")
    print(libro_uno.obtener_estado_prestamo())
    print(libro_dos.obtener_estado_prestamo())

    # Se realiza un prestamo de libro
    print("\nRealizando Préstamo de Libro 1 a Carlos")
    libro_uno.prestar_libro(cliente_carlos)
    print("\nEstado de los Libros después del Préstamo")
    print(libro_uno.obtener_estado_prestamo())
    print(libro_dos.obtener_estado_prestamo())

    # Se realizar Devolución
    print("\nRealizando Devolución de Libro 1")
    libro_uno.devolver_libro()
    print("\nEstado de los Libros después de la Devolución")
    print(libro_uno.obtener_estado_prestamo())
    print(libro_dos.obtener_estado_prestamo())

    # Se intenta devolver un libro que no está prestado
    print("\nIntentando devolver un libro no prestado")
    libro_uno.devolver_libro()