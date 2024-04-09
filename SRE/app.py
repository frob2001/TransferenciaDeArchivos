from flask import Flask, render_template, Response
import csv
import io

app = Flask(__name__)

#Caso 1
# empleados = [
#     {"nombre": "Felipe Robalino", "telefono": "0987660915", "cargo": "Gerente", "horas_trabajo": 160},
#     {"nombre": "Ana Gómez", "telefono": "987654321", "cargo": "Asistente", "horas_trabajo": 150},
#     {"nombre": "Luis Morales", "telefono": "555666777", "cargo": "Analista", "horas_trabajo": 170},
# ]

#Caso 2
empleados = [
    {"nombre": "Felipe Robalino", "telefono": "0987660915", "cargo": "Gerente", "horas_trabajo": 165},
    {"nombre": "Ana Gómez", "telefono": "0987654321", "cargo": "Asistente", "horas_trabajo": 145},
    {"nombre": "María López", "telefono": "0922233344", "cargo": "Asistente", "horas_trabajo": 150},
    {"nombre": "Julia Martínez", "telefono": "0966677788", "cargo": "Analista", "horas_trabajo": 180},
    {"nombre": "Lucía Hernández", "telefono": "0999000111", "cargo": "Asistente", "horas_trabajo": 140},
    {"nombre": "Fernando Gómez", "telefono": "0977788899", "cargo": "Analista", "horas_trabajo": 180},
    {"nombre": "Miguel Ángel Torres", "telefono": "0911122233", "cargo": "Asistente", "horas_trabajo": 152}
]



@app.route('/')
def index():
    return render_template('index.html', empleados=empleados)

@app.route('/descargar-csv')
def descargar_csv():
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["Nombre", "Teléfono", "Cargo", "Horas de Trabajo Mensuales"])  # Encabezados de CSV
    for emp in empleados:
        cw.writerow([emp['nombre'], emp['telefono'], emp['cargo'], emp['horas_trabajo']])
    
    output = si.getvalue()
    si.close()
    
    # Codificar la salida a UTF-8 y agregar BOM
    output = '\ufeff' + output  # Agregar BOM para UTF-8
    output = output.encode('utf-8')

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=empleados.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
