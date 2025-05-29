from flask_restx import Resource, fields
from app.api.namespaces import notification_ns
from app.services.notification_service import NotificationService
from app.services.user_service import UserService

# Configuración del modelo de validación
notification_model = notification_ns.model('Notification', {
    'user_id': fields.Integer(required=True, description='ID del usuario'),
    'user_name': fields.String(required=False, description='Nombre del usuario (opcional)'), 
    'message': fields.String(required=True, description='Contenido del mensaje'),
    'priority': fields.String(required=True, enum=['low', 'medium', 'high'])
})

# Inicialización del servicio
notification_service = NotificationService(UserService())

@notification_ns.route('/send')
class SendNotification(Resource):
    @notification_ns.doc('send_notification')
    @notification_ns.expect(notification_model)
    @notification_ns.response(200, 'Notificación enviada exitosamente')
    @notification_ns.response(400, 'Datos de entrada inválidos')
    @notification_ns.response(404, 'Usuario no encontrado')
    def post(self):
        data = notification_ns.payload
        result = notification_service.send_notification(
            user_id=data['user_id'],
            user_name=data.get('user_name'),  # Usar .get() para que sea opcional
            message=data['message'],
            priority=data['priority']
        )
        
        if result['status'] == 'error':
            if "not found" in result['message'].lower():
                notification_ns.abort(404, result['message'])
            else:
                notification_ns.abort(400, result['message'])
        
        return result, 200