import uuid
import re
import hashlib
from config import get_conexion
from datetime import datetime

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# === NEONATOS ===

def registrar_neonato(fecha_nac, servicio, madre, hora_nac, peso, talla, genero):
    codigo = str(uuid.uuid4())[:8]
    conexion, cursor = get_conexion()
    cursor.execute(
        "INSERT INTO neonatos (codigo, madre, fecha_nac, servicio, hora_nac, peso, talla, genero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (codigo, madre, fecha_nac, servicio, hora_nac, peso, talla, genero)
    )
    conexion.commit()
    conexion.close()
    return codigo

def buscar_por_codigo(codigo):
    try:
        conexion, cursor = get_conexion()
        cursor.execute("SELECT * FROM neonatos WHERE codigo = %s", (codigo,))
        resultado = cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar el código: {e}")
        resultado = None
    finally:
        conexion.close()
    return resultado



def obtener_todos_los_neonatos():
    conexion, cursor = get_conexion()
    cursor.execute("SELECT codigo, madre, fecha_nac, hora_nac, genero FROM neonatos")
    datos = cursor.fetchall()
    conexion.close()
    return datos

# === PERSONAL ===

def registrar_personal(username, password, cedula, nombre):
    conexion, cursor = get_conexion()
    cursor.execute("SELECT * FROM personal WHERE username=%s", (username,))
    if not cursor.fetchone():
        hashed_pw = hash_password(password)
        cursor.execute(
            "INSERT INTO personal (username, password, cedula, nombre) VALUES (%s, %s, %s, %s)",
            (username, hashed_pw, cedula, nombre)
        )
        conexion.commit()
        conexion.close()
        return True
    conexion.close()
    return False


def verificar_profesional_db(username, password):
    conexion, cursor = get_conexion()
    hashed_pw = hash_password(password)
    cursor.execute(
        "SELECT * FROM personal WHERE username=%s AND password=%s",
        (username, hashed_pw)
    )
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None

def obtener_datos_usuario_completo(username):
    conexion, cursor = get_conexion()
    cursor.execute(
        "SELECT nombre, cedula, username FROM personal WHERE username = %s",
        (username,)
    )
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

# VALIDACIONES

def validar_hora(hora):
    return bool(re.fullmatch(r"\d{2}:\d{2}", hora))