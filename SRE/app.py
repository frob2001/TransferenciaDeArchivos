from flask import Flask, render_template, Response
import csv
import io
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)

# Datos iniciales
empleados = [
    {"nombre": "Felipe Robalino", "telefono": "0987660915", "cargo": "Gerente", "horas_trabajo": 165},
    {"nombre": "Ana Gómez", "telefono": "0987654321", "cargo": "Asistente", "horas_trabajo": 145},
    {"nombre": "María López", "telefono": "0922233344", "cargo": "Asistente", "horas_trabajo": 150},
    {"nombre": "Julia Martínez", "telefono": "0966677788", "cargo": "Analista", "horas_trabajo": 180},
    {"nombre": "Lucía Hernández", "telefono": "0999000111", "cargo": "Asistente", "horas_trabajo": 140},
    {"nombre": "Fernando Gómez", "telefono": "0977788899", "cargo": "Analista", "horas_trabajo": 180},
    {"nombre": "Miguel Ángel Torres", "telefono": "0911122233", "cargo": "Asistente", "horas_trabajo": 152}
]

# Conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='empleados',
        user='postgres',
        password='Felixpro2510')
    return conn

# Crear tabla empleados si no existe
def create_table():
    conn = get_db_connection()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            nombre VARCHAR(255),
            telefono VARCHAR(20),
            cargo VARCHAR(50),
            horas_trabajo INT
        );
    ''')
    conn.close()

# Insertar datos iniciales en la tabla empleados
def insert_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    for emp in empleados:
        cursor.execute('''
            INSERT INTO empleados (nombre, telefono, cargo, horas_trabajo) 
            VALUES (%s, %s, %s, %s);
        ''', (emp['nombre'], emp['telefono'], emp['cargo'], emp['horas_trabajo']))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, telefono, cargo, horas_trabajo FROM empleados;')
    empleados_db = cursor.fetchall()
    conn.close()
    empleados = [
        {"nombre": emp[0], "telefono": emp[1], "cargo": emp[2], "horas_trabajo": emp[3]}
        for emp in empleados_db
    ]
    return render_template('index.html', empleados=empleados)

@app.route('/descargar-csv')
def descargar_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, telefono, cargo, horas_trabajo FROM empleados;')
    empleados_db = cursor.fetchall()
    conn.close()
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["Nombre", "Teléfono", "Cargo", "Horas de Trabajo Mensuales"])
    for emp in empleados_db:
        cw.writerow(emp)
    
    output = si.getvalue()
    si.close()
    
    # Codificar la salida a UTF-8 y agregar BOM
    output = '\ufeff' + output
    output = output.encode('utf-8')

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=empleados.csv"}
    )

if __name__ == '__main__':
    create_table() # Crear tabla si no existe
    #insert_initial_data() # Descomentar esta línea si necesitas insertar los datos iniciales
    app.run(debug=True)
