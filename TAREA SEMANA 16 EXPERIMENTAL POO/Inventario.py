import json
from Producto import Producto


class Inventario:
    def __init__(self):
        self.productos = {}
        self.archivo = 'inventario.json'
        self.cargar_inventario()
        self.cargar_datos_ejemplo()

    def agregar_producto(self, id_producto, nombre, cantidad, precio):
        if id_producto in self.productos:
            return False
        self.productos[id_producto] = Producto(id_producto, nombre, cantidad, precio)
        self.guardar_inventario()
        return True

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_inventario()
            return True
        return False

    def modificar_producto(self, id_producto, nombre=None, cantidad=None, precio=None):
        if id_producto in self.productos:
            producto = self.productos[id_producto]
            if nombre:
                producto.set_nombre(nombre)
            if cantidad is not None:
                producto.set_cantidad(cantidad)
            if precio is not None:
                producto.set_precio(precio)
            self.guardar_inventario()
            return True
        return False

    def mostrar_todos_productos(self):
        return list(self.productos.values())

    def guardar_inventario(self):
        try:
            with open(self.archivo, 'w') as f:
                datos = {str(id): prod.to_dict() for id, prod in self.productos.items()}
                json.dump(datos, f, indent=4)
        except Exception as e:
            print(f"Error guardando inventario: {e}")

    def cargar_inventario(self):
        try:
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                for id_str, prod_data in datos.items():
                    id_producto = int(id_str)
                    self.productos[id_producto] = Producto(
                        id_producto,
                        prod_data['nombre'],
                        prod_data['cantidad'],
                        prod_data['precio']
                    )
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error cargando inventario: {e}")

    def cargar_datos_ejemplo(self):
        # Cargar productos de ejemplo si el inventario está vacío
        if not self.productos:
            productos_ejemplo = [
                (1, "Laptop HP Pavilion", 5, 899.99),
                (2, "Mouse Inalámbrico", 15, 25.50),
                (3, "Teclado Mecánico", 8, 75.00),
                (4, "Monitor 24 pulgadas", 3, 199.99),
                (5, "Impresora Laser", 4, 299.50),
                (6, "Router WiFi Doble Banda", 10, 50.50),
                (7, "Cargador USB-C Rápido", 25, 20.00),
                (8, "Altavoz Portátil", 28, 45.00),
                (9, "Licencia Microsoft Office", 80, 65.00),
                (10, "Pendrive USB 128GB", 30, 15.75)
            ]
            for id_producto, nombre, cantidad, precio in productos_ejemplo:
                self.agregar_producto(id_producto, nombre, cantidad, precio)