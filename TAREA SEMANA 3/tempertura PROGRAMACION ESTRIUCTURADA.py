def promedio_temperaturas():
    temperaturas = []
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    print("Ingresa las temperaturas de la semana:")
    for dia in dias:
        temp = float(input(f"{dia}: "))
        temperaturas.append(temp)

    promedio = sum(temperaturas) / 7
    print(f"El promedio es: {promedio:.2f}°C")

    return promedio

# Ejecutar la función
promedio_temperaturas()