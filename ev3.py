# Importamos las librerias
import sqlite3
import random
import string
import re
import datetime
from datetime import datetime
import csv
import openpyxl
import os

# Conexión a la base de datos SQLite

# Función para crear las tablas en sqlite al iniciar el programa
def crear_tablas():
    try:
        with sqlite3.connect("taller.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clientes (
                idcliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombrecliente TEXT NOT NULL,
                rfccliente TEXT NOT NULL,
                correocliente TEXT NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Servicios (
                idservicio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombreservicio TEXT NOT NULL,
                costoservicio REAL CHECK (costoservicio > 0.00) NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Notas (
                folionota INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                idcliente INTEGER NOT NULL,
                idservicio INTEGER NOT NULL,
                status INTEGER DEFAULT 1,
                FOREIGN KEY (idcliente) REFERENCES Clientes(idcliente),
                FOREIGN KEY (idservicio) REFERENCES Servicios(idservicio)
            )
            """)
    except sqlite3.Error as e:
        print(f"Error al crear tablas en la base de datos: {e}")

# Creamos los submenus
def mostrar_menu_notas():
    print("\nMenú Notas:")
    print("1. Registrar una nota")
    print("2. Cancelar una nota")
    print("3. Recuperar una nota")
    print("4. Consultas y reportes de notas")
    print("5. Volver al menú principal")

def mostrar_menu_clientes():
    print("\nMenú Clientes:")
    print("1. Agregar un cliente")
    print("2. Consultas y reportes de clientes")
    print("3. Volver al menú principal")

def mostrar_menu_servicios():
    print("\nMenú Servicios")
    print("1. Agregar un servicio")
    print("2. Consultas y reportes de servicios")
    print("3. Volver al menú anterior")

# Creamos la opción Notas
def Notas():
    while True:
        mostrar_menu_notas()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_nota()
        elif opcion == "2":
            cancelar_nota()
        elif opcion == "3":
            recuperar_nota()
        elif opcion == "4":
            consultasreportes_notas()
        elif opcion == "5":
            print("Volviendo al menú principal.")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            
def registrar_nota():
    while True:
        while True:
            fecha_ingresada = input("Ingresa una fecha en el formato DD/MM/YYYY: ")
            if validar_fecha(fecha_ingresada):
                break
            else:
                print("Fecha no válida o es posterior a la fecha actual. Intenta de nuevo.")

        with sqlite3.connect("taller.db") as conn:
            cursor = conn.cursor()
            mostrar_registros("Clientes")
            mostrar_registros("Servicios")

            while True:
                try:
                    cliente = input("\nIngrese la clave del cliente: ")
                    cliente = int(cliente)
                    cursor.execute("SELECT idcliente, nombrecliente FROM Clientes WHERE idcliente = ?", (cliente,))
                    cliente_existente = cursor.fetchone()
                    if cliente_existente:
                        print(f"Cliente seleccionado: {cliente_existente[1]}")
                        break
                    else:
                        print("Clave de cliente no válida. Debe ser mayor que 0 y existir en la tabla Clientes. Intente de nuevo.")
                except ValueError:
                    print("Error: Ingrese una clave de cliente válida.")

            while True:
                try:
                    servicio = int(input("Ingrese la clave del servicio: "))
                    cursor.execute("SELECT idservicio, nombreservicio FROM Servicios WHERE idservicio = ?", (servicio,))
                    servicio_existente = cursor.fetchone()
                    if servicio_existente:
                        print(f"Servicio seleccionado: {servicio_existente[1]}")
                        break
                    else:
                        print("Clave de servicio no válida. Debe ser mayor que 0 y existir en la tabla Servicios. Intente de nuevo.")
                except ValueError:
                    print("Error: Ingrese una clave de servicio válida.")

            # Realizar la inserción de la nota en la base de datos
            try:
                cursor.execute("INSERT INTO Notas (fecha, idcliente, idservicio) VALUES (?, ?, ?)", (fecha_ingresada, cliente, servicio))
                conn.commit()
                cursor.execute("SELECT folionota FROM Notas WHERE folionota = (SELECT MAX(folionota) FROM Notas)")
                folio = cursor.fetchone()
                print(f"Nota agregada exitosamente con folio {folio[0]}")
                break
            except Exception as e:
                print(f"Error al agregar la nota: {e}")

def cancelar_nota():
    while True:
        try:
            folio = int(input("Ingrese el folio de la nota que desea cancelar: "))
        except ValueError:
            print("Error: El folio debe ser un número válido.")
            continue

        with sqlite3.connect("taller.db") as conn:
            cursor = conn.cursor()

            # Verificar si la nota con el folio proporcionado existe y no está cancelada
            cursor.execute("SELECT * FROM Notas WHERE folionota = ? AND status = 1", (folio,))
            nota = cursor.fetchone()

            if nota:
                # Mostrar los detalles de la nota antes de la cancelación
                print("Detalle de la nota a cancelar:")
                print(f"Folio de la nota: {nota[0]}")
                print(f"Fecha: {nota[1]}")
                cursor.execute("SELECT nombrecliente FROM Clientes WHERE idcliente = ?", (nota[2],))
                nombre_cliente = cursor.fetchone()[0]
                cursor.execute("SELECT nombreservicio FROM Servicios WHERE idservicio = ?", (nota[3],))
                nombre_servicio = cursor.fetchone()[0]
                print(f"Cliente: {nombre_cliente}")
                print(f"Servicio: {nombre_servicio}")

                confirmacion = input("¿Está seguro de que desea cancelar esta nota? (S/N): ").strip().upper()

                if confirmacion == 'S':
                    # Cambiar el estado de la nota a cancelada
                    cursor.execute("UPDATE Notas SET status = 0 WHERE folionota = ?", (folio,))
                    conn.commit()
                    print("La nota ha sido cancelada exitosamente.")
                else:
                    print("La cancelación de la nota ha sido cancelada a solicitud del usuario.")
            else:
                print("La nota no existe o ya está cancelada en el sistema.")

        break


def recuperar_nota():
    with sqlite3.connect("taller.db") as conn:
        cursor = conn.cursor()

        # Obtener una lista de notas canceladas (sin su detalle)
        cursor.execute("SELECT folionota FROM Notas WHERE status = 0")
        notas_canceladas = cursor.fetchall()

        if not notas_canceladas:
            print("No hay notas canceladas para recuperar.")
            return

        print("Listado de notas canceladas:")
        for folio in notas_canceladas:
            print(f"Folio de la nota: {folio[0]}")

        while True:
            try:
                folio_recuperar = int(input("Ingrese el folio de la nota que desea recuperar o 0 para cancelar: "))
            except ValueError:
                print("Error: El folio debe ser un número válido.")
                continue

            if folio_recuperar == 0:
                print("Operación cancelada. No se recuperó ninguna nota.")
                return
            elif (folio_recuperar,) in notas_canceladas:
                cursor.execute("SELECT * FROM Notas WHERE folionota = ?", (folio_recuperar,))
                nota = cursor.fetchone()

                # Mostrar el detalle de la nota cancelada antes de la recuperación
                print("Detalle de la nota a recuperar:")
                print(f"Folio de la nota: {nota[0]}")
                print(f"Fecha: {nota[1]}")
                cursor.execute("SELECT nombrecliente FROM Clientes WHERE idcliente = ?", (nota[2],))
                nombre_cliente = cursor.fetchone()[0]
                cursor.execute("SELECT nombreservicio FROM Servicios WHERE idservicio = ?", (nota[3],))
                nombre_servicio = cursor.fetchone()[0]
                print(f"Cliente: {nombre_cliente}")
                print(f"Servicio: {nombre_servicio}")

                confirmacion = input("¿Está seguro de que desea recuperar esta nota? (S/N): ").strip().upper()

                if confirmacion == 'S':
                    # Cambiar el estado de la nota a activa (no cancelada)
                    cursor.execute("UPDATE Notas SET status = 1 WHERE folionota = ?", (folio_recuperar,))
                    conn.commit()
                    print("La nota ha sido recuperada exitosamente.")
                else:
                    print("La recuperación de la nota ha sido cancelada a solicitud del usuario.")
                break
            else:
                print("El folio ingresado no corresponde a una nota cancelada en el sistema.")


def consultasreportes_notas():
    while True:
        print("\nConsultas y Reportes de Notas:")
        print("1. Consulta por período")
        print("2. Consulta por folio")
        print("3. Volver atrás")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":  # Consulta por período
            consulta_por_periodo()
        elif opcion == "2":  # Consulta por folio
            consulta_por_folio()
        elif opcion == "3":  # Volver atrás
            print("Volviendo al menú principal.")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

def consulta_por_periodo():
    while True:
        fecha_inicial = input("Ingrese la fecha inicial (DD-MM-YYYY) o presione Enter para asumir 01/01/2000: ")
        fecha_final = input("Ingrese la fecha final (DD-MM-YYYY) o presione Enter para asumir la fecha actual: ")

        if fecha_inicial == "":
            fecha_inicial = "01-01-2000"
        if fecha_final == "":
            fecha_final = datetime.datetime.now().strftime("%d-%m-%Y")

        try:
            fecha_inicial = datetime.datetime.strptime(fecha_inicial, '%d-%m-%Y')
            fecha_final = datetime.datetime.strptime(fecha_final, '%d-%m-%Y')
        except ValueError:
            print("Error: Las fechas no tienen un formato válido (DD-MM-YYYY).")
            continue

        if fecha_final < fecha_inicial:
            print("Error: La fecha final debe ser igual o posterior a la fecha inicial.")
            continue

        with sqlite3.connect("taller.db") as conn:
            cursor = conn.cursor()

            # Consulta de notas por período
            cursor.execute("""
                SELECT n.folionota, n.fecha, c.nombrecliente
                FROM Notas n
                JOIN Clientes c ON n.idcliente = c.idcliente
                WHERE date(n.fecha) BETWEEN ? AND ?
            """, (fecha_inicial, fecha_final))
            notas = cursor.fetchall()

            if notas:
                # Calcular el monto promedio de las notas del período
                cursor.execute("""
                    SELECT AVG(s.costoservicio)
                    FROM Servicios s
                    JOIN Notas n ON s.idservicio = n.idservicio
                    WHERE date(n.fecha) BETWEEN ? AND ?
                """, (fecha_inicial, fecha_final))
                promedio_monto = cursor.fetchone()[0]

                print("Notas dentro del período seleccionado:")
                print(f"{'Folio':<10} {'Fecha':<12} {'Nombre del Cliente':<30}")
                for nota in notas:
                    print(f"{nota[0]:<10} {nota[1]:<12} {nota[2]:<30}")

                print(f"Monto promedio del período: {promedio_monto:.2f}")

                while True:
                    opcion_exportar = input("¿Desea exportar el reporte a CSV, Excel o regresar al menú de reportes? (CSV/Excel/Regresar): ").strip().lower()
                    if opcion_exportar == "csv":
                        exportar_reporte_csv(notas, fecha_inicial, fecha_final, promedio_monto)
                        break
                    elif opcion_exportar == "excel":
                        exportar_reporte_excel(notas, fecha_inicial, fecha_final, promedio_monto)
                        break
                    elif opcion_exportar == "regresar":
                        break
                    else:
                        print("Opción no válida. Por favor, seleccione una opción válida.")
            else:
                print("No hay notas emitidas para el período especificado.")
            break
