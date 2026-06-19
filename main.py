import sqlite3
import openpyxl

conn = sqlite3.connect("empleados.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        puesto TEXT NOT NULL,
        salario REAL NOT NULL
    )
""")
conn.commit()

def mostrar_menu():
    print("\n=== Sistema de Empleados ===")
    print("1. Agregar empleado")
    print("2. Ver todos los empleados")
    print("3. Buscar empleado")
    print("4. Editar salario")
    print("5. Eliminar empleado")
    print("6. Exportar a Excel")
    print("7. Salir")
    return input("Elige una opcion: ")

while True:
    opcion = mostrar_menu()

    if opcion == "1":
        nombre = input("Nombre: ")
        puesto = input("Puesto: ")
        salario = float(input("Salario: "))
        cursor.execute("INSERT INTO empleados (nombre, puesto, salario) VALUES (?, ?, ?)",
                       (nombre, puesto, salario))
        conn.commit()
        print(f"Empleado {nombre} guardado.")

    elif opcion == "2":
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
        if not empleados:
            print("No hay empleados registrados.")
        else:
            print("\n--- Lista de empleados ---")
            for emp in empleados:
                print(f"{emp[0]}. {emp[1]} | {emp[2]} | ${emp[3]}")

    elif opcion == "3":
        nombre = input("Nombre a buscar: ")
        cursor.execute("SELECT * FROM empleados WHERE nombre LIKE ?", (f"%{nombre}%",))
        resultados = cursor.fetchall()
        if not resultados:
            print("No se encontro ningun empleado.")
        else:
            for emp in resultados:
                print(f"{emp[0]}. {emp[1]} | {emp[2]} | ${emp[3]}")

    elif opcion == "4":
        nombre = input("Nombre del empleado a editar: ")
        nuevo_salario = float(input("Nuevo salario: "))
        cursor.execute("UPDATE empleados SET salario = ? WHERE nombre LIKE ?",
                       (nuevo_salario, f"%{nombre}%"))
        conn.commit()
        print("Salario actualizado.")

    elif opcion == "5":
        nombre = input("Nombre del empleado a eliminar: ")
        cursor.execute("DELETE FROM empleados WHERE nombre LIKE ?", (f"%{nombre}%",))
        conn.commit()
        print("Empleado eliminado.")

    elif opcion == "6":
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Empleados"
        ws.append(["ID", "Nombre", "Puesto", "Salario"])
        for emp in empleados:
            ws.append(list(emp))
        wb.save("empleados.xlsx")
        print("Archivo empleados.xlsx generado.")

    elif opcion == "7":
        print("Hasta luego!")
        conn.close()
        break

    else:
        print("Opcion no valida.")