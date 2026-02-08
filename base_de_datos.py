# base_de_datos.py
import sqlite3
from datetime import datetime, timedelta

# Crear base de datos y tabla si no existe
def crear_base_de_datos():
    conn = sqlite3.connect('precios_viaje.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        precio REAL,
        fecha_actualizacion TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Función para guardar los precios en la base de datos
def guardar_precio_en_bd(producto, precio):
    try:
        conn = sqlite3.connect('precios_viaje.db')
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT INTO productos (producto, precio, fecha_actualizacion)
        VALUES (?, ?, ?)
        ''', (producto, precio, fecha_actual))

        conn.commit()
        conn.close()
        print(f"Precio de {producto} guardado correctamente.")
    except Exception as e:
        print(f"Error al guardar el precio en la base de datos: {e}")

# Función para obtener el precio de la base de datos
def obtener_precio_bd(producto):
    try:
        conn = sqlite3.connect('precios_viaje.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT precio, fecha_actualizacion FROM productos WHERE producto = ? ORDER BY fecha_actualizacion DESC LIMIT 1
        ''', (producto,))
        
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            precio, fecha_actualizacion = resultado
            fecha_actualizacion = datetime.strptime(fecha_actualizacion, '%Y-%m-%d %H:%M:%S')

            # Si la fecha de actualización es más reciente que 1 día
            if datetime.now() - fecha_actualizacion < timedelta(days=1):
                return precio
            else:
                return None  # Si el precio está desactualizado o no tiene 1 día, retornar None

        return None  # Si no existe el producto en la base de datos, retornar None
    except Exception as e:
        print(f"Error al consultar el precio en la base de datos: {e}")
        return None
