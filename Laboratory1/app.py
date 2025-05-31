from flask import Flask, request, jsonify
from models.user import User
from channels.email import EmailChannel
from channels.sms import SMSChannel
from channels.console import ConsoleChannel
from logger import Logger
from flasgger import Swagger
import random

app = Flask(__name__)
swagger = Swagger(app)


# Base de datos en memoria
users_db = {}

# Función para construir la cadena de canales según los canales disponibles y preferido
def build_channel_chain(user):
    """
    Construye la cadena de canales para notificaciones en base a la preferencia del usuario.
    Args:
        user (User): El usuario al que se notificará.
    Returns:
        Channel: El canal inicial de la cadena.
    """
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
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              description: Nombre del usuario
            preferred_channel:
              type: string
              enum: [email, sms, console]
              description: Canal preferido para notificaciones
            available_channels:
              type: array
              items:
                type: string
              description: Lista de canales disponibles
    responses:
      201:
        description: Usuario creado exitosamente
      400:
        description: El usuario ya existe
    """
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
    """
    Listar todos los usuarios registrados
    ---
    tags:
      - Users
    responses:
      200:
        description: Lista de usuarios
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              preferred_channel:
                type: string
              available_channels:
                type: array
                items:
                  type: string
    """
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
    """
    Enviar notificación a un usuario
    ---
    tags:
      - Notifications
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              description: Nombre del usuario destinatario
            message:
              type: string
              description: Mensaje de la notificación
            priority:
              type: string
              description: Prioridad de la notificación
    responses:
      200:
        description: Notificación enviada exitosamente
      404:
        description: Usuario no encontrado
      500:
        description: Fallaron todos los canales
    """
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

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Obtener logs del sistema
    ---
    tags:
      - Logs
    responses:
      200:
        description: Lista de logs del sistema
        schema:
          type: object
          properties:
            logs:
              type: array
              items:
                type: string
    """
    logger = Logger()
    return jsonify({'logs': logger.get_logs()})

if __name__ == '__main__':
    app.run(debug=True)
