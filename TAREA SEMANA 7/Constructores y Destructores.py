# Ejercicio: Sistema de Universidad Estatal Amazónica (Uso de Constructores y Destructores en Python)
# Cada vez que un estudiante entra a la universidad, se crea una instancia de la clase 'estudiante_uea',
# lo cual representa su entrada. Cuando el estudiante sale (el objeto se elimina), se ejecuta
# automáticamente el destructor para simular la salida de la universidad.

class estudiante_uea:  # usage
    def __init__(self, nombre, cedula):
        # Constructor: se llama al crear el objeto (entrada a la universidad)
        self.nombre = nombre
        self.cedula = cedula
        print("Estudiante ingreso a la UEA")

    def mostrar_info(self):  # usage
        print(f'''Información del estudiante:
        Nombre: {self.nombre}
        Cédula: {self.cedula}''')

    def __del__(self):
        # Destructor: se llama automáticamente cuando el objeto se elimina (salida de la universidad)
        print("Estudiante salio de la UEA")
# Ingreso de estudiantes
estudiante1 = estudiante_uea("Francisco Jinez", "1003867429")

estudiante1.mostrar_info()
