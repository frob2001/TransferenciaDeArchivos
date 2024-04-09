from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import csv
import io
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])

# Configurar la conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='nomina',
        user='postgres',
        password='Felixpro2510')
    return conn

def inicializar_tabla():
    conn = get_db_connection()
    cur = conn.cursor()
    # Borrar la tabla si ya existe y luego crearla nuevamente
    cur.execute('DROP TABLE IF EXISTS empleados;')
    cur.execute('''
        CREATE TABLE empleados (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255),
            telefono VARCHAR(20),
            cargo VARCHAR(100),
            horas_trabajo INT,
            salario NUMERIC,
            fecha_carga DATE,
            hora_carga TIMESTAMP WITHOUT TIME ZONE
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()


@app.route('/empleados', methods=['GET'])
def mostrar_empleados():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nombre, telefono, cargo, horas_trabajo, salario, fecha_carga, hora_carga FROM empleados;')
    empleados_rows = cur.fetchall()
    # Convertir los resultados a una lista de diccionarios
    empleados = [
        {
            'id': row[0],
            'nombre': row[1],
            'telefono': row[2],
            'cargo': row[3],
            'horas_trabajo': row[4],
            'salario': row[5],
            'fecha_carga': row[6].strftime('%Y-%m-%d') if row[6] else None,
            'hora_carga': row[7].strftime('%H:%M:%S') if row[7] else None
        
        }
        for row in empleados_rows
    ]
    cur.close()
    conn.close()
    return jsonify(empleados)


@app.route('/subir', methods=['POST'])
def subir_y_calcular_salario():
    # Verificar si el archivo está presente en la solicitud
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    # Verificar si se seleccionó un archivo
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # Preparar el archivo para la lectura
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input)  # Omitir la cabecera del CSV

        # Preparar la conexión a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Procesar cada fila del archivo CSV
        for row in csv_input:
            nombre, telefono, cargo, horas_trabajo = row
            # Asumir que los salarios y horas requeridas por cargo son conocidos
            salarios = {'Gerente': 50, 'Asistente': 30, 'Analista': 40}
            horas_requeridas = {'Gerente': 160, 'Asistente': 150, 'Analista': 170}
            salario = (int(horas_trabajo) / horas_requeridas[cargo]) * salarios[cargo] * horas_requeridas[cargo]

            # Capturar la fecha y la hora de carga
            fecha_carga = datetime.now().date()
            hora_carga = datetime.now()

            # Insertar el registro en la base de datos
            cur.execute('INSERT INTO empleados (nombre, telefono, cargo, horas_trabajo, salario, fecha_carga, hora_carga) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (nombre, telefono, cargo, horas_trabajo, salario, fecha_carga, hora_carga))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        cur.close()
        conn.close()
        return 'Archivo procesado exitosamente', 200


if __name__ == '__main__':
    inicializar_tabla()  # Inicializa la tabla antes de procesar el archivo
    app.run(debug=True, port=5500)