"""
app.py - Módulo principal de la aplicación Flask para el Sistema de Notificación Multicanal

Este módulo configura e inicia la API REST que permite:
1. Registrar usuarios con sus canales de notificación preferidos
2. Listar usuarios registrados
3. Enviar notificaciones a través de múltiples canales

Dependencias:
- Flask: Framework web para crear la API REST
- Flasgger: Para generar documentación Swagger interactiva
- Logger: Utilidad para registro de eventos (patrón Singleton)
- Services: Contiene la lógica de negocio (UserService y NotificationService)
- Config: Configuración específica para Swagger
"""

from flask import Flask, request, jsonify
from flasgger import Swagger  # Para documentación Swagger UI
from logger import Logger  # Logger Singleton
from services import UserService, NotificationService  # Servicios de negocio
from config import SWAGGER_CONFIG  # Configuración de Swagger

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de Swagger para documentación interactiva
Swagger(app, template=SWAGGER_CONFIG)

# Inicialización de servicios globales
user_service = UserService()  # Servicio para gestión de usuarios
notification_service = NotificationService(user_service)  # Servicio para notificaciones
logger = Logger()  # Instancia única del Logger (Singleton)

@app.route('/users', methods=['POST'])
def register_user():
    """
    Endpoint para registrar un nuevo usuario
    
    Documentación Swagger:
    ---
    tags:
      - users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              example: "Juan"
            preferred_channel:
              type: string
              example: "email"
            available_channels:
              type: array
              items:
                type: string
              example: ["email", "sms"]
    responses:
      201:
        description: Usuario registrado exitosamente
      400:
        description: Datos de entrada inválidos
    """
    # Obtener datos JSON del request
    data = request.get_json()
    
    try:
        # Registrar usuario mediante el servicio
        user = user_service.register_user(
            data['name'],
            data['preferred_channel'],
            data['available_channels']
        )
        
        # Registrar evento en logger
        logger.log(f"Usuario registrado: {user.name}")
        
        # Devolver respuesta exitosa
        return jsonify(user.to_dict()), 201
    
    except (KeyError, ValueError) as e:
        # Manejar errores de validación
        logger.log(f"Error registrando usuario: {str(e)}", "ERROR")
        return jsonify({"error": str(e)}), 400

@app.route('/users', methods=['GET'])
def list_users():
    """
    Endpoint para listar todos los usuarios registrados
    
    Documentación Swagger:
    ---
    tags:
      - users
    responses:
      200:
        description: Lista de usuarios registrados
    """
    # Obtener todos los usuarios y convertirlos a formato JSON
    users = [user.to_dict() for user in user_service.get_all_users()]
    return jsonify(users)

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Endpoint para enviar una notificación
    
    Documentación Swagger:
    ---
    tags:
      - notifications
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              example: "Juan"
            message:
              type: string
              example: "Your appointment is tomorrow"
            priority:
              type: string
              example: "high"
    responses:
      200:
        description: Notificación entregada exitosamente
      404:
        description: Usuario no encontrado
      500:
        description: Todos los canales de entrega fallaron
    """
    data = request.get_json()
    try:
        # Enviar notificación mediante el servicio
        result = notification_service.send_notification(
            data['user_name'],
            data['message'],
            data['priority']
        )
        
        # Manejar diferentes resultados
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except ValueError as e:
        # Manejar usuario no encontrado
        logger.log(f"Error enviando notificación: {str(e)}", "ERROR")
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    # Iniciar la aplicación en modo debug en el puerto 5001
    app.run(debug=True, port=5001)