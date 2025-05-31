from flask import Flask, request, jsonify
from flask_restx import Resource
from models import User, Notification
from logger import Logger
from handlers import ChannelChainBuilder
from swagger_config import configure_swagger

app = Flask(__name__)

# Initialize the logger (Singleton pattern)
logger = Logger.get_instance()

# Configure Swagger UI
api, users_ns, notifications_ns = configure_swagger(app)

# In-memory data storage
users_db = {} # Stores User objects, keyed by name

@users_ns.route('/')
class UserList(Resource):
    """
    Handles operations related to listing and registering users.
    """
    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(api.models['User'])
    def get(self):
        """
        List all registered users.
        """
        logger.log("GET /users - Listing all users.")
        return [user.to_dict() for user in users_db.values()]

    @users_ns.doc('register_user')
    @users_ns.expect(api.models['User'])
    @users_ns.response(201, 'User registered successfully')
    @users_ns.response(400, 'Invalid input')
    @users_ns.response(409, 'User with this name already exists')
    def post(self):
        """
        Register a new user.
        """
        data = request.json
        name = data.get('name')
        preferred_channel = data.get('preferred_channel')
        available_channels = data.get('available_channels')

        if not all([name, preferred_channel, available_channels]):
            logger.log(f"POST /users - Missing data: {data}")
            return {'message': 'Missing name, preferred_channel, or available_channels'}, 400

        if name in users_db:
            logger.log(f"POST /users - User '{name}' already exists.")
            return {'message': f'User with name "{name}" already exists'}, 409
        
        # Validate channels
        valid_channels = ["email", "sms", "console"]
        if preferred_channel not in valid_channels:
            logger.log(f"POST /users - Invalid preferred channel: {preferred_channel}")
            return {'message': f'Invalid preferred channel: {preferred_channel}. Must be one of {valid_channels}.'}, 400
        
        if not all(channel in valid_channels for channel in available_channels):
            logger.log(f"POST /users - Invalid channel in available_channels: {available_channels}")
            return {'message': f'Invalid channel in available_channels. Must be one of {valid_channels}.'}, 400

        new_user = User(name, preferred_channel, available_channels)
        users_db[name] = new_user
        logger.log(f"POST /users - User '{name}' registered successfully.")
        return {'message': 'User registered successfully', 'user': new_user.to_dict()}, 201

@notifications_ns.route('/send')
class NotificationSender(Resource):
    """
    Handles sending notifications to users.
    """
    @notifications_ns.doc('send_notification')
    @notifications_ns.expect(api.models['NotificationSend'])
    @notifications_ns.response(200, 'Notification process initiated')
    @notifications_ns.response(400, 'Invalid input')
    @notifications_ns.response(404, 'User not found')
    @notifications_ns.response(500, 'Notification delivery failed for all channels')
    def post(self):
        """
        Send a notification to a specific user.
        The system will attempt delivery via preferred channel, then fall back to available channels.
        """
        data = request.json
        user_name = data.get('user_name')
        message = data.get('message')
        priority = data.get('priority')

        if not all([user_name, message, priority]):
            logger.log(f"POST /notifications/send - Missing data: {data}")
            return {'message': 'Missing user_name, message, or priority'}, 400

        user = users_db.get(user_name)
        if not user:
            logger.log(f"POST /notifications/send - User '{user_name}' not found.")
            return {'message': f'User "{user_name}" not found'}, 404

        notification = Notification(user_name, message, priority)
        
        # Build the Chain of Responsibility for the user
        chain_builder = ChannelChainBuilder()
        head_handler = chain_builder.build_chain(user)

        if not head_handler:
            logger.log(f"POST /notifications/send - No valid channels configured for user '{user_name}'.")
            return {'message': f'No valid channels configured for user "{user_name}".'}, 500

        # Initiate the notification sending process through the chain
        logger.log(f"Initiating notification delivery for user '{user_name}'.")
        delivery_successful = head_handler.send(notification, user)

        if delivery_successful:
            logger.log(f"Notification '{message}' successfully delivered to '{user_name}' via one of the channels.")
            return {'message': 'Notification process initiated. Check logs for delivery status.'}, 200
        else:
            logger.log(f"Notification '{message}' failed to deliver to '{user_name}' via any available channel.")
            return {'message': 'Notification delivery failed for all available channels.'}, 500

# Add the namespaces to the API
api.add_namespace(users_ns)
api.add_namespace(notifications_ns)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5000)

