from flask import Flask, request, jsonify
from crud import (
    registrar_neonato,
    buscar_por_codigo,
    obtener_todos_los_neonatos,
    registrar_personal,
    verificar_profesional_db,
    obtener_datos_usuario_completo,
    validar_hora
)

app = Flask(__name__)

# Ruta para registrar neonato (POST)
@app.route('/registrar_neonato', methods=['POST'])
def api_registrar_neonato():
    data = request.json
    required_fields = ['fecha_nac', 'servicio', 'madre', 'hora_nac', 'peso', 'talla', 'genero']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    # Validar hora
    if not validar_hora(data['hora_nac']):
        return jsonify({"error": "Formato de hora inválido, debe ser HH:MM"}), 400
    codigo = registrar_neonato(
        data['fecha_nac'], data['servicio'], data['madre'],
        data['hora_nac'], data['peso'], data['talla'], data['genero']
    )
    return jsonify({"mensaje": "Neonato registrado", "codigo": codigo})

# Ruta para buscar neonato por código (POST o GET)
@app.route('/buscar_por_codigo', methods=['POST'])
def api_buscar_por_codigo():
    data = request.json
    codigo = data.get('codigo')
    if not codigo:
        return jsonify({"error": "Falta código"}), 400
    neonato = buscar_por_codigo(codigo)
    if neonato:
        # suponiendo que el resultado es una tupla que corresponde a las columnas de la tabla
        campos = ['codigo', 'madre', 'fecha_nac', 'servicio', 'hora_nac', 'peso', 'talla', 'genero']
        return jsonify(dict(zip(campos, neonato)))
    else:
        return jsonify({"error": "Neonato no encontrado"}), 404

# Ruta para obtener todos los neonatos (GET)
@app.route('/todos_los_neonatos', methods=['GET'])
def api_todos_los_neonatos():
    datos = obtener_todos_los_neonatos()
    campos = ['codigo', 'madre', 'fecha_nac', 'hora_nac', 'genero']
    lista = [dict(zip(campos, fila)) for fila in datos]
    return jsonify(lista)

# Ruta para registrar personal (POST)
@app.route('/registrar_personal', methods=['POST'])
def api_registrar_personal():
    data = request.json
    required_fields = ['username', 'password', 'cedula', 'nombre']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    success = registrar_personal(data['username'], data['password'], data['cedula'], data['nombre'])
    if success:
        return jsonify({"mensaje": "Usuario registrado"})
    else:
        return jsonify({"error": "Username ya existe"}), 409

# Ruta para login (POST)
@app.route('/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Falta username o password"}), 400
    if verificar_profesional_db(username, password):
        usuario = obtener_datos_usuario_completo(username)
        campos = ['nombre', 'cedula', 'username']
        return jsonify(dict(zip(campos, usuario)))
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)