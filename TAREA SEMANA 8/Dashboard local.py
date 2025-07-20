import os
import subprocess


def mostrar_codigo(ruta_script):
    # Asegúrate de que la ruta al script es absoluta
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None


def ejecutar_codigo(ruta_script):
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")


def mostrar_menu():
    # Define la ruta base donde se encuentra el proyecto PROGRAMACION-ORIENTADA-A-OBJETOS
    ruta_base = r"C:\Users\FRANCISCO\PycharmProjects\PROGRAMACION-ORIENTADA-A-OBJETOS"

    # Verificar si la ruta existe
    if not os.path.exists(ruta_base):
        print(f"Error: No se encontró el directorio {ruta_base}")
        print("Por favor, verifica que la ruta sea correcta.")
        return

    # Obtener todas las carpetas TAREA SEMANA dinámicamente
    carpetas_tarea = {}
    try:
        for carpeta in os.listdir(ruta_base):
            ruta_carpeta = os.path.join(ruta_base, carpeta)
            if os.path.isdir(ruta_carpeta) and carpeta.startswith("TAREA SEMANA"):
                # Extraer el número de semana para usar como clave
                numero_semana = carpeta.replace("TAREA SEMANA ", "")
                carpetas_tarea[numero_semana] = carpeta
    except Exception as e:
        print(f"Error al leer el directorio: {e}")
        return

    if not carpetas_tarea:
        print("No se encontraron carpetas 'TAREA SEMANA' en el directorio especificado.")
        return

    while True:
        print(f"\nMenu Principal - Dashboard")
        print(f"Directorio: {ruta_base}")
        print("=" * 50)

        # Imprime las opciones del menú principal ordenadas
        for key in sorted(carpetas_tarea.keys(), key=int):
            print(f"{key} - {carpetas_tarea[key]}")
        print("0 - Salir")

        eleccion_unidad = input("\nElige una semana o '0' para salir: ")
        if eleccion_unidad == '0':
            print("Saliendo del programa.")
            break
        elif eleccion_unidad in carpetas_tarea:
            mostrar_sub_menu(os.path.join(ruta_base, carpetas_tarea[eleccion_unidad]))
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")


def mostrar_sub_menu(ruta_unidad):
    if not os.path.exists(ruta_unidad):
        print(f"Error: No se encontró el directorio {ruta_unidad}")
        return

    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    if not sub_carpetas:
        print("No se encontraron subcarpetas en este directorio.")
        # Si no hay subcarpetas, buscar scripts directamente
        mostrar_scripts(ruta_unidad)
        return

    while True:
        print(f"\nSubmenú - Selecciona una subcarpeta")
        print(f"Directorio: {ruta_unidad}")
        print("=" * 50)

        # Imprime las subcarpetas
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion_carpeta = input("\nElige una subcarpeta o '0' para regresar: ")
        if eleccion_carpeta == '0':
            break
        else:
            try:
                eleccion_carpeta = int(eleccion_carpeta) - 1
                if 0 <= eleccion_carpeta < len(sub_carpetas):
                    mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[eleccion_carpeta]))
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")


def mostrar_scripts(ruta_sub_carpeta):
    if not os.path.exists(ruta_sub_carpeta):
        print(f"Error: No se encontró el directorio {ruta_sub_carpeta}")
        return

    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

    if not scripts:
        print("No se encontraron scripts de Python (.py) en este directorio.")
        input("Presiona Enter para regresar...")
        return

    while True:
        print(f"\nScripts - Selecciona un script para ver y ejecutar")
        print(f"Directorio: {ruta_sub_carpeta}")
        print("=" * 50)

        # Imprime los scripts
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar al submenú anterior")
        print("9 - Regresar al menú principal")

        eleccion_script = input("\nElige un script, '0' para regresar o '9' para ir al menú principal: ")
        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return  # Regresar al menú principal
        else:
            try:
                eleccion_script = int(eleccion_script) - 1
                if 0 <= eleccion_script < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion_script])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("\n¿Desea ejecutar el script? (1: Sí, 0: No): ")
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print("Opción no válida. Regresando al menú de scripts.")
                        input("\nPresiona Enter para volver al menú de scripts.")
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")


# Ejecutar el dashboard
if __name__ == "__main__":
    mostrar_menu()
