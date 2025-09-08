import uuid
import json
import os
from datetime import datetime


class Libro:
    """Representa un libro con atributos inmutables usando tuplas"""

    def __init__(self, titulo, autor, categoria, isbn):
        # Usar tupla para título y autor (inmutables)
        self._info_basica = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn
        self.prestado = False
        self.usuario_prestado = None

    @property
    def titulo(self):
        return self._info_basica[0]

    @property
    def autor(self):
        return self._info_basica[1]

    def to_dict(self):
        """Convierte el libro a diccionario para guardar en archivo"""
        return {
            'titulo': self.titulo,
            'autor': self.autor,
            'categoria': self.categoria,
            'isbn': self.isbn,
            'prestado': self.prestado,
            'usuario_prestado': self.usuario_prestado
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un libro desde un diccionario"""
        libro = cls(data['titulo'], data['autor'], data['categoria'], data['isbn'])
        libro.prestado = data.get('prestado', False)
        libro.usuario_prestado = data.get('usuario_prestado', None)
        return libro

    def __str__(self):
        estado = "Prestado" if self.prestado else "Disponible"
        return f"'{self.titulo}' por {self.autor} - Categoría: {self.categoria} - ISBN: {self.isbn} - Estado: {estado}"


class Usuario:
    """Representa un usuario de la biblioteca"""

    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        # Lista para gestionar libros prestados (almacenaremos ISBNs)
        self.libros_prestados_isbn = []
        self.fecha_registro = datetime.now().isoformat()

    def to_dict(self):
        """Convierte el usuario a diccionario para guardar en archivo"""
        return {
            'nombre': self.nombre,
            'id_usuario': self.id_usuario,
            'libros_prestados_isbn': self.libros_prestados_isbn,
            'fecha_registro': self.fecha_registro
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un usuario desde un diccionario"""
        usuario = cls(data['nombre'], data['id_usuario'])
        usuario.libros_prestados_isbn = data.get('libros_prestados_isbn', [])
        usuario.fecha_registro = data.get('fecha_registro', datetime.now().isoformat())
        return usuario

    def agregar_libro_prestado(self, isbn):
        """Agrega el ISBN de un libro a la lista de prestados"""
        if isbn not in self.libros_prestados_isbn:
            self.libros_prestados_isbn.append(isbn)

    def quitar_libro_prestado(self, isbn):
        """Quita el ISBN de un libro de la lista de prestados"""
        if isbn in self.libros_prestados_isbn:
            self.libros_prestados_isbn.remove(isbn)

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario}) - Libros prestados: {len(self.libros_prestados_isbn)}"


class Biblioteca:
    """Gestiona la biblioteca digital completa con persistencia en archivos"""

    def __init__(self):
        # Archivos de datos
        self.archivo_libros = "libros.txt"
        self.archivo_usuarios = "usuarios.txt"
        self.archivo_historial = "historial_prestamos.txt"

        # Diccionario para libros con ISBN como clave
        self.libros = {}
        # Conjunto para IDs de usuarios únicos
        self.ids_usuarios = set()
        # Diccionario para usuarios registrados
        self.usuarios = {}
        self.historial_prestamos = []

        # Cargar datos existentes
        self.cargar_datos()

    def guardar_libros(self):
        """Guarda todos los libros en archivo de texto"""
        try:
            with open(self.archivo_libros, 'w', encoding='utf-8') as archivo:
                libros_data = [libro.to_dict() for libro in self.libros.values()]
                json.dump(libros_data, archivo, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar libros: {e}")

    def cargar_libros(self):
        """Carga todos los libros desde archivo de texto"""
        if not os.path.exists(self.archivo_libros):
            return

        try:
            with open(self.archivo_libros, 'r', encoding='utf-8') as archivo:
                libros_data = json.load(archivo)
                for libro_data in libros_data:
                    libro = Libro.from_dict(libro_data)
                    self.libros[libro.isbn] = libro
        except Exception as e:
            print(f"Error al cargar libros: {e}")

    def guardar_usuarios(self):
        """Guarda todos los usuarios en archivo de texto"""
        try:
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as archivo:
                usuarios_data = [usuario.to_dict() for usuario in self.usuarios.values()]
                json.dump(usuarios_data, archivo, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")

    def cargar_usuarios(self):
        """Carga todos los usuarios desde archivo de texto"""
        if not os.path.exists(self.archivo_usuarios):
            return

        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as archivo:
                usuarios_data = json.load(archivo)
                for usuario_data in usuarios_data:
                    usuario = Usuario.from_dict(usuario_data)
                    self.usuarios[usuario.id_usuario] = usuario
                    self.ids_usuarios.add(usuario.id_usuario)
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")

    def guardar_historial(self):
        """Guarda el historial de préstamos en archivo de texto"""
        try:
            with open(self.archivo_historial, 'w', encoding='utf-8') as archivo:
                # Convertir fechas datetime a string para JSON
                historial_serializable = []
                for prestamo in self.historial_prestamos:
                    prestamo_copia = prestamo.copy()
                    if isinstance(prestamo_copia.get('fecha_prestamo'), datetime):
                        prestamo_copia['fecha_prestamo'] = prestamo_copia['fecha_prestamo'].isoformat()
                    if isinstance(prestamo_copia.get('fecha_devolucion'), datetime):
                        prestamo_copia['fecha_devolucion'] = prestamo_copia['fecha_devolucion'].isoformat()
                    historial_serializable.append(prestamo_copia)

                json.dump(historial_serializable, archivo, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar historial: {e}")

    def cargar_historial(self):
        """Carga el historial de préstamos desde archivo de texto"""
        if not os.path.exists(self.archivo_historial):
            return

        try:
            with open(self.archivo_historial, 'r', encoding='utf-8') as archivo:
                historial_data = json.load(archivo)
                for prestamo in historial_data:
                    # Convertir strings de fecha de vuelta a datetime
                    if isinstance(prestamo.get('fecha_prestamo'), str):
                        try:
                            prestamo['fecha_prestamo'] = datetime.fromisoformat(prestamo['fecha_prestamo'])
                        except:
                            prestamo['fecha_prestamo'] = datetime.now()

                    if isinstance(prestamo.get('fecha_devolucion'), str):
                        try:
                            prestamo['fecha_devolucion'] = datetime.fromisoformat(prestamo['fecha_devolucion'])
                        except:
                            pass

                    self.historial_prestamos.append(prestamo)
        except Exception as e:
            print(f"Error al cargar historial: {e}")

    def cargar_datos(self):
        """Carga todos los datos desde archivos"""
        self.cargar_libros()
        self.cargar_usuarios()
        self.cargar_historial()

    def guardar_datos(self):
        """Guarda todos los datos en archivos"""
        self.guardar_libros()
        self.guardar_usuarios()
        self.guardar_historial()

    def añadir_libro(self, titulo, autor, categoria, isbn):
        """Añade un libro a la biblioteca"""
        if isbn in self.libros:
            print(f"Error: Ya existe un libro con ISBN {isbn}")
            return False

        nuevo_libro = Libro(titulo, autor, categoria, isbn)
        self.libros[isbn] = nuevo_libro
        self.guardar_libros()  # Guardar cambios
        print(f"Libro '{titulo}' añadido exitosamente")
        return True

    def quitar_libro(self, isbn):
        """Quita un libro de la biblioteca"""
        if isbn not in self.libros:
            print(f"Error: No existe un libro con ISBN {isbn}")
            return False

        libro = self.libros[isbn]
        if libro.prestado:
            print(f"Error: No se puede quitar el libro '{libro.titulo}' porque está prestado")
            return False

        del self.libros[isbn]
        self.guardar_libros()  # Guardar cambios
        print(f"Libro '{libro.titulo}' eliminado exitosamente")
        return True

    def registrar_usuario(self, nombre, id_usuario=None):
        """Registra un nuevo usuario"""
        if id_usuario is None:
            id_usuario = str(uuid.uuid4())[:8]

        if id_usuario in self.ids_usuarios:
            print(f"Error: Ya existe un usuario con ID {id_usuario}")
            return None

        nuevo_usuario = Usuario(nombre, id_usuario)
        self.ids_usuarios.add(id_usuario)
        self.usuarios[id_usuario] = nuevo_usuario
        self.guardar_usuarios()  # Guardar cambios
        print(f"Usuario '{nombre}' registrado con ID: {id_usuario}")
        return nuevo_usuario

    def dar_baja_usuario(self, id_usuario):
        """Da de baja a un usuario"""
        if id_usuario not in self.ids_usuarios:
            print(f"Error: No existe usuario con ID {id_usuario}")
            return False

        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados_isbn:
            print(
                f"Error: El usuario tiene {len(usuario.libros_prestados_isbn)} libros prestados. Debe devolverlos primero.")
            return False

        self.ids_usuarios.remove(id_usuario)
        del self.usuarios[id_usuario]
        self.guardar_usuarios()  # Guardar cambios
        print(f"Usuario '{usuario.nombre}' dado de baja exitosamente")
        return True

    def prestar_libro(self, isbn, id_usuario):
        """Presta un libro a un usuario"""
        if isbn not in self.libros:
            print(f"Error: No existe libro con ISBN {isbn}")
            return False

        if id_usuario not in self.ids_usuarios:
            print(f"Error: No existe usuario con ID {id_usuario}")
            return False

        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]

        if libro.prestado:
            print(f"Error: El libro '{libro.titulo}' ya está prestado")
            return False

        libro.prestado = True
        libro.usuario_prestado = id_usuario
        usuario.agregar_libro_prestado(isbn)

        # Agregar al historial
        prestamo = {
            'usuario': usuario.nombre,
            'libro': libro.titulo,
            'isbn': isbn,
            'fecha_prestamo': datetime.now(),
            'devuelto': False
        }
        self.historial_prestamos.append(prestamo)

        # Guardar cambios
        self.guardar_datos()

        print(f"Libro '{libro.titulo}' prestado a {usuario.nombre}")
        return True

    def devolver_libro(self, isbn, id_usuario):
        """Devuelve un libro"""
        if isbn not in self.libros:
            print(f"Error: No existe libro con ISBN {isbn}")
            return False

        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]

        if not libro.prestado or libro.usuario_prestado != id_usuario:
            print(f"Error: El libro '{libro.titulo}' no está prestado a este usuario")
            return False

        libro.prestado = False
        libro.usuario_prestado = None
        usuario.quitar_libro_prestado(isbn)

        # Actualizar historial
        for prestamo in self.historial_prestamos:
            if (prestamo['isbn'] == isbn and
                    prestamo['usuario'] == usuario.nombre and
                    not prestamo['devuelto']):
                prestamo['devuelto'] = True
                prestamo['fecha_devolucion'] = datetime.now()
                break

        # Guardar cambios
        self.guardar_datos()

        print(f"Libro '{libro.titulo}' devuelto por {usuario.nombre}")
        return True

    def buscar_libros(self, criterio, valor):
        """Busca libros por título, autor o categoría"""
        resultados = []
        valor_lower = valor.lower()

        for libro in self.libros.values():
            if criterio == "titulo" and valor_lower in libro.titulo.lower():
                resultados.append(libro)
            elif criterio == "autor" and valor_lower in libro.autor.lower():
                resultados.append(libro)
            elif criterio == "categoria" and valor_lower in libro.categoria.lower():
                resultados.append(libro)

        return resultados

    def listar_libros_prestados(self, id_usuario):
        """Lista todos los libros prestados a un usuario"""
        if id_usuario not in self.ids_usuarios:
            print(f"Error: No existe usuario con ID {id_usuario}")
            return []

        usuario = self.usuarios[id_usuario]
        libros_prestados = []

        for isbn in usuario.libros_prestados_isbn:
            if isbn in self.libros:
                libros_prestados.append(self.libros[isbn])

        return libros_prestados

    def mostrar_todos_los_libros(self):
        """Muestra todos los libros de la biblioteca"""
        if not self.libros:
            print("No hay libros en la biblioteca")
            return

        print("\n" + "=" * 60)
        print("CATÁLOGO COMPLETO DE LIBROS")
        print("=" * 60)
        for libro in self.libros.values():
            print(libro)

    def mostrar_usuarios(self):
        """Muestra todos los usuarios registrados"""
        if not self.usuarios:
            print("No hay usuarios registrados")
            return

        print("\n" + "=" * 50)
        print("USUARIOS REGISTRADOS")
        print("=" * 50)
        for usuario in self.usuarios.values():
            print(usuario)


def inicializar_biblioteca():
    """Inicializa la biblioteca y agrega libros predeterminados si no existen"""
    biblioteca = Biblioteca()

    # Si no hay libros cargados, agregar los iniciales
    if not biblioteca.libros:
        libros_iniciales = [
            ("Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", "978-0001"),
            ("1984", "George Orwell", "Distopía", "978-0002"),
            ("Cien años de soledad", "Gabriel García Márquez", "Realismo mágico", "978-0003"),
            ("Orgullo y prejuicio", "Jane Austen", "Clásico", "978-0004"),
            ("Frankenstein", "Mary Shelley", "Ciencia ficción", "978-0005"),
            ("El Principito", "Antoine de Saint-Exupéry", "Fábula", "978-0006"),
            ("La Odisea", "Homero", "Clásico", "978-0007"),
            ("El Hobbit", "J.R.R. Tolkien", "Fantasía", "978-0008"),
            ("El código Da Vinci", "Dan Brown", "Thriller", "978-0009")
        ]

        print("Inicializando biblioteca con libros predeterminados...")
        for titulo, autor, categoria, isbn in libros_iniciales:
            biblioteca.añadir_libro(titulo, autor, categoria, isbn)
    else:
        print(f"Biblioteca cargada: {len(biblioteca.libros)} libros, {len(biblioteca.usuarios)} usuarios")

    return biblioteca


def menu_principal():
    """Menú interactivo principal"""
    biblioteca = inicializar_biblioteca()

    while True:
        print("\n" + "=" * 50)
        print("SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL")
        print("=" * 50)
        print("1. Ver todos los libros")
        print("2. Buscar libros")
        print("3. Añadir libro")
        print("4. Quitar libro")
        print("5. Registrar usuario")
        print("6. Ver usuarios registrados")
        print("7. Dar de baja usuario")
        print("8. Prestar libro")
        print("9. Devolver libro")
        print("10. Ver libros prestados de un usuario")
        print("11. Ver historial de préstamos")
        print("12. Guardar datos manualmente")
        print("0. Salir")
        print("-" * 50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            biblioteca.mostrar_todos_los_libros()

        elif opcion == "2":
            print("\nBuscar por:")
            print("1. Título")
            print("2. Autor")
            print("3. Categoría")
            criterio_num = input("Seleccione criterio: ").strip()

            criterios = {"1": "titulo", "2": "autor", "3": "categoria"}
            if criterio_num in criterios:
                valor = input(f"Ingrese {criterios[criterio_num]} a buscar: ").strip()
                resultados = biblioteca.buscar_libros(criterios[criterio_num], valor)

                if resultados:
                    print(f"\nSe encontraron {len(resultados)} resultado(s):")
                    for libro in resultados:
                        print(libro)
                else:
                    print("No se encontraron libros con ese criterio")

        elif opcion == "3":
            titulo = input("Título del libro: ").strip()
            autor = input("Autor del libro: ").strip()
            categoria = input("Categoría del libro: ").strip()
            isbn = input("ISBN del libro: ").strip()

            if titulo and autor and categoria and isbn:
                biblioteca.añadir_libro(titulo, autor, categoria, isbn)
            else:
                print("Error: Todos los campos son obligatorios")

        elif opcion == "4":
            isbn = input("ISBN del libro a quitar: ").strip()
            biblioteca.quitar_libro(isbn)

        elif opcion == "5":
            nombre = input("Nombre del usuario: ").strip()
            id_usuario = input("ID de usuario (presione Enter para generar automáticamente): ").strip()

            if nombre:
                if not id_usuario:
                    id_usuario = None
                biblioteca.registrar_usuario(nombre, id_usuario)
            else:
                print("Error: El nombre es obligatorio")

        elif opcion == "6":
            biblioteca.mostrar_usuarios()

        elif opcion == "7":
            id_usuario = input("ID del usuario a dar de baja: ").strip()
            biblioteca.dar_baja_usuario(id_usuario)

        elif opcion == "8":
            isbn = input("ISBN del libro a prestar: ").strip()
            id_usuario = input("ID del usuario: ").strip()
            biblioteca.prestar_libro(isbn, id_usuario)

        elif opcion == "9":
            isbn = input("ISBN del libro a devolver: ").strip()
            id_usuario = input("ID del usuario: ").strip()
            biblioteca.devolver_libro(isbn, id_usuario)

        elif opcion == "10":
            id_usuario = input("ID del usuario: ").strip()
            libros_prestados = biblioteca.listar_libros_prestados(id_usuario)

            if libros_prestados:
                print(f"\nLibros prestados:")
                for libro in libros_prestados:
                    print(f"- {libro}")
            else:
                print("El usuario no tiene libros prestados")

        elif opcion == "11":
            if biblioteca.historial_prestamos:
                print("\n" + "=" * 60)
                print("HISTORIAL DE PRÉSTAMOS")
                print("=" * 60)
                for prestamo in biblioteca.historial_prestamos:
                    estado = "Devuelto" if prestamo['devuelto'] else "Pendiente"
                    fecha_dev = f" - Devuelto: {prestamo.get('fecha_devolucion', 'N/A')}" if prestamo[
                        'devuelto'] else ""
                    print(
                        f"'{prestamo['libro']}' - {prestamo['usuario']} - Prestado: {prestamo['fecha_prestamo']} - Estado: {estado}{fecha_dev}")
            else:
                print("No hay historial de préstamos")

        elif opcion == "12":
            biblioteca.guardar_datos()
            print("Datos guardados manualmente en los archivos")

        elif opcion == "0":
            print("Guardando datos...")
            biblioteca.guardar_datos()
            print("¡Gracias por usar el Sistema de Gestión de Biblioteca Digital!")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()