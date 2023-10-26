import mysql.connector

conexion = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='almacen'
)


cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255),
        precio FLOAT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS entrada (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT,
        cantidad INT,
        fecha DATE,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS salida (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT,
        cantidad INT,
        fecha DATE,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT,
        cantidad INT,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
''')

#Sp
cursor.execute('''
CREATE PROCEDURE IF NOT EXISTS sp_insertar_entrada(
    IN p_producto_id INT,
    IN p_cantidad INT,
    IN p_fecha DATE
)
BEGIN
    INSERT INTO entrada (producto_id, cantidad, fecha)
    VALUES (p_producto_id, p_cantidad, p_fecha);
END
''')
cursor.execute('''
CREATE PROCEDURE IF NOT EXISTS sp_actualizar_entrada(
    IN p_entrada_id INT,
    IN p_producto_id INT,
    IN p_cantidad INT,
    IN p_fecha DATE
)
BEGIN
    UPDATE entrada
    SET producto_id = p_producto_id, cantidad = p_cantidad, fecha = p_fecha
    WHERE id = p_entrada_id;
END
''')

# Crear vista inventario_productos
cursor.execute('''
CREATE VIEW IF NOT EXISTS vista_inventario_productos AS
SELECT p.id AS producto_id, p.nombre AS producto_nombre, p.precio AS producto_precio, i.cantidad AS inventario_cantidad
FROM productos p
LEFT JOIN inventario i ON p.id = i.producto_id;
''')

conexion.commit()
conexion.close()

print("Tablas creadas exitosamente en la base de datos MySQL.")



