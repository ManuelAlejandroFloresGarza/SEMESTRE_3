import re  # Importa el módulo re para trabajar con expresiones regulares

class Nota:
    def __init__(self, folio, fecha, cliente):
        self.folio = folio  # Asigna el folio a la instancia de la clase
        self.fecha = fecha  # Asigna la fecha a la instancia de la clase
        self.cliente = cliente  # Asigna el cliente a la instancia de la clase
        self.servicios = []  # Inicializa una lista vacía para almacenar servicios
        self.monto_total = 0.0  # Inicializa el monto total en 0.0
        self.cancelada = False  # Inicializa el estado de cancelación en False (no cancelada)

    def agregar_servicio(self, nombre_servicio, costo_servicio):
        try:
            costo_servicio = float(costo_servicio)  # Convierte el costo del servicio en un número decimal
            self.servicios.append((nombre_servicio, costo_servicio))  # Agrega el servicio a la lista de servicios
            self.monto_total += costo_servicio  # Actualiza el monto total
        except ValueError:
            print("Error: El costo del servicio debe ser un número válido.")  # Maneja errores de valor

class TallerMecanico:
    def __init__(self):
        self.notas = []  # Inicializa una lista vacía para almacenar notas

    def generar_folio(self):
        return len(self.notas) + 1  # Genera un nuevo folio basado en la cantidad de notas existentes

    def registrar_nota(self):
        try:
            while True:
                try:
                    folio = int(input("Ingrese el folio de la nota (solo números): "))  # Lee y convierte el folio a entero
                    break  # Sale del bucle si se ingresó un número válido
                except ValueError:
                    print("Error: El folio debe ser un número válido.")  # Maneja errores de valor

            fecha_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')  # Define un patrón de expresión regular para la fecha
            while True:
                fecha = input("Ingrese la fecha de la nota (DD-MM-YYYY): ")
                if fecha_pattern.match(fecha):  # Comprueba si la fecha coincide con el patrón
                    break  # Sale del bucle si la fecha tiene el formato correcto
                else:
                    print("Error: El formato de fecha es incorrecto. Debe ser DD-MM-YYYY.")  # Maneja errores de formato

            while True:
                cliente = input("Ingrese el nombre del cliente (solo letras): ")
                if cliente.replace(" ", "").isalpha():  # Comprueba si el cliente contiene solo letras
                    break  # Sale del bucle si el cliente es válido
                else:
                    print("Error: El nombre del cliente debe contener solo letras.")  # Maneja errores de formato

            nota = Nota(folio, fecha, cliente)  # Crea una instancia de la clase Nota
            while True:
                while True:
                    nombre_servicio = input("Ingrese el nombre del servicio (solo letras): ")
                    if nombre_servicio.replace(" ", "").isalpha():  # Comprueba si el nombre del servicio contiene solo letras
                        break  # Sale del bucle si el nombre del servicio es válido
                    else:
                        print("Error: El nombre del servicio debe contener solo letras.")  # Maneja errores de formato

                while True:
                    costo_servicio = input("Ingrese el costo del servicio (números con centavos): ")
                    try:
                        costo_servicio = float(costo_servicio)  # Convierte el costo del servicio en un número decimal
                        break  # Sale del bucle si el costo del servicio es un número válido
                    except ValueError:
                        print("Error: El costo del servicio debe ser un número válido.")  # Maneja errores de valor

                nota.agregar_servicio(nombre_servicio, costo_servicio)  # Agrega el servicio a la nota
                continuar = input("¿Desea agregar otro servicio? (S/N): ")
                if continuar.lower() != 's':
                    break  # Sale del bucle si no se desean agregar más servicios
            self.notas.append(nota)  # Agrega la nota a la lista de notas
            print("Nota registrada con éxito.")  # Imprime un mensaje de confirmación
        except ValueError:
            print("Error: El costo del servicio debe ser un número válido.")  # Maneja errores de valor
