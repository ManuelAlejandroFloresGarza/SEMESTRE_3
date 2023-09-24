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
