from flask import Flask, request
from flask_restx import Api, Resource, fields
from services import NotificationService

app = Flask(__name__)
api = Api(app, version='1.0', title='Multichannel Notification System API',
          description='A REST API for a notification system using Chain of Responsibility and Singleton patterns.',
          doc='/swagger/') # Added swagger UI path

# Initialize service
notification_service = NotificationService()

# Define namespaces
ns_users = api.namespace('users', description='User operations')
ns_notifications = api.namespace('notifications', description='Notification operations')

# Define models for request and response payloads
user_model = api.model('UserModel', {
    'name': fields.String(required=True, description='User name'),
    'preferred_channel': fields.String(required=True, description='Preferred notification channel'),
    'available_channels': fields.List(fields.String, required=True, description='List of available channels')
})

notification_model = api.model('NotificationModel', {
    'user_name': fields.String(required=True, description='User name to send notification to'),
    'message': fields.String(required=True, description='Notification message'),
    'priority': fields.String(required=True, description='Notification priority (e.g., high, medium, low)')
})

@ns_users.route('')
class UserList(Resource):
    @ns_users.doc('list_users')
    @ns_users.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return notification_service.get_all_users()

    @ns_users.doc('create_user')
    @ns_users.expect(user_model)
    @ns_users.marshal_with(user_model, code=201)
    def post(self):
        """Register a new user"""
        data = request.json
        user = notification_service.register_user(data['name'], data['preferred_channel'], data['available_channels'])
        if user:
            return user, 201
        api.abort(400, "User already exists or invalid data")

@ns_notifications.route('/send')
class NotificationSend(Resource):
    @ns_notifications.doc('send_notification')
    @ns_notifications.expect(notification_model)
    def post(self):
        """Send a notification"""
        data = request.json
        success, message = notification_service.send_notification(data['user_name'], data['message'], data['priority'])
        if success:
            return {'message': message}, 200
        else:
            return {'message': message}, 400 # Or another appropriate error code

if __name__ == '__main__':
    app.run(debug=True) 