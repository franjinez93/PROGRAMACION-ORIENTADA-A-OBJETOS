import os


# Clase Inventario con persistencia en archivo usando diccionarios
class Inventario:
    ARCHIVO = "inventario.txt"

    def __init__(self):
        self.productos = []  # Lista de diccionarios
        self.cargar_desde_archivo()

    # Crear un producto como diccionario
    def crear_producto(self, id, nombre, cantidad, precio):
        return {
            'id': id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio
        }

    # Convertir diccionario a formato de archivo
    def producto_to_file_format(self, producto):
        return f"{{\n    'id': '{producto['id']}',\n    'nombre': '{producto['nombre']}',\n    'cantidad': {producto['cantidad']},\n    'precio': {producto['precio']}\n}}"

    # Convertir línea de archivo a diccionario
    def producto_from_file_format(self, linea):
        try:
            # Evalúa la cadena como un diccionario Python
            producto = eval(linea.strip())
            # Verificar que tenga las claves necesarias
            if isinstance(producto, dict) and all(key in producto for key in ['id', 'nombre', 'cantidad', 'precio']):
                return producto
        except:
            pass
        return None

    # Cargar productos desde el archivo (si existe)
    def cargar_desde_archivo(self):
        if not os.path.exists(self.ARCHIVO):
            # Si no existe, lo crea con los 2 productos por defecto
            self.añadir_producto("ID001", "Galletas Saladitas", 20, 0.40)
            self.añadir_producto("ID002", "Chicle Agogo", 30, 0.10)
            self.guardar_en_archivo()
            return

        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                contenido = f.read()
                # Dividir por dobles saltos de línea para separar productos
                productos_texto = contenido.split('\n\n')
                for producto_texto in productos_texto:
                    if producto_texto.strip():  # Si no está vacío
                        producto = self.producto_from_file_format(producto_texto)
                        if producto:
                            self.productos.append(producto)
        except FileNotFoundError:
            print("El archivo de inventario no existe, se creará uno nuevo.")
        except PermissionError:
            print("Error: No tienes permisos para leer el archivo de inventario.")

    # Guardar todo el inventario en archivo
    def guardar_en_archivo(self):
        try:
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                for i, producto in enumerate(self.productos):
                    f.write(self.producto_to_file_format(producto))
                    if i < len(self.productos) - 1:  # No agregar línea extra al final
                        f.write("\n\n")  # Doble salto entre productos
                    else:
                        f.write("\n")
        except PermissionError:
            print("Error: No tienes permisos para escribir en el archivo de inventario.")

    # Buscar producto por ID
    def buscar_producto_por_id(self, id):
        for producto in self.productos:
            if producto['id'] == id:
                return producto
        return None

    def añadir_producto(self, id, nombre, cantidad, precio):
        # Verificar si el ID ya existe
        if self.buscar_producto_por_id(id):
            return False

        nuevo_producto = self.crear_producto(id, nombre, cantidad, precio)
        self.productos.append(nuevo_producto)
        self.guardar_en_archivo()
        return True

    def eliminar_producto(self, id):
        producto = self.buscar_producto_por_id(id)
        if producto:
            self.productos.remove(producto)
            self.guardar_en_archivo()
            return True
        return False

    def actualizar_producto(self, id, nueva_cantidad=None, nuevo_precio=None):
        producto = self.buscar_producto_por_id(id)
        if producto:
            if nueva_cantidad is not None:
                producto['cantidad'] = nueva_cantidad
            if nuevo_precio is not None:
                producto['precio'] = nuevo_precio
            self.guardar_en_archivo()
            return True
        return False

    def buscar_por_nombre(self, nombre):
        resultados = []
        for producto in self.productos:
            if nombre.lower() in producto['nombre'].lower():
                resultados.append(producto)
        return resultados

    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            for producto in self.productos:
                print(f"ID: {producto['id']} | Nombre: {producto['nombre']} | "
                      f"Cantidad: {producto['cantidad']} | Precio: ${producto['precio']:.2f}")


# Función menú con interfaz de consola
def menu():
    inventario = Inventario()

    while True:
        print("\n=== MENÚ INVENTARIO ===")
        print("1. Añadir producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                if inventario.añadir_producto(id, nombre, cantidad, precio):
                    print("Producto añadido con éxito al inventario y archivo.")
                else:
                    print("Error: el ID ya existe.")
            except ValueError:
                print("Datos inválidos.")

        elif opcion == "2":
            id = input("ID a eliminar: ")
            if inventario.eliminar_producto(id):
                print("Producto eliminado del inventario y archivo.")
            else:
                print("No se encontró el producto.")

        elif opcion == "3":
            id = input("ID del producto a actualizar: ")
            nueva_cantidad = input("Nueva cantidad (enter para no cambiar): ")
            nuevo_precio = input("Nuevo precio (enter para no cambiar): ")
            try:
                cantidad = int(nueva_cantidad) if nueva_cantidad.strip() else None
                precio = float(nuevo_precio) if nuevo_precio.strip() else None
                if inventario.actualizar_producto(id, cantidad, precio):
                    print("Producto actualizado en inventario y archivo.")
                else:
                    print("No se encontró el producto.")
            except ValueError:
                print("Datos inválidos.")

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print(f"\nSe encontraron {len(resultados)} producto(s):")
                for producto in resultados:
                    print(f"ID: {producto['id']} | Nombre: {producto['nombre']} | "
                          f"Cantidad: {producto['cantidad']} | Precio: ${producto['precio']:.2f}")
            else:
                print("No se encontraron productos.")

        elif opcion == "5":
            print(f"\nInventario actual ({len(inventario.productos)} productos):")
            inventario.mostrar_productos()

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()