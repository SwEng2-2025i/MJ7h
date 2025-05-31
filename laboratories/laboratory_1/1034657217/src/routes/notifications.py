# routes/notification_routes.py
from flask_restx import Resource, fields
from utils.logger import Logger
from services.notification_service import NotificationService

# Instancia NotificationService 
notification_service_instance = None # Se asignará en init_notification_routes

# Este namespace será inicializado en main.py
notification_ns = None

def init_notification_routes(api_instance, service_instance):
    """
    Inicializa las rutas de notificación y los modelos de Flask-RestX.
    Debe ser llamado desde main.py.
    """
    global notification_ns, notification_service_instance
    notification_ns = api_instance.namespace('notifications', description='Notification operations')
    notification_service_instance = service_instance

    notification_send_model = api_instance.model('NotificationSend', {
        'user_name': fields.String(required=True, description='Name of the user to notify'),
        'message': fields.String(required=True, description='The notification message'),
        'priority': fields.String(enum=['high', 'medium', 'low'], default='medium', description='Priority of the notification')
    })

    @notification_ns.route('/send')
    class NotificationSender(Resource):
        @notification_ns.doc('send_notification')
        @notification_ns.expect(notification_send_model, validate=True)
        @notification_ns.response(200, 'Notification sent successfully')
        @notification_ns.response(400, 'Missing data or Validation Error')
        @notification_ns.response(500, 'Failed to send notification')
        def post(self):
            """Send a notification to a user"""
            data = notification_ns.payload
            user_name = data.get('user_name')
            message = data.get('message')
            priority = data.get('priority', 'medium')

            try:
                # Asegúrate de que notification_service_instance.sendNotification espera el dict completo
                success, msg = notification_service_instance.sendNotification(data)
                if success:
                    return {'message': msg}, 200
                else:
                    notification_ns.abort(500, msg)
            except Exception as e:
                Logger().log(f"Error sending notification: {e}")
                notification_ns.abort(500, str(e))
    
    return notification_ns