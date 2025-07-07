"""
Sistema de Veterinaria Simple
Programa que demuestra los conceptos básicos de POO: Herencia, Encapsulación y Polimorfismo
"""

"""La clase animal es en general"""


class Animal:

    def __init__(self, nombre, edad):
        """Constructor con atributos privados para demostrar encapsulación."""
        self._nombre = nombre  # Atributo privado encapsulado
        self._edad = edad  # Atributo privado encapsulado

    # Métodos getter para demostrar encapsulación
    @property
    def nombre(self):
        """Getter para obtener el nombre del animal (encapsulación)."""
        return self._nombre

    @property
    def edad(self):
        """Getter para obtener la edad del animal (encapsulación)."""
        return self._edad

    def hacer_sonido(self):
        """
        Método que será sobrescrito en las clases derivadas.
        Demuestra POLIMORFISMO a través de métodos sobrescritos.
        """
        print(f"{self._nombre} hace un sonido genérico.")

    def obtener_info(self):
        """Método para obtener información básica del animal."""
        return f"{self._nombre} tiene {self._edad} años"


class Perro(Animal):
    """
    Clase derivada que representa un perro.
    Demuestra HERENCIA al heredar de la clase Animal.
    """

    def __init__(self, nombre, edad):
        """Constructor que utiliza super() para llamar al constructor padre (herencia)."""
        super().__init__(nombre, edad)  # Llamada al constructor padre
        self._juega = True

    @property
    def juega(self):
        return self._juega

    def hacer_sonido(self):
        """
        Método sobrescrito que demuestra POLIMORFISMO.
        Modificación específica para perros.
        """
        print(f"{self._nombre} dice: guau, guau")


class Gato(Animal):
    """
    Clase derivada que representa un gato.
    Demuestra HERENCIA al heredar de la clase Animal.
    """

    def __init__(self, nombre, edad):
        """Constructor que utiliza super() para llamar al constructor padre (herencia)."""
        super().__init__(nombre, edad)  # Llamada al constructor padre
        self._ronronea = True

    @property
    def ronronea(self):
        return self._ronronea

    def hacer_sonido(self):
        """
        Método sobrescrito que demuestra POLIMORFISMO.
        Modificación específica para gatos.
        """
        print(f"{self._nombre} dice: miau, miau")


class Loro(Animal):
    """
    Clase derivada que representa un loro.
    Demuestra HERENCIA al heredar de la clase Animal.
    """

    def __init__(self, nombre, edad):
        """Constructor que utiliza super() para llamar al constructor padre (herencia)."""
        super().__init__(nombre, edad)  # Llamada al constructor padre
        self._vuela = True

    @property
    def vuela(self):
        return self._vuela

    def hacer_sonido(self):
        """
        Método sobrescrito que demuestra POLIMORFISMO.
        Modificación específica para loros.
        """
        print(f"{self._nombre} dice: hola hola ")


def main():
    """
    Función principal que demuestra los conceptos de POO.
    """
    print("\n Animales de la veterinaria")

    # Crear animales - cada uno hereda de Animal
    perro = Perro("Lucas", 1)
    gato = Gato("Pelos", 8)
    loro = Loro("Luchin", 4)

    # Lista de animales para demostrar polimorfismo
    animales = [perro, gato, loro]
    for i, animal in enumerate(animales, 1):
        print(f"{i}. {animal.obtener_info()}")
        print(f" ")

    for animal in animales:
        print(f"Nombre: {animal.nombre}")
        print(f"Edad: {animal.edad}")
        print(f"Tipo de animal: {type(animal).__name__}")

        # Mostrar atributos específicos
        if isinstance(animal, Perro):
            print(f"Juega: {animal.juega}")
        elif isinstance(animal, Gato):
            print(f"Ronronea: {animal.ronronea}")
        elif isinstance(animal, Loro):
            print(f"Vuela: {animal.vuela}")

        print(f" ")

    # Polimorfismo de sobre escritura con los sonidos de los animales
    for animal in animales:
        animal.hacer_sonido()


# Ejecutar el programa principal
if __name__ == "__main__":
    main()