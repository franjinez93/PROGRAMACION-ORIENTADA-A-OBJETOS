class Zapato:
    def __init__(self, marca, talla):
        self.marca = marca
        self.talla = talla
        self.propietario = None  # Inicialmente, el zapato no tiene propietario
        self.vendedor = None  # Inicialmente, el zapato no tiene vendedor

    def asignar_propietario(self, comprador):
        if isinstance(comprador, Comprador):
            self.propietario = comprador

    def asignar_vendedor(self, vendedor):
        if isinstance(vendedor, Vendedor):
            self.vendedor = vendedor

    def __str__(self):
        return f'Zapato {self.marca} talla {self.talla}, usado por {self.propietario.nombre if self.propietario else "nadie"}, vendido por {self.vendedor.nombre if self.vendedor else "nadie"}.'


class Comprador:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def __str__(self):
        return f'Comprador {self.nombre} de {self.edad} años.'


class Vendedor:
    def __init__(self, nombre, tienda):
        self.nombre = nombre
        self.tienda = tienda

    def __str__(self):
        return f'Vendedor {self.nombre} de la tienda {self.tienda}.'


# Creación de objetos
zapato1 = Zapato('Nike', 42)
zapato2 = Zapato('Adidas', 38)
comprador = Comprador('Carlos', 25)
vendedor = Vendedor('María', 'Deportes Express')

# Asignar un propietario y vendedor al zapato
zapato1.asignar_propietario(comprador)
zapato1.asignar_vendedor(vendedor)

# Ejemplo de salida
print(zapato1)  # Debería imprimir: Zapato Nike talla 42, usado por Carlos, vendido por María.
print(zapato2)  # Debería imprimir: Zapato Adidas talla 38, usado por nadie, vendido por nadie.
print(comprador)  # Debería imprimir: Comprador Carlos de 25 años.
print(vendedor)  # Debería imprimir: Vendedor María de la tienda Deportes Express.