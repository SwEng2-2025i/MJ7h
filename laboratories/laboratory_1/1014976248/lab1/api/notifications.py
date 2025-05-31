from flask_restx import Resource, fields
from flask import request
from extensions import api
from services.notification_service import NotificationService
from models.user import user_manager

# Inicializa el servicio de notificaciones con el manejador de usuarios
notification_service = NotificationService(user_manager)

# Modelo para la documentación Swagger del cuerpo del POST /notifications/send
notification_model = api.model('Notification', {
    'user_name': fields.String(required=True, description='Target user name'),
    'message': fields.String(required=True, description='Notification message'),
    'priority': fields.String(required=False, default='normal', description='Message priority (low, normal, high)')
})

# Endpoint para enviar una notificación a un usuario
class NotificationResource(Resource):
    @api.doc('send_notification')              # Nombre en la documentación Swagger
    @api.expect(notification_model)            # Define qué datos espera el endpoint
    @api.response(200, 'Notification sent successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'User not found')
    def post(self):
        """
        POST /notifications/send

        Envía una notificación a un usuario utilizando su cadena de canales disponibles.
        Prioriza el canal preferido y recurre a otros si hay fallos.
        """
        try:
            data = request.get_json()  # Extrae JSON del body
            if not data:
                return {'error': 'Request body is required'}, 400

            # Validación de campos obligatorios
            required_fields = ['user_name', 'message']
            for field in required_fields:
                if field not in data:
                    return {'error': f'Field {field} is required'}, 400

            # Si no se especifica prioridad, se usa 'normal'
            priority = data.get('priority', 'normal')

            # Ejecuta el proceso de envío de notificación
            result = notification_service.send_notification(
                data['user_name'],
                data['message'],
                priority
            )

            # Si fue exitosa, retorna 200. Si no, 202 (aceptada pero fallida en ejecución).
            status_code = 200 if result['success'] else 202
            return result, status_code

        except ValueError as e:
            # Error de negocio (por ejemplo, usuario no encontrado)
            return {'error': str(e)}, 404
        except Exception as e:
            # Error inesperado del sistema
            return {'error': f'Internal server error: {str(e)}'}, 500

# Endpoint para consultar el historial de intentos de notificación
class NotificationHistoryResource(Resource):
    @api.doc('get_notification_history')
    @api.response(200, 'Success')
    def get(self):
        """
        GET /notifications/history

        Retorna el historial de todos los intentos de notificación registrados
        por el logger singleton. Incluye tanto exitosos como fallidos.
        """
        try:
            from logger.notification_logger import NotificationLogger
            logger = NotificationLogger()
            history = logger.get_history()
            return {
                'history': history,
                'total': len(history)
            }, 200
        except Exception as e:
            return {'error': f'Internal server error: {str(e)}'}, 500
