
from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos simulada en memoria
bandas_db = [
    {
        "id": 1,
        "nombre": "Queen",
        "genero": "Rock",
        "pais_origen": "Reino Unido",
        "año_formacion": 1970,
        "integrantes": ["Freddie Mercury", "Brian May", "Roger Taylor", "John Deacon"]
    },
    {
        "id": 2,
        "nombre": "Soda Stereo",
        "genero": "Rock en Español",
        "pais_origen": "Argentina",
        "año_formacion": 1982,
        "integrantes": ["Gustavo Cerati", "Zeta Bosio", "Charly Alberti"]
    }
]
next_banda_id = 3 # Para asignar IDs a nuevas bandas

@app.route('/')
def index():
    return "<h1>API de Gestión de Bandas</h1><p>Endpoints disponibles: /bandas</p>"

# --- CRUD Operations ---

# CREATE: Añadir una nueva banda
@app.route('/bandas', methods=['POST'])
def crear_banda():
    global next_banda_id
    datos_banda = request.get_json()

    if not datos_banda or not 'nombre' in datos_banda or not 'genero' in datos_banda:
        return jsonify({"error": "Datos incompletos. Se requiere 'nombre' y 'genero'."}), 400

    nueva_banda = {
        "id": next_banda_id,
        "nombre": datos_banda['nombre'],
        "genero": datos_banda['genero'],
        "pais_origen": datos_banda.get('pais_origen', 'Desconocido'), # .get() para valores opcionales
        "año_formacion": datos_banda.get('año_formacion', None),
        "integrantes": datos_banda.get('integrantes', [])
    }
    bandas_db.append(nueva_banda)
    next_banda_id += 1
    return jsonify(nueva_banda), 201 # 201 Created

# READ: Obtener todas las bandas
@app.route('/bandas', methods=['GET'])
def obtener_todas_las_bandas():
    return jsonify(bandas_db)

# READ: Obtener una banda por su ID
@app.route('/bandas/<int:banda_id>', methods=['GET'])
def obtener_banda_por_id(banda_id):
    banda_encontrada = next((banda for banda in bandas_db if banda["id"] == banda_id), None)
    if banda_encontrada:
        return jsonify(banda_encontrada)
    else:
        return jsonify({"error": "Banda no encontrada"}), 404 # 404 Not Found

# UPDATE: Actualizar una banda existente
@app.route('/bandas/<int:banda_id>', methods=['PUT'])
def actualizar_banda(banda_id):
    banda_actualizar = next((banda for banda in bandas_db if banda["id"] == banda_id), None)
    if not banda_actualizar:
        return jsonify({"error": "Banda no encontrada para actualizar"}), 404

    datos_nuevos = request.get_json()
    if not datos_nuevos:
        return jsonify({"error": "No se enviaron datos para actualizar"}), 400

    # Actualizar solo los campos proporcionados
    banda_actualizar["nombre"] = datos_nuevos.get('nombre', banda_actualizar["nombre"])
    banda_actualizar["genero"] = datos_nuevos.get('genero', banda_actualizar["genero"])
    banda_actualizar["pais_origen"] = datos_nuevos.get('pais_origen', banda_actualizar["pais_origen"])
    banda_actualizar["año_formacion"] = datos_nuevos.get('año_formacion', banda_actualizar["año_formacion"])
    banda_actualizar["integrantes"] = datos_nuevos.get('integrantes', banda_actualizar["integrantes"])

    return jsonify(banda_actualizar)

# DELETE: Eliminar una banda
@app.route('/bandas/<int:banda_id>', methods=['DELETE'])
def eliminar_banda(banda_id):
    global bandas_db
    banda_eliminar = next((banda for banda in bandas_db if banda["id"] == banda_id), None)
    if not banda_eliminar:
        return jsonify({"error": "Banda no encontrada para eliminar"}), 404

    bandas_db = [banda for banda in bandas_db if banda["id"] != banda_id]
    return jsonify({"mensaje": f"Banda con ID {banda_id} eliminada correctamente"}), 200 # O 204 No Content si no devuelves cuerpo

if __name__ == '__main__':
    print("Iniciando servidor API de Bandas en http://localhost:5000")
    app.run(port=5000, debug=True)
