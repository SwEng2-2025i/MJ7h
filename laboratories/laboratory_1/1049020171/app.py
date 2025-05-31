from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from models.user import User
from notification.handler import NotificationHandler
import sys
import io

# Configura la salida estándar para usar UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)

# Configuración básica de Swagger
app.config['SWAGGER'] = {
    'title': 'Notification API',
    'version': '1.0',
    'description': 'API para enviar notificaciones multicanal',
    'uiversion': 3
}
swagger = Swagger(app)

users = []

@app.route('/users', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'description': 'Registra un nuevo usuario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Yume'},
                    'preferred_channel': {'type': 'string', 'example': 'email'},
                    'available_channels': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['email', 'sms', 'console']
                    }
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Usuario registrado exitosamente'},
        400: {'description': 'Datos inválidos'}
    }
})
def register_user():
    data = request.json
    user = User(
        name=data['name'],
        preferred_channel=data['preferred_channel'],
        available_channels=data['available_channels']
    )
    users.append(user)
    return jsonify({"message": "Usuario registrado"}), 201

@app.route('/users', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'description': 'Lista todos los usuarios registrados',
    'responses': {
        200: {
            'description': 'Lista de usuarios',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'preferred_channel': {'type': 'string'},
                        'available_channels': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def list_users():
    return jsonify([user.__dict__ for user in users])

@app.route('/notifications/send', methods=['POST'])
@swag_from({
    'tags': ['Notifications'],
    'description': 'Envía una notificación al usuario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_name': {'type': 'string', 'example': 'Yume'},
                    'message': {'type': 'string', 'example': 'Tu cita es mañana'},
                    'priority': {'type': 'string', 'example': 'high'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Notificación enviada',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'}
                }
            }
        },
        404: {'description': 'Usuario no encontrado'}
    }
})
def send_notification():
    data = request.json
    user = next((u for u in users if u.name == data['user_name']), None)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    handler = NotificationHandler(user)
    success = handler.handle(
        message=data['message'],
        priority=data.get('priority', 'medium')
    )
    
    return jsonify({"success": success}), 200 if success else 500

if __name__ == '__main__':
    app.run(debug=True)