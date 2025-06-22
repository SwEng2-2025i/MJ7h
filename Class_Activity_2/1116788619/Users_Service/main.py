from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacenamiento en memoria
usuarios = {}
contador_usuarios = 1

@app.route('/users', methods=['POST'])
def crear_usuario():
    global contador_usuarios
    datos = request.get_json()
    if 'name' not in datos:
        return jsonify({'error': 'Falta el nombre del usuario'}), 400
    
    user_id = str(contador_usuarios)
    usuarios[user_id] = {
        'id': user_id,
        'name': datos['name']
    }
    contador_usuarios += 1
    return jsonify(usuarios[user_id]), 201

@app.route('/users/<user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):
    if user_id in usuarios:
        del usuarios[user_id]
        return jsonify({'message': f'Usuario {user_id} eliminado'}), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/users/<user_id>', methods=['GET'])
def obtener_usuario(user_id):
    if user_id in usuarios:
        return jsonify(usuarios[user_id]), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/users', methods=['GET'])
def listar_usuarios():
    return jsonify(list(usuarios.values())), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
