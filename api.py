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
@app.route('/entradas', methods=['GET'])
def obtener_entradas():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute('SELECT * FROM entrada')
    entradas = cursor.fetchall()
    return jsonify(entradas)

@app.route('/entradas', methods=['POST'])
def crear_entrada():
    data = request.get_json()
    producto_id = data['producto_id']
    cantidad = data['cantidad']
    fecha = data['fecha']

    cursor = conexion.cursor()
    # Insertar la entrada en la tabla de entradas
    cursor.callproc('sp_insertar_entrada', (producto_id, cantidad, fecha))
    conexion.commit()
    cursor.execute('SELECT cantidad FROM inventario WHERE producto_id = %s', (producto_id,))
    inventario_cantidad = cursor.fetchone()
    if inventario_cantidad:
        nueva_cantidad = inventario_cantidad[0] + cantidad
        cursor.execute('UPDATE inventario SET cantidad = %s WHERE producto_id = %s', (nueva_cantidad, producto_id))
    else:
        cursor.execute('INSERT INTO inventario (producto_id, cantidad) VALUES (%s, %s)', (producto_id, cantidad))
    
    conexion.commit()

    return jsonify({'mensaje': 'Entrada creada correctamente'}), 200

@app.route('/entradas/<int:entrada_id>', methods=['PUT'])
def actualizar_entrada(entrada_id):
    data = request.get_json()
    producto_id = data['producto_id']
    nueva_cantidad = data['cantidad']  # Nueva cantidad ingresada en la entrada
    fecha = data['fecha']

    cursor = conexion.cursor()

    # Obtener la cantidad actual de la entrada que se va a actualizar
    cursor.execute('SELECT producto_id, cantidad FROM entrada WHERE id = %s', (entrada_id,))
    entrada_actual = cursor.fetchone()

    if entrada_actual:
        producto_id_actual = entrada_actual[0]
        cantidad_actual = entrada_actual[1]

        # Calcular la diferencia entre la cantidad actual y la nueva cantidad
        diferencia_cantidad = nueva_cantidad - cantidad_actual

        # Actualizar la entrada en la tabla de entradas
        cursor.callproc('sp_actualizar_entrada', (entrada_id, producto_id, nueva_cantidad, fecha))
        conexion.commit()

        cursor.execute('SELECT cantidad FROM inventario WHERE producto_id = %s', (producto_id_actual,))
        inventario_cantidad = cursor.fetchone()

        if inventario_cantidad:
            nueva_cantidad_inventario = inventario_cantidad[0] + diferencia_cantidad
            cursor.execute('UPDATE inventario SET cantidad = %s WHERE producto_id = %s', (nueva_cantidad_inventario, producto_id_actual))
            conexion.commit()

        return jsonify({'mensaje': 'Entrada actualizada correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Entrada no encontrada'}), 404

@app.route('/entradas/<int:entrada_id>', methods=['DELETE'])
def eliminar_entrada(entrada_id):
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM entrada WHERE id = %s', (entrada_id,))
    conexion.commit()

    return jsonify({'mensaje': 'Entrada eliminada correctamente'}), 200

#salida
@app.route('/salidas', methods=['GET'])
def obtener_salidas():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute('SELECT * FROM salida')
    salidas = cursor.fetchall()
    return jsonify(salidas)

@app.route('/salidas', methods=['POST'])
def crear_salida():
    data = request.get_json()
    producto_id = data['producto_id']
    cantidad = data['cantidad']
    fecha = data['fecha']

    cursor = conexion.cursor()

    # Verificar si hay suficiente cantidad en inventario
    cursor.execute('SELECT cantidad FROM inventario WHERE producto_id = %s', (producto_id,))
    inventario_cantidad = cursor.fetchone()

    if inventario_cantidad and inventario_cantidad[0] >= cantidad:
        # Actualizar la cantidad en inventario del producto correspondiente
        nueva_cantidad_inventario = inventario_cantidad[0] - cantidad
        cursor.execute('UPDATE inventario SET cantidad = %s WHERE producto_id = %s', (nueva_cantidad_inventario, producto_id))
        conexion.commit()

        # Insertar la salida en la tabla de salidas
        cursor.execute('INSERT INTO salida (producto_id, cantidad, fecha) VALUES (%s, %s, %s)', (producto_id, cantidad, fecha))
        conexion.commit()

        return jsonify({'mensaje': 'Salida creada correctamente '}), 200
    else:
        return jsonify({'mensaje': 'No hay suficiente cantidad en inventario para realizar la salida'}), 400

@app.route('/salidas/<int:salida_id>', methods=['PUT'])
def actualizar_salida(salida_id):
    data = request.get_json()
    producto_id = data['producto_id']
    nueva_cantidad = data['cantidad']
    fecha = data['fecha']

    cursor = conexion.cursor()

    # Obtener la cantidad actual de la salida que se va a actualizar
    cursor.execute('SELECT producto_id, cantidad FROM salida WHERE id = %s', (salida_id,))
    salida_actual = cursor.fetchone()

    if salida_actual:
        producto_id_actual = salida_actual[0]
        cantidad_actual = salida_actual[1]

        # Calcular la diferencia entre la cantidad actual y la nueva cantidad
        diferencia_cantidad = nueva_cantidad - cantidad_actual

        # Actualizar la salida en la tabla de salidas
        cursor.execute('UPDATE salida SET producto_id = %s, cantidad = %s, fecha = %s WHERE id = %s', (producto_id, nueva_cantidad, fecha, salida_id))
        conexion.commit()

        # Actualizar la cantidad en inventario del producto correspondiente
        cursor.execute('SELECT cantidad FROM inventario WHERE producto_id = %s', (producto_id_actual,))
        inventario_cantidad = cursor.fetchone()

        if inventario_cantidad:
            nueva_cantidad_inventario = inventario_cantidad[0] - diferencia_cantidad
            cursor.execute('UPDATE inventario SET cantidad = %s WHERE producto_id = %s', (nueva_cantidad_inventario, producto_id_actual))
            conexion.commit()

        return jsonify({'mensaje': 'Salida actualizada correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Salida no encontrada'}), 404


@app.route('/salidas/<int:salida_id>', methods=['DELETE'])
def eliminar_salida(salida_id):
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM salida WHERE id = %s', (salida_id,))
    conexion.commit()

    return jsonify({'mensaje': 'Salida eliminada correctamente'}), 200

#productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    return jsonify(productos)

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
