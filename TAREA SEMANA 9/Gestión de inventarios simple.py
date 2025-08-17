# Clase Producto: Representa cada artículo dentro del inventario
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        # Constructor que inicializa los atributos del producto
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Métodos getter: permiten obtener el valor de los atributos
    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Métodos setter: permiten modificar los valores de los atributos
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    # Representación en texto de un producto, útil para imprimir directamente
    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


# Clase Inventario: se encarga de gestionar la lista de productos
class Inventario:
    def __init__(self):
        self.productos = []  # Aquí guardaremos los productos en una lista

        # Al iniciar el inventario, cargamos dos productos por defecto
        self.añadir_producto(Producto("ID001", "Galletas Saladitas", 20, 0.40))
        self.añadir_producto(Producto("ID002", "Chicle Agogo", 30, 0.10))

    # Añadir un producto al inventario (verifica que el ID no esté repetido)
    def añadir_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            return False  # Si el ID ya existe, no lo agrega
        self.productos.append(producto)
        return True

    # Eliminar producto por su ID
    def eliminar_producto(self, id):
        for p in self.productos:
            if p.get_id() == id:
                self.productos.remove(p)
                return True
        return False  # Si no lo encuentra, devuelve False

    # Actualizar cantidad o precio de un producto según su ID
    def actualizar_producto(self, id, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id:
                if nueva_cantidad is not None:  # Solo actualiza si el usuario da un valor
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                return True
        return False

    # Buscar producto(s) que contengan en su nombre el texto ingresado
    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]

    # Mostrar todos los productos que hay en el inventario
    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            for p in self.productos:
                print(p)


# Función menú con interfaz de consola
def menu():
    inventario = Inventario()  # Se crea un inventario al iniciar el menú

    while True:
        # Menú de opciones
        print("\n=== MENÚ INVENTARIO ===")
        print("1. Añadir producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        # Caso 1: Añadir producto
        if opcion == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                nuevo = Producto(id, nombre, cantidad, precio)
                if inventario.añadir_producto(nuevo):
                    print("Producto añadido con éxito.")
                else:
                    print("Error: el ID ya existe.")
            except ValueError:
                print("Datos inválidos.")

        # Caso 2: Eliminar producto
        elif opcion == "2":
            id = input("ID a eliminar: ")
            if inventario.eliminar_producto(id):
                print("Producto eliminado.")
            else:
                print("No se encontró el producto.")

        # Caso 3: Actualizar producto
        elif opcion == "3":
            id = input("ID del producto a actualizar: ")
            nueva_cantidad = input("Nueva cantidad (enter para no cambiar): ")
            nuevo_precio = input("Nuevo precio (enter para no cambiar): ")

            # Si el usuario no escribe nada, deja el valor como None
            cantidad = int(nueva_cantidad) if nueva_cantidad.strip() else None
            precio = float(nuevo_precio) if nuevo_precio.strip() else None

            if inventario.actualizar_producto(id, cantidad, precio):
                print("Producto actualizado.")
            else:
                print("No se encontró el producto.")

        # Caso 4: Buscar producto(s) por nombre
        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos.")

        # Caso 5: Mostrar inventario completo
        elif opcion == "5":
            inventario.mostrar_productos()

        # Caso 0: Terminar el programa
        elif opcion == "0":
            print("Saliendo...")
            break

        # Si el usuario ingresa una opción inválida
        else:
            print("Opción inválida.")


# Punto inicial del programa
if __name__ == "__main__":
    menu()