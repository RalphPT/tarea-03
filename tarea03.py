from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL
conexion = psycopg2.connect(
    host="localhost",
    port="5432",
    database="tarea03",
    user="postgres",
    password="root"
)

# Endpoint para obtener todas las áreas
@app.route('/areas', methods=['GET'])
def get_areas():
    """
    Devuelve todas las áreas.
    """
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM areas")
    areas = cursor.fetchall()
    cursor.close()
    return jsonify(areas)

# Endpoint para crear un área
@app.route('/area', methods=['POST'])
def create_area():
    new_area = request.get_json()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO areas (id, nombre, piso) VALUES (%s, %s, %s) RETURNING *",
                   (new_area["id"], new_area["nombre"], new_area["piso"]))
    created_area = cursor.fetchone()
    conexion.commit()
    cursor.close()
    return jsonify(created_area), 201

# Endpoint para obtener un área por su ID
@app.route('/area/<int:area_id>', methods=['GET'])
def get_area(area_id):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM areas WHERE id = %s", (area_id,))
    area = cursor.fetchone()
    cursor.close()

    if area:
        return jsonify(area)
    else:
        return jsonify({'error': 'No se encontró el área'}), 404

# Endpoint para crear un empleado
@app.route('/empleado', methods=['POST'])
def create_empleado():
    new_empleado = request.get_json()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO empleados (id, nombre, apellido, correo, piso, area_id) VALUES (%s, %s, %s, %s,%s, %s) RETURNING *",
                   (new_empleado["id"], new_empleado["nombre"], new_empleado["apellido"], new_empleado["correo"], new_empleado["piso"],new_empleado["area_id"]))
    created_empleado = cursor.fetchone()
    conexion.commit()
    cursor.close()
    return jsonify(created_empleado), 201

# Endpoint para obtener empleados de según condición de query
@app.route('/empleados', methods=['GET'])
def get_empleados():
    email = request.args.get('email')
    nombre = request.args.get('nombre')

    cursor = conexion.cursor()
    if email:
        cursor.execute("SELECT * FROM empleados WHERE correo = %s", (email,))
    elif nombre:
        cursor.execute("SELECT * FROM empleados WHERE nombre = %s", (nombre,))
    else:
        return jsonify({'error': 'No se encontró el parámetro'}), 404

    empleados = cursor.fetchall()
    cursor.close()
    return jsonify(empleados)

if __name__ == '__main__':
    app.run(debug = True)