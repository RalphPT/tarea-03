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
    data = conexion.cursor()
    data.execute("SELECT * FROM areas")
    areas = data.fetchall()
    data.close()
    return jsonify(areas)

# Endpoint para crear un área
@app.route('/area', methods=['POST'])
def create_area():
    new_area = request.get_json()
    data = conexion.cursor()
    data.execute("INSERT INTO areas (id, nombre, piso) VALUES (%s, %s, %s) RETURNING *",
                   (new_area["id"], new_area["nombre"], new_area["piso"]))
    created_area = data.fetchone()
    conexion.commit()
    data.close()
    return jsonify(created_area), 201

# Endpoint para obtener un área por su ID
@app.route('/area/<int:area_id>', methods=['GET'])
def get_area(area_id):
    data = conexion.cursor()
    data.execute("SELECT * FROM areas WHERE id = %s", (area_id,))
    area = data.fetchone()
    data.close()

    if area:
        return jsonify(area)
    else:
        return jsonify({'error': 'No se encontró el área'}), 404

# Endpoint para crear un empleado
@app.route('/empleado', methods=['POST'])
def create_empleado():
    new_empleado = request.get_json()
    data = conexion.cursor()
    data.execute("INSERT INTO empleados (id, nombre, apellido, correo, piso, area_id) VALUES (%s, %s, %s, %s,%s, %s) RETURNING *",
                   (new_empleado["id"], new_empleado["nombre"], new_empleado["apellido"], new_empleado["correo"], new_empleado["piso"],new_empleado["area_id"]))
    created_empleado = data.fetchone()
    conexion.commit()
    data.close()
    return jsonify(created_empleado), 201

# Endpoint para obtener empleados de según condición de query
@app.route('/empleados', methods=['GET'])
def get_empleados():
    email = request.args.get('email')
    nombre = request.args.get('nombre')

    data = conexion.cursor()
    if email:
        data.execute("SELECT * FROM empleados WHERE correo = %s", (email,))
    elif nombre:
        data.execute("SELECT * FROM empleados WHERE nombre = %s", (nombre,))
    else:
        return jsonify({'error': 'No se encontró el parámetro'}), 404

    empleados = data.fetchall()
    data.close()
    return jsonify(empleados)

if __name__ == '__main__':
    app.run(debug = True)
