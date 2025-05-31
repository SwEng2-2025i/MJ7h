from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from app.services.notification_service import NotificationService
from app.models.user import User
from app.models.notification import NotificationPayload
from app.utils.logger import logger # Importar la instancia del logger

app = Flask(__name__)

# Configuración de Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # Todo los endpoints
            "model_filter": lambda tag: True,  # Todos los modelos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/" # Ruta para la UI de Swagger
}
swagger = Swagger(app, config=swagger_config)

# Instancia del servicio de notificación
notification_service = NotificationService()

@app.route('/users', methods=['POST'])
@swag_from({
    'tags': ['Usuarios'],
    'summary': 'Registra un nuevo usuario o actualiza uno existente.',
    'description': 'Registra un usuario con su nombre, canal preferido y canales disponibles. Si el usuario ya existe por nombre, se actualizan sus datos.',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Juan Perez'},
                    'preferred_channel': {'type': 'string', 'example': 'email', 'enum': ['email', 'sms', 'whatsapp']},
                    'available_channels': {
                        'type': 'array',
                        'items': {'type': 'string', 'enum': ['email', 'sms', 'whatsapp']},
                        'example': ['email', 'sms', 'whatsapp']
                    }
                },
                'required': ['name', 'preferred_channel', 'available_channels']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuario registrado/actualizado exitosamente.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'preferred_channel': {'type': 'string'},
                            'available_channels': {'type': 'array', 'items': {'type': 'string'}}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Error en la solicitud (e.g., datos faltantes, canal inválido).',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def register_user_route():
    #Registra un nuevo usuario en el sistema.
    data = request.get_json()
    if not data:
        logger.warning("Intento de registro de usuario con payload vacío.")
        return jsonify({"error": "Payload vacío o no es JSON válido."}), 400

    try:
        name = data.get('name')
        preferred_channel = data.get('preferred_channel')
        available_channels = data.get('available_channels')

        if not all([name, preferred_channel, available_channels]):
            logger.warning(f"Intento de registro de usuario con datos incompletos: {data}")
            return jsonify({"error": "Faltan datos: se requiere 'name', 'preferred_channel' y 'available_channels'"}), 400
        if not isinstance(available_channels, list):
             logger.warning(f"available_channels no es una lista para el usuario {name}")
             return jsonify({"error": "'available_channels' debe ser una lista."}), 400

        user = notification_service.register_user(name, preferred_channel, available_channels)
        return jsonify({"message": f"Usuario '{user.name}' registrado/actualizado exitosamente.", "user": user.to_dict()}), 201
    except ValueError as e:
        logger.error(f"Error de validación al registrar usuario: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Excepción inesperada al registrar usuario: {e}", exc_info=True)
        return jsonify({"error": "Ocurrió un error interno."}), 500

@app.route('/users', methods=['GET'])
@swag_from({
    'tags': ['Usuarios'],
    'summary': 'Lista todos los usuarios registrados.',
    'description': 'Obtiene una lista de todos los usuarios que han sido registrados en el sistema.',
    'produces': ['application/json'],
    'responses': {
        200: {
            'description': 'Lista de usuarios obtenida exitosamente.',
            'schema': {
                'type': 'object',
                'properties': {
                    'users': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string'},
                                'preferred_channel': {'type': 'string'},
                                'available_channels': {'type': 'array', 'items': {'type': 'string'}}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_users_route():
    #Lista todos los usuarios registrados.
    users = notification_service.get_all_users()
    return jsonify({"users": [user.to_dict() for user in users]}), 200

@app.route('/notifications/send', methods=['POST'])
@swag_from({
    'tags': ['Notificaciones'],
    'summary': 'Envía una notificación a un usuario específico.',
    'description': 'Envía un mensaje a un usuario utilizando su cadena de canales configurada (preferido primero, luego los de respaldo).',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_name': {'type': 'string', 'example': 'Juan Perez'},
                    'message': {'type': 'string', 'example': 'Tu cita ha sido confirmada.'},
                    'priority': {'type': 'string', 'example': 'high', 'description': 'Prioridad de la notificación (actualmente no afecta la lógica de envío).'}
                },
                'required': ['user_name', 'message', 'priority']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Notificación procesada (puede haber sido enviada o fallado en todos los canales).',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'enviada'},
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Error en la solicitud (e.g., datos faltantes).',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Usuario no encontrado.',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def send_notification_route():
    #Envía una notificación a un usuario.
    data = request.get_json()
    if not data:
        logger.warning("Intento de envío de notificación con payload vacío.")
        return jsonify({"error": "Payload vacío o no es JSON válido."}), 400

    try:
        user_name = data.get('user_name')
        message = data.get('message')
        priority = data.get('priority')

        if not all([user_name, message, priority]):
            logger.warning(f"Intento de envío de notificación con datos incompletos: {data}")
            return jsonify({"error": "Faltan datos: se requiere 'user_name', 'message' y 'priority'"}), 400

        payload = NotificationPayload(user_name, message, priority)
        result = notification_service.send_notification(payload)
        
        if result["status"] == "fallo_usuario_no_encontrado":
            return jsonify({"error": result["message"]}), 404
        elif result["status"] == "fallo_sin_canales" or result["status"] == "fallo_envio":
             # Aún retornamos 200 porque la solicitud fue procesada, pero el mensaje indica el fallo.
            return jsonify(result), 200
        
        return jsonify(result), 200

    except ValueError as e: # Podría surgir de la creación de NotificationPayload
        logger.error(f"Error de validación al enviar notificación: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Excepción inesperada al enviar notificación: {e}", exc_info=True)
        return jsonify({"error": "Ocurrió un error interno."}), 500

if __name__ == '__main__':
    logger.info("Iniciando la aplicación de Notificaciones Multicanal...")
    app.run(debug=True) 