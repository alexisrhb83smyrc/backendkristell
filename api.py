from flask import Flask, request, jsonify
from flasgger import Swagger
import mysql.connector

app = Flask(__name__)
swagger = Swagger(app)

# Configuración de la base de datos
conexion = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='almacen'
)

# entradas
@app.route('/entradas', methods=['POST'])
def crear_entrada():
    data = request.get_json()
    producto_id = data['producto_id']
    cantidad = data['cantidad']
    fecha = data['fecha']

    cursor = conexion.cursor()
    cursor.callproc('sp_insertar_entrada', (producto_id, cantidad, fecha))
    conexion.commit()

    return jsonify({'mensaje': 'Entrada creada correctamente'})


@app.route('/entradas/<int:entrada_id>', methods=['PUT'])
def actualizar_entrada(entrada_id):
    data = request.get_json()
    producto_id = data['producto_id']
    cantidad = data['cantidad']
    fecha = data['fecha']

    cursor = conexion.cursor()
    cursor.callproc('sp_actualizar_entrada', (entrada_id, producto_id, cantidad, fecha))
    conexion.commit()

    return jsonify({'mensaje': 'Entrada actualizada correctamente'})

@app.route('/entradas/<int:entrada_id>', methods=['DELETE'])
def eliminar_entrada(entrada_id):
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM entrada WHERE id = %s', (entrada_id,))
    conexion.commit()

    return jsonify({'mensaje': 'Entrada eliminada correctamente'}), 200

#salida
@app.route('/salidas', methods=['POST'])
def crear_salida():
    data = request.get_json()
    producto_id = data['producto_id']
    cantidad = data['cantidad']
    fecha = data['fecha']

    cursor = conexion.cursor()
    cursor.execute('INSERT INTO salida (producto_id, cantidad, fecha) VALUES (%s, %s, %s)', (producto_id, cantidad, fecha))
    conexion.commit()

    return jsonify({'mensaje': 'Salida creada correctamente'})


@app.route('/productos', methods=['GET'])
def obtener_productos():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    return jsonify(productos)

@app.route('/salidas/<int:salida_id>', methods=['DELETE'])
def eliminar_salida(salida_id):
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM salida WHERE id = %s', (salida_id,))
    conexion.commit()

    return jsonify({'mensaje': 'Salida eliminada correctamente'}), 200

#productos
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data['nombre']
    precio = data['precio']

    cursor = conexion.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio) VALUES (%s, %s)', (nombre, precio))
    conexion.commit()

    return jsonify({'mensaje': 'Producto creado correctamente'})


@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    nombre = data['nombre']
    precio = data['precio']

    cursor = conexion.cursor()
    cursor.execute('UPDATE productos SET nombre = %s, precio = %s WHERE id = %s', (nombre, precio, producto_id))
    conexion.commit()

    return jsonify({'mensaje': 'Producto actualizado correctamente'})


@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
    conexion.commit()

    return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200


if __name__ == '__main__':
    app.run(debug=True)
