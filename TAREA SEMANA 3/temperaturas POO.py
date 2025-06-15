class TemperaturaDia:
    def __init__(self):
        self.temperaturas = []
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    def ingresar_temperaturas(self):
        print("Ingresa las temperaturas por dias de la semana")
        for dia in self.dias:
            temp = float(input(f"{dia}: "))
            self.temperaturas.append(temp)

    def mostrar_temperaturas(self):
        for i, dia in enumerate(self.dias):
            print(f"{dia}: {self.temperaturas[i]}°C")


class SemanaTemp:
    def __init__(self, temperatura_dia):
        self.temp_dia = temperatura_dia

    def calcular_promedio(self):
        promedio = sum(self.temp_dia.temperaturas) / 7
        return promedio

    def mostrar_promedio(self):
        promedio = self.calcular_promedio()
        print(f"El promedio es: {promedio:.2f}°C")



temp_dia = TemperaturaDia()
temp_dia.ingresar_temperaturas()

semana = SemanaTemp(temp_dia)
semana.mostrar_promedio()