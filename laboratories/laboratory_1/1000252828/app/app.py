from flask import Flask, request, jsonify
from models.user_store import UserStore
from channels.builder import build_chain
from extra.logger import logger
import random

app = Flask(__name__)

user_store = UserStore()
# obtener usuarios
@app.route('/users', methods=['GET'])
def list_users():
    users = user_store.list_users()
    return jsonify({'users': users}), 200

# api de users para registrar un usuario
@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels', [])

    if not name or not preferred or not available:
        return jsonify({'error': 'Falta nombre, canal preferido o canales disponibles'}), 400

    if preferred not in available:
        return jsonify({'error': 'El canal preferido debe estar en la lista de disponibles'}), 400

    success = user_store.add_user(name, preferred, available)
    if not success:
        return jsonify({'error': 'Usuario ya existe'}), 400

    return jsonify({'message': f'Usuario {name} registrado.'}), 201

# notificaciones 

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority', 'normal')
    # verificacion vasica de contenido
    if not user_name or not message:
        return jsonify({'error': 'Falta user_name o message'}), 400
    user = user_store.get_user(user_name)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Verificamos que el usuario tenga canales disponibles
    chain = build_chain(user['available_channels'], user['preferred_channel'])

    delivered = False
    attempts = []
    current = chain
    # Iteramos sobre la cadena de responsabilidad para enviar el mensaje
    while current:
        channel_name = current.name
        # Simula el envío del mensaje a través del canal con la posibilidad de que salga mal
        success = random.choice([True, False])
        # guarda el log del intento
        logger.log_attempt(user_name, channel_name, message, success)
        attempts.append({'channel': channel_name, 'success': success})
        if success:
            delivered = True
            break
        current = current.next_channel

    return jsonify({
        'delivered': delivered,
        'attempts': attempts,
        'priority': priority
    }), 200




if __name__ == '__main__':
    app.run(debug=True)