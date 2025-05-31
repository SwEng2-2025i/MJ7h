from flask import Flask, request, jsonify
from models.user_store import UserStore
from channels.builder import build_chain
from extra.logger import logger
from flask_swagger_ui import get_swaggerui_blueprint
import random

app = Flask(__name__)

# Configuración de Swagger UI
SWAGGER_URL = '/docs'           
API_URL = '/static/swagger.yaml' 

# Configuración de Swagger UI para la documentación de la API
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # optional swagger-ui config overrides
        'app_name': "Multichannel Notification System"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)



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
        return jsonify({'error': 'The name, preferred_channel or available_channels is missing'}), 400

    if preferred not in available:
        return jsonify({'error': 'the preferred_channel must be in the list of available'}), 400

    success = user_store.add_user(name, preferred, available)
    if not success:
        return jsonify({'error': 'User already exist'}), 400

    return jsonify({'message': f'user {name} registered.'}), 201

# notificaciones 

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority', 'normal')
    # verificacion vasica de contenido
    if not user_name or not message:
        return jsonify({'error': 'Missing user_name or message'}), 400
    user = user_store.get_user(user_name)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    
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