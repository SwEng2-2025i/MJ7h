# swagger_config.py
from flask_restx import Api, fields 

def configure_swagger(app):
    api = Api(
        app,
        version='1.0',
        title='Multichannel Notification System API',
        description='A REST API for managing users and sending multichannel notifications with fallback mechanisms.',
        doc='/apidocs/'
    )

    # Define common models for Swagger documentation
    
    user_model = api.model('User', {
        'name': fields.String(required=True, description='Unique name of the user'),
        'preferred_channel': fields.String(required=True, description='Preferred notification channel (e.g., "email", "sms", "console")', enum=['email', 'sms', 'console']),
        'available_channels': fields.List(fields.String, required=True, description='List of available notification channels for the user', enum=['email', 'sms', 'console'])
    })

 
    notification_send_model = api.model('NotificationSend', {
        'user_name': fields.String(required=True, description='Name of the user to send the notification to'),
        'message': fields.String(required=True, description='The notification message content'),
        'priority': fields.String(required=True, description='Priority of the notification (e.g., "high", "medium", "low")', enum=['high', 'medium', 'low'])
    })

    users_ns = api.namespace('users', description='User management operations')
    notifications_ns = api.namespace('notifications', description='Notification sending operations')

    return api, users_ns, notifications_ns