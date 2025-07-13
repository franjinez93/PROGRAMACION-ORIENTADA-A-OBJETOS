class Vehiculo:  # usage
    def __init__(self, placa, tipo_vehiculo):
        # Constructor: se llama al crear el objeto (entrada al parqueadero)
        self.placa = placa
        self.tipo_vehiculo = tipo_vehiculo
        print("Ingreso exitoso del vehiculo ")

    def mostrar_info(self):  # usage
        print(f'''Información del vehículo: {self.tipo_vehiculo} 
Placa: {self.placa}''')

    def __del__(self):
        # Destructor: se llama automáticamente cuando el objeto se elimina (salida del parqueadero)
        print("Salida del vehiculo")
        print("Adios")

# Ingreso de vehículos
vehiculo1 = Vehiculo("PDH 5340", "Automóvil HAVAL M4")

vehiculo1.mostrar_info()