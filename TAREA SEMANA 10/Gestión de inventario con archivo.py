import os

# Clase Producto: Representa cada artículo dentro del inventario
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"

    # Para guardar el producto en archivo como texto plano
    def to_file_format(self):
        return f"{self.id};{self.nombre};{self.cantidad};{self.precio}"

    @staticmethod
    def from_file_format(linea):
        parts = linea.strip().split(";")
        if len(parts) == 4:  # ID;Nombre;Cantidad;Precio
            return Producto(parts[0], parts, int(parts), float(parts))
        return None


# Clase Inventario con persistencia en archivo
class Inventario:
    ARCHIVO = "inventario.txt"

    def __init__(self):
        self.productos = []
        self.cargar_desde_archivo()

    # Cargar productos desde el archivo (si existe)
    def cargar_desde_archivo(self):
        if not os.path.exists(self.ARCHIVO):
            # Si no existe, lo crea con los 2 productos por defecto
            self.añadir_producto(Producto("ID001", "Galletas Saladitas", 20, 0.40))
            self.añadir_producto(Producto("ID002", "Chicle Agogo", 30, 0.10))
            self.guardar_en_archivo()
            return

        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                for linea in f:
                    producto = Producto.from_file_format(linea)
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
                for p in self.productos:
                    f.write(p.to_file_format() + "\n")
        except PermissionError:
            print("Error: No tienes permisos para escribir en el archivo de inventario.")

    def añadir_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            return False
        self.productos.append(producto)
        self.guardar_en_archivo()
        return True

    def eliminar_producto(self, id):
        for p in self.productos:
            if p.get_id() == id:
                self.productos.remove(p)
                self.guardar_en_archivo()
                return True
        return False

    def actualizar_producto(self, id, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                self.guardar_en_archivo()
                return True
        return False

    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]

    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            for p in self.productos:
                print(p)


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
                nuevo = Producto(id, nombre, cantidad, precio)
                if inventario.añadir_producto(nuevo):
                    print(" Producto añadido con éxito al inventario y archivo.")
                else:
                    print(" Error: el ID ya existe.")
            except ValueError:
                print(" Datos inválidos.")

        elif opcion == "2":
            id = input("ID a eliminar: ")
            if inventario.eliminar_producto(id):
                print(" Producto eliminado del inventario y archivo.")
            else:
                print(" No se encontró el producto.")

        elif opcion == "3":
            id = input("ID del producto a actualizar: ")
            nueva_cantidad = input("Nueva cantidad (enter para no cambiar): ")
            nuevo_precio = input("Nuevo precio (enter para no cambiar): ")
            try:
                cantidad = int(nueva_cantidad) if nueva_cantidad.strip() else None
                precio = float(nuevo_precio) if nuevo_precio.strip() else None
                if inventario.actualizar_producto(id, cantidad, precio):
                    print(" Producto actualizado en inventario y archivo.")
                else:
                    print(" No se encontró el producto.")
            except ValueError:
                print(" Datos inválidos.")

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                for p in resultados:
                    print(p)
            else:
                print(" No se encontraron productos.")

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "0":
            print(" Saliendo...")
            break

        else:
            print(" Opción inválida.")


if __name__ == "__main__":
    menu()
