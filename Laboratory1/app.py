from flask import Flask, request, jsonify
from models.user import User
from channels.email import EmailChannel
from channels.sms import SMSChannel
from channels.console import ConsoleChannel

import random

app = Flask(__name__)

# Base de datos en memoria
users_db = {}

# Función para construir la cadena de canales según los canales disponibles y preferido
def build_channel_chain(user):
    # Ordena los canales según el preferido; después, los otros
    ordered = [user.preferred_channel] + [ch for ch in user.available_channels if ch != user.preferred_channel]
    
    handler = None
    # Crea la cadena en orden inverso para que el primero sea el preferido
    for channel in reversed(ordered):
        if channel == 'email':
            handler = EmailChannel(next_handler=handler)
        elif channel == 'sms':
            handler = SMSChannel(next_handler=handler)
        elif channel == 'console':
            handler = ConsoleChannel(next_handler=handler)
    return handler

# Endpoint para registrar usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data['name']
    preferred = data['preferred_channel']
    available = data['available_channels']
    if name in users_db:
        return jsonify({'error': 'User already exists'}), 400
    users_db[name] = User(name, preferred, available)
    return jsonify({'message': f'User {name} created'}), 201

# Endpoint para listar usuarios
@app.route('/users', methods=['GET'])
def list_users():
    return jsonify([
        {
            'name': user.name,
            'preferred_channel': user.preferred_channel,
            'available_channels': user.available_channels
        }
        for user in users_db.values()
    ])

# Endpoint para enviar notificación
@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.json
    user_name = data['user_name']
    message = data['message']
    priority = data['priority']

    user = users_db.get(user_name)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    chain = build_channel_chain(user)
    success = chain.handle(user, message)
    if success:
        return jsonify({'message': 'Notification sent successfully'})
    else:
        return jsonify({'message': 'All channels failed!'}), 500

if __name__ == '__main__':
    app.run(debug=True)