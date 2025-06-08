# Abstracción: Creamos una clase abstracta que representa un animal doméstico
class AnimalDomestico:
    def __init__(self, nombre, peso, raza):
        self._nombre = nombre            # Encapsulamiento: atributo protegido
        self._peso = peso                # Encapsulamiento: atributo protegido
        self._raza = raza                # Encapsulamiento: atributo protegido

    def atributos(self):
        print(self._nombre, ":", sep="")
        print(".nombre:", self._nombre)
        print(".peso:", self._peso)
        print(".raza:", self._raza)

    def comer(self):
        print(self._nombre, "está comiendo.")

    def jugar(self):
        print(self._nombre, "está jugando.")


# Herencia: Perro hereda de AnimalDomestico
class Perro(AnimalDomestico):
    def __init__(self, nombre, peso, raza, ruido):
        super().__init__(nombre, peso, raza)
        self._ruido = ruido

    def hacer_ruido_del_perro(self):  # Polimorfismo
        print(self._nombre, "dice", self._ruido)

    def atributos(self):  # Polimorfismo sobrescribiendo
        super().atributos()
        print(self._nombre,"dice", self._ruido)

# Herencia: gato hereda de AnimalDomestico
class gato(AnimalDomestico):
    def __init__(self, nombre, peso, raza, ruido):
        super().__init__(nombre, peso, raza)
        self._ruido = ruido

    def hacer_ruido_del_gato(self):  # Polimorfismo
        print(self._nombre, "dice", self._ruido)

    def atributos(self):  # Polimorfismo sobrescribiendo
        super().atributos()
        print(self._nombre, "dice", self._ruido)

# Crear objeto (instancia)
mi_perro = Perro("Max", 15, "Labrador", "Guau Guau")
mi_gato = gato("Misifu",4 , "siames", "Miau")

# Probar métodos
mi_perro.atributos()
mi_perro.comer()
mi_perro.jugar()

mi_gato.atributos()
mi_gato.comer()
mi_gato.jugar()