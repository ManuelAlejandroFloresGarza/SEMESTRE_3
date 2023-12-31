import re
import csv
import os
from datetime import datetime

class Nota:
    def __init__(self, folio, fecha, cliente, rfc, correo):
        self.folio = folio
        self.fecha = fecha
        self.cliente = cliente
        self.rfc = rfc
        self.correo = correo
        self.servicios = []
        self.monto_total = 0.0
        self.cancelada = False

    def agregar_servicio(self, nombre_servicio, costo_servicio):
        try:
            costo_servicio = float(costo_servicio)
            self.servicios.append((nombre_servicio, costo_servicio))
            self.monto_total += costo_servicio
        except ValueError:
            print("Error: El costo del servicio debe ser un número válido.")

class TallerMecanico:
    def __init__(self):
        self.notas = []
        self.folio_actual = 1
        self.notas_canceladas = []

    def generar_folio(self):
        folio = self.folio_actual
        self.folio_actual += 1
        return folio

    def registrar_nota(self):
        try:
            while True:
                try:
                    folio = self.generar_folio()
                    break
                except ValueError:
                    print("Error generando el folio.")

            fecha_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')
            while True:
                fecha = input("Ingrese la fecha de la nota (DD-MM-YYYY): ")
                if fecha_pattern.match(fecha):
                    try:
                        fecha_ingresada = datetime.strptime(fecha, "%d-%m-%Y")
                        fecha_actual = datetime.now()
                        if fecha_ingresada > fecha_actual:
                            print("Error: La fecha no puede ser mayor a la fecha actual.")
                        else:
                            break
                    except ValueError:
                        print("Error: El formato de fecha es incorrecto. Debe ser DD-MM-YYYY.")
                else:
                    print("Error: El formato de fecha es incorrecto. Debe ser DD-MM-YYYY.")

            while True:
                cliente = input("Ingrese el nombre del cliente (solo letras): ")
                if cliente.replace(" ", "").isalpha():
                    break
                else:
                    print("Error: El nombre del cliente debe contener solo letras.")

            while True:
                rfc = input("Ingrese el RFC de la persona (13 dígitos, letras en mayúscula): ")
                if not re.match(r'^[A-Z]{4}\d{6}[A-Z0-9]{3}$', rfc):
                    print("Error: El RFC debe tener un formato válido de 13 dígitos (4 letras, 6 números y 3 letras/números).")
                else:
                    break
            while True:
                correo = input("Ingrese el correo electrónico del cliente: ")
                if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
                    break
                else:
                    print("Error: El correo electrónico debe tener un formato válido.")


            nota = Nota(folio, fecha, cliente, rfc, correo)
            while True:
                while True:
                    nombre_servicio = input("Ingrese el nombre del servicio (solo letras): ")
                    if nombre_servicio.replace(" ", "").isalpha():
                        break
                    else:
                        print("Error: El nombre del servicio debe contener solo letras.")

                while True:
                    costo_servicio = input("Ingrese el costo del servicio (números con centavos): ")
                    try:
                        costo_servicio = float(costo_servicio)
                        if costo_servicio <= 0:
                            print("Error: El costo del servicio debe ser un número válido.")
                        else:
                            break
                    except ValueError:
                        print("Error: El costo del servicio debe ser un número válido.")

                nota.agregar_servicio(nombre_servicio, costo_servicio)
                continuar = input("¿Desea agregar otro servicio? (S/N): ")
                if continuar.lower() != 's':
                    break
            self.notas.append(nota)
            print("Nota registrada con éxito.")
        except ValueError:
            print("Error: El costo del servicio debe ser un número válido.")
    def consultar_por_periodo(self):
        try:
            while True:
                print("\nMenú de Consultas y Reportes:")  
                print("1. Consulta por periodo")  
                print("2. Consulta por folio")  
                print("3. Consulta por cliente")
                print("4. Regresar al menú principal")
                opcion = input("Seleccione una opción (1/2/3/4): ")

                if opcion == "1":
                    while True:
                        fecha_inicial = input("Ingrese la fecha inicial (DD-MM-YYYY): ")
                        fecha_final = input("Ingrese la fecha final (DD-MM-YYYY): ")
                        try:
                            fecha_inicial = datetime.strptime(fecha_inicial, "%d-%m-%Y")
                            fecha_final = datetime.strptime(fecha_final, "%d-%m-%Y")
                            break
                        except ValueError:
                            print("Error: El formato de fecha es incorrecto. Debe ser DD-MM-YYYY.")

                    notas_periodo = [nota for nota in self.notas if fecha_inicial <= datetime.strptime(nota.fecha, "%d-%m-%Y") <= fecha_final]
                    if not notas_periodo:
                        print("No hay notas emitidas para el período indicado.")
                    else:
                        print("Notas en el período:")
                        for nota in notas_periodo:
                            print(f"Folio: {nota.folio}, Fecha: {nota.fecha}, Cliente: {nota.cliente}, RFC: {nota.rfc}, Correo: {nota.correo}, Monto: {nota.monto_total:.2f}")
                            print("Detalle de servicios:")
                            for servicio in nota.servicios:
                                print(f"  Servicio: {servicio[0]}, Costo: {servicio[1]:.2f}")
                elif opcion == "2":
                    folio_consulta = int(input("Ingrese el folio de la nota a consultar: "))
                    nota_consulta = next((nota for nota in self.notas if nota.folio == folio_consulta), None)
                    if nota_consulta is None:
                        print("La nota no se encuentra en el sistema.")
                    else:
                        print(f"Folio: {nota_consulta.folio}, Fecha: {nota_consulta.fecha}, Cliente: {nota_consulta.cliente}, RFC: {nota_consulta.rfc}, Correo: {nota_consulta.correo}, Monto: {nota_consulta.monto_total:.2f}")
                        print("Detalle de servicios:")
                        for servicio in nota_consulta.servicios:
                            print(f"  Servicio: {servicio[0]}, Costo: {servicio[1]:.2f}")
                elif opcion == "3":
                    self.consulta_por_cliente()
                elif opcion == "4":
                    break
                else:
                    print("Opción no válida.")
        except ValueError:
            print("Error: Ingrese un valor válido.")

    def consulta_por_cliente(self):
        
        notas_por_cliente = {}
        
        
        rfc_unicos = sorted(set(nota.rfc for nota in self.notas))
        
        
        folio_consecutivo = 1
        rfc_folio = {}
        for rfc in rfc_unicos:
            rfc_folio[rfc] = folio_consecutivo
            folio_consecutivo += 1
        
        
        for rfc, folio in rfc_folio.items():
            print("\nLista de RFCs:")
            print(f"Folio {folio}: {rfc}")
        
        salir = False  
        
        try:
            while not salir:  
                try:
                    rfc_elegido = None
                    folio_elegido = int(input("\nSeleccione el folio correspondiente al RFC a consultar: "))
                    if folio_elegido in rfc_folio.values():
                        for rfc, folio in rfc_folio.items():
                            if folio == folio_elegido:
                                rfc_elegido = rfc
                                break
                    else:
                        print("Error: Ingrese un número de folio válido.")
                except ValueError:
                    print("Error: Folio no válido. Intente nuevamente.")

                
                if rfc_elegido is not None:
                    notas_cliente = [nota for nota in self.notas if nota.rfc == rfc_elegido]
                    
                    if notas_cliente:
                        print(f"Notas para el RFC {rfc_elegido}:")
                        monto_promedio = sum(nota.monto_total for nota in notas_cliente) / len(notas_cliente)
                        for nota in notas_cliente:
                            print(f"Folio: {rfc_folio[rfc_elegido]}, Fecha: {nota.fecha}, Cliente: {nota.cliente}, RFC: {nota.rfc}, Correo: {nota.correo}, Monto: {nota.monto_total:.2f}")
                            print("Detalle de servicios:")
                            for servicio in nota.servicios:
                                print(f"  Servicio: {servicio[0]}, Costo: {servicio[1]:.2f}")
                        print(f"Monto promedio de las notas para el RFC {rfc_elegido}: {monto_promedio:.2f}")
                        
                        exportar_csv = input("¿Desea exportar esta información a un archivo CSV? (S/N): ")
                        if exportar_csv.lower() == 's':
                            
                            directorio_actual = os.path.dirname(os.path.abspath(__file__))
                            nombre_archivo = os.path.join(directorio_actual, f"{rfc_elegido}_{datetime.now().strftime('%Y%m%d')}.csv")
                            
                            with open(nombre_archivo, 'w', newline='') as archivo_csv:
                                escritor_csv = csv.writer(archivo_csv)
                                escritor_csv.writerow(['Folio', 'Fecha', 'Cliente', 'RFC', 'Correo', 'Monto Total'])
                                for nota in notas_cliente:
                                    escritor_csv.writerow([rfc_folio[rfc_elegido], nota.fecha, nota.cliente, nota.rfc, nota.correo, nota.monto_total])
                            print(f"Los datos han sido exportados a {nombre_archivo}.")
                            salir = True  
                        else:
                            break
                    else:
                        print(f"No hay notas registradas para el RFC {rfc_elegido}.")
                else:
                    print("Folio no válido. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un valor válido para el folio.")
    def cancelar_nota(self):
        try:
            folio_cancelar = int(input("Ingrese el folio de la nota a cancelar: "))
            nota_cancelar = next((nota for nota in self.notas if nota.folio == folio_cancelar), None)
            if nota_cancelar is None or nota_cancelar.cancelada:
                print("La nota no está en el sistema o ya está cancelada.")
            else:
                print(f"Folio: {nota_cancelar.folio}, Fecha: {nota_cancelar.fecha}, Cliente: {nota_cancelar.cliente}, RFC: {nota_cancelar.rfc}, Correo: {nota_cancelar.correo}, Monto: {nota_cancelar.monto_total:.2f}")
                confirmacion = input("¿Confirmar cancelación de la nota? (S/N): ")
                if confirmacion.lower() == 's':
                    nota_cancelar.cancelada = True
                    self.notas.remove(nota_cancelar)
                    self.notas_canceladas.append(nota_cancelar)
                    print("Nota cancelada y movida a notas canceladas.")
        except ValueError:
            print("Error: Ingrese un número de folio válido.")

    def recuperar_nota(self):
        try:
            if not self.notas_canceladas:
                print("No hay notas canceladas en el sistema.")
            else:
                print("Notas canceladas:")
                for nota in self.notas_canceladas:
                    print(f"Folio: {nota.folio}, Fecha: {nota.fecha}, Cliente: {nota.cliente}")

                folio_recuperar = int(input("Ingrese el folio de la nota a recuperar (o 0 para cancelar): "))
                if folio_recuperar != 0:
                    nota_recuperar = next((nota for nota in self.notas_canceladas if nota.folio == folio_recuperar), None)
                    if nota_recuperar is None:
                        print("La nota no está en el sistema.")
                    else:
                        print(f"Folio: {nota_recuperar.folio}, Fecha: {nota_recuperar.fecha}, Cliente: {nota_recuperar.cliente}")
                        confirmacion = input("¿Confirmar recuperación de la nota? (S/N): ")
                        if confirmacion.lower() == 's':
                            nota_recuperar.cancelada = False
                            self.notas_canceladas.remove(nota_recuperar)
                            self.notas.append(nota_recuperar)
                            print("Nota recuperada y movida de vuelta a notas activas.")
        except ValueError:
            print("Error: Ingrese un número de folio válido.")

    def ejecutar(self):
        while True:
            print("\nMenú Principal:")
            print("1. Registrar una nota")
            print("2. Consultas y Reportes") 
            print("3. Cancelar una nota")
            print("4. Recuperar una nota")
            print("5. Salir")

            opcion = input("Seleccione una opción (1/2/3/4/5): ")

            if opcion == "1":
                self.registrar_nota()
            elif opcion == "2":
                self.consultar_por_periodo()
            elif opcion == "3":
                self.cancelar_nota()
            elif opcion == "4":
                self.recuperar_nota()
            elif opcion == "5":
                confirmacion = input("¿Está seguro de que desea salir del programa? (S/N): ")
                if confirmacion.lower() == 's':
                    print("\nSaliendo del programa. ¡Hasta luego!")
                    break
                elif confirmacion.lower() == 'n':
                    continue
                else:
                    print("Opción no válida. Por favor, seleccione 'S' para salir o 'N' para continuar.")
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
                
    def guardar_estado(self):
        try:
            with open("estado_de_aplicacion.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                
                for nota in self.notas:
                    writer.writerow([nota.folio, nota.fecha, nota.cliente, nota.rfc, nota.correo, nota.monto_total, nota.cancelada])
                
                for nota in self.notas_canceladas:
                    writer.writerow([nota.folio, nota.fecha, nota.cliente, nota.rfc, nota.correo, nota.monto_total, True])
            print("Estado de la aplicación guardado con éxito.")
        except Exception as e:
            print(f"Error al guardar el estado de la aplicación: {e}")

    def cargar_estado(self):
        try:
            with open("estado_de_aplicacion.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    folio, fecha, cliente, rfc, correo, monto_total, cancelada = row
                    if cancelada == "True":
                        nota = Nota(int(folio), fecha, cliente, rfc, correo)
                        nota.monto_total = float(monto_total)
                        nota.cancelada = True
                        self.notas_canceladas.append(nota)
                    else:
                        nota = Nota(int(folio), fecha, cliente, rfc, correo)
                        nota.monto_total = float(monto_total)
                        self.notas.append(nota)
            print("Estado de la aplicación cargado con éxito.")
        except FileNotFoundError:
            print("No se encontró un archivo de estado anterior. Se parte de un estado inicial vacío.")
        except Exception as e:
            print(f"Error al cargar el estado de la aplicación: {e}")

if __name__ == "__main__":
    taller = TallerMecanico()
    taller.cargar_estado()  
    taller.ejecutar()
    taller.guardar_estado()  
