# ejercicio3.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# -------------------------------------------------------
# Configuración de conexión a MySQL
# Cambia 'password' por tu contraseña de MySQL
# -------------------------------------------------------
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': '1234',
    'database': 'estudiantes_db'
}

def get_connection():
    """Crea y devuelve una conexión a la base de datos"""
    return mysql.connector.connect(**DB_CONFIG)


# -------------------------------------------------------
# POST /estudiantes — Registrar un nuevo estudiante
# -------------------------------------------------------
@app.route('/estudiantes', methods=['POST'])
def agregar_estudiante():
    datos = request.get_json()

    # Validar que se enviaron datos
    if not datos:
        return jsonify({'error': 'No se recibieron datos'}), 400

    nombre   = datos.get('nombre')
    carrera  = datos.get('carrera')
    semestre = datos.get('semestre')

    # Validar que todos los campos estén presentes
    if not nombre:
        return jsonify({'error': 'Falta el campo nombre'}), 400
    if not carrera:
        return jsonify({'error': 'Falta el campo carrera'}), 400
    if semestre is None:
        return jsonify({'error': 'Falta el campo semestre'}), 400

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # Insertar el nuevo estudiante en la base de datos
        sql = "INSERT INTO estudiantes (nombre, carrera, semestre) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, carrera, semestre))
        conn.commit()

        nuevo_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            'mensaje':  'Estudiante registrado correctamente',
            'id':       nuevo_id,
            'nombre':   nombre,
            'carrera':  carrera,
            'semestre': semestre
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -------------------------------------------------------
# GET /estudiantes — Consultar todos los estudiantes
# -------------------------------------------------------
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    try:
        conn   = get_connection()
        # dictionary=True hace que cada fila regrese como diccionario
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM estudiantes")
        estudiantes = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'total':       len(estudiantes),
            'estudiantes': estudiantes
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)