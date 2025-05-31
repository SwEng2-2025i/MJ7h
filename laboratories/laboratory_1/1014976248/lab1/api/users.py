from flask_restx import Resource, fields
from flask import request
from models.user import user_manager
from extensions import api

# Define el modelo Swagger para el cuerpo del POST /users
user_model = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'preferred_channel': fields.String(required=True, description='Preferred notification channel'),
    'available_channels': fields.List(fields.String, required=True, description='Available notification channels')
})

# Endpoint para registrar y listar usuarios
class UsersResource(Resource):

    @api.doc('register_user')             # Documentación Swagger: nombre del endpoint
    @api.expect(user_model)              # Modelo de entrada esperado
    @api.response(201, 'User registered successfully')
    @api.response(400, 'Invalid input')
    def post(self):
        """
        POST /users

        Registra un nuevo usuario con un canal preferido y una lista de canales disponibles.
        Valida que el canal preferido esté dentro de la lista y que los canales sean válidos.
        """
        try:
            data = request.get_json()
            if not data:
                return {'error': 'Request body is required'}, 400

            # Validación de campos obligatorios
            required_fields = ['name', 'preferred_channel', 'available_channels']
            for field in required_fields:
                if field not in data:
                    return {'error': f'Field {field} is required'}, 400

            # Llama al UserManager para registrar al usuario
            user = user_manager.register_user(
                data['name'],
                data['preferred_channel'],
                data['available_channels']
            )

            # Devuelve el usuario creado
            return {
                'message': 'User registered successfully',
                'user': user.to_dict()
            }, 201

        except ValueError as e:
            # Errores de validación lógica (ej. canal inválido)
            return {'error': str(e)}, 400
        except Exception as e:
            # Errores internos inesperados
            return {'error': f'Internal server error: {str(e)}'}, 500

    @api.doc('list_users')              # Documentación Swagger
    @api.response(200, 'Success')
    def get(self):
        """
        GET /users

        Retorna la lista de todos los usuarios registrados, incluyendo sus canales.
        """
        try:
            users = user_manager.get_all_users()
            return {
                'users': [user.to_dict() for user in users],  # Serializa cada usuario
                'total': len(users)
            }, 200
        except Exception as e:
            return {'error': f'Internal server error: {str(e)}'}, 500
