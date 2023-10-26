import mysql.connector

conexion = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='almacen'
)
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255),
        precio FLOAT
    )
''')

cursor.execute('''
    CREATE TABLE entrada (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT,
        cantidad INT,
        fecha DATE,
        INDEX fk_producto_id (producto_id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
''')

cursor.execute('''
    CREATE TABLE salida (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT,
        cantidad INT,
        fecha DATE,
        INDEX fk_producto_id (producto_id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
''')

cursor.execute('''
    CREATE TABLE inventario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT,
        cantidad INT,
        INDEX fk_producto_id (producto_id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
''')




conexion.commit()
conexion.close()

print("Tablas creadas exitosamente en la base de datos MySQL.")
