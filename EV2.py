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
