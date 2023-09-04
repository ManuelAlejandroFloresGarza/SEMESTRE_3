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

    def consultar_por_periodo(self):
        try:
            while True:
                print("\nConsultar por período:")
                print("1. Por folio")
                print("2. Por fecha de creación")
                print("3. Regresar al menú principal")
                opcion = input("Seleccione una opción (1/2/3): ")

                if opcion == "1":
                    folio_consulta = int(input("Ingrese el folio de la nota a consultar: "))  # Lee el folio a consultar
                    nota_consulta = next((nota for nota in self.notas if nota.folio == folio_consulta), None)  # Busca la nota por folio
                    if nota_consulta is None:
                        print("La nota no se encuentra en el sistema.")  # Imprime un mensaje si la nota no se encuentra
                    else:
                        print(f"Folio: {nota_consulta.folio}, Fecha: {nota_consulta.fecha}, Cliente: {nota_consulta.cliente}, Monto: {nota_consulta.monto_total:.2f}")  # Imprime información de la nota
                        print("Detalle de servicios:")
                        for servicio in nota_consulta.servicios:
                            print(f"  Servicio: {servicio[0]}, Costo: {servicio[1]:.2f}")  # Imprime detalles de los servicios
                elif opcion == "2":
                    fecha_inicial = input("Ingrese la fecha inicial (DD-MM-YYYY): ")  # Lee la fecha inicial
                    fecha_final = input("Ingrese la fecha final (DD-MM-YYYY): ")  # Lee la fecha final

                    notas_periodo = [nota for nota in self.notas if fecha_inicial <= nota.fecha <= fecha_final]  # Filtra las notas por fecha
                    if not notas_periodo:
                        print("No hay notas emitidas para el período indicado.")  # Imprime un mensaje si no hay notas en el período
                    else:
                        print("Notas en el período:")
                    for nota in notas_periodo:
                        print(f"Folio: {nota.folio}, Fecha: {nota.fecha}, Cliente: {nota.cliente}, Monto: {nota.monto_total:.2f}")  # Imprime información de las notas en el período
                        print("Detalle de servicios:")
                    for servicio in nota.servicios:
                        print(f"  Servicio: {servicio[0]}, Costo: {servicio[1]:.2f}")  # Imprime detalles de los servicios
                elif opcion == "3":
                    break  # Regresar al menú principal
                else:
                    print("Opción no válida.")  # Imprime un mensaje si la opción no es válida
        except ValueError:
            print("Error: Ingrese un valor válido.")  # Maneja errores de valor

    def cancelar_nota(self):
        try:
            folio_cancelar = int(input("Ingrese el folio de la nota a cancelar: "))  # Lee el folio de la nota a cancelar
            nota_cancelar = next((nota for nota in self.notas if nota.folio == folio_cancelar), None)  # Busca la nota por folio
            if nota_cancelar is None or nota_cancelar.cancelada:
                print("La nota no está en el sistema o ya está cancelada.")  # Imprime un mensaje si la nota no se encuentra o ya está cancelada
            else:
                print(f"Folio: {nota_cancelar.folio}, Fecha: {nota_cancelar.fecha}, Cliente: {nota_cancelar.cliente}, Monto: {nota_cancelar.monto_total:.2f}")  # Imprime información de la nota a cancelar
                confirmacion = input("¿Confirmar cancelación de la nota? (S/N): ")  # Pide confirmación para cancelar la nota
                if confirmacion.lower() == 's':
                    nota_cancelar.cancelada = True  # Cambia el estado de la nota a cancelada
                    print("Nota cancelada.")  # Imprime un mensaje de confirmación
        except ValueError:
            print("Error: Ingrese un número de folio válido.")  # Maneja errores de valor

    def recuperar_nota(self):
        try:
            notas_canceladas = [nota for nota in self.notas if nota.cancelada]  # Filtra las notas que están canceladas
            if not notas_canceladas:
                print("No hay notas canceladas en el sistema.")  # Imprime un mensaje si no hay notas canceladas
            else:
                print("Notas canceladas:")
                for nota in notas_canceladas:
                    print(f"Folio: {nota.folio}, Fecha: {nota.fecha}, Cliente: {nota.cliente}")  # Imprime información de las notas canceladas
                folio_recuperar = int(input("Ingrese el folio de la nota a recuperar (o 0 para cancelar): "))  # Lee el folio de la nota a recuperar
                if folio_recuperar != 0:
                    nota_recuperar = next((nota for nota in notas_canceladas if nota.folio == folio_recuperar), None)  # Busca la nota a recuperar por folio
                    if nota_recuperar is None:
                        print("La nota no está en el sistema.")  # Imprime un mensaje si la nota no se encuentra
                    else:
                        print(f"Folio: {nota_recuperar.folio}, Fecha: {nota_recuperar.fecha}, Cliente: {nota_recuperar.cliente}")  # Imprime información de la nota a recuperar
                        confirmacion = input("¿Confirmar recuperación de la nota? (S/N): ")  # Pide confirmación para recuperar la nota
                        if confirmacion.lower() == 's':
                            nota_recuperar.cancelada = False  # Cambia el estado de la nota a no cancelada (recuperada)
                            print("Nota recuperada.")  # Imprime un mensaje de confirmación
        except ValueError:
            print("Error: Ingrese un número de folio válido.")  # Maneja errores de valor

    def ejecutar(self):
     while True:
        # Imprime el menú principal del programa
        print("\nMenú Principal:")
        print("1. Registrar una nota")
        print("2. Consultar por período")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota")
        print("5. Salir")

        # Solicita al usuario que seleccione una opción
        opcion = input("Seleccione una opción (1/2/3/4/5): ")

        if opcion == "1":
            self.registrar_nota()  # Llama al método para registrar una nota si la opción es "1"
        elif opcion == "2":
            self.consultar_por_periodo()  # Llama al método para consultar por período si la opción es "2"
        elif opcion == "3":
            self.cancelar_nota()  # Llama al método para cancelar una nota si la opción es "3"
        elif opcion == "4":
            self.recuperar_nota()  # Llama al método para recuperar una nota si la opción es "4"
        elif opcion == "5":
            confirmacion = input("¿Está seguro de que desea salir del programa? (S/N): ")
            if confirmacion.lower() == 's':
                # Sale del bucle while (finaliza el programa) si se confirma la salida
                print("Saliendo del programa. ¡Hasta luego!")
                break
            elif confirmacion.lower() == 'n':
                continue  # Continúa en el bucle while si se elige no salir
            else:
                # Maneja una opción no válida si no se ingresa 'S' o 'N'
                print("Opción no válida. Por favor, seleccione 'S' para salir o 'N' para continuar.")
        else:
            # Maneja una opción no válida si se ingresa un número diferente a 1, 2, 3, 4 o 5
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    taller = TallerMecanico()
    taller.ejecutar()  # Inicia la ejecución del programa principal llamando al método "ejecutar" de la instancia
