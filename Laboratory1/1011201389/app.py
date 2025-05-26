from flask import Flask, jsonify, request
from flasgger import Swagger

# Validators
from handlers.register.register_handlers import NameHandler, PreferredChannelHandler, AvailableChannelsHandler, PreferredInAvailableChannelsHandler
from handlers.notification.notification_handlers import UserNameHandler, MessageHandler, PriorityHandler

# Database
from database.database import database_users

# Models
from user import User
from notification import Notification

app = Flask(__name__)
swagger = Swagger(app)

# Validate user data definition
validator_user_data = NameHandler(PreferredChannelHandler(AvailableChannelsHandler(PreferredInAvailableChannelsHandler())))

# Validate notification data definition
validator_notification_data = UserNameHandler(MessageHandler(PriorityHandler()))

# Enpoints definition

# Register users
@app.post('/users')
def register_user():
    """
    Create a user
    ---
    tags:
        - User
    parameters:
        - in: body
          name: body
          required: true
          schema:
            id: User
            properties:
                name:
                    type: string
                    description: Name of the user
                    example: Samuel
                preferred_channel:
                    type: string
                    description: Preferred channel of the user
                    example: sms
                available_channels:
                    type: array
                    description: List of every available channel of the user
                    example: ["sms", "console"]
            required:
                - name
                - preferred_channel
                - available_channels
    responses:
        201:
            description: User created
            examples:
                application/json: {"name": "Samuel",
                                    "preferred_channel": "sms",
                                    "available_channels": ["sms", "console"]
                                } 
        400:
            description: Invalid input
            examples:
                application/json: {"error": "'name' must be a non-empty string"}

    """
    data = request.get_json()
    try:
        validator_user_data.handle(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    # Check if user already exists
    for user in database_users:
        if user.name == data.get("name"):
            return jsonify({"error": "User already exists"}), 400

    # Create user
    user = User.from_dict(data)
    database_users.append(user)

    return jsonify(data), 201

# Get users
@app.get('/users')
def get_users():
    """
    Obtain all users
    --- 
    tags:
        - User
    responses:
        200:
            description: All the users
            examples:
                application/json:
                    [
                        {"name": "Samuel",
                            "preferred_channel": "sms",
                            "available_channels": ["sms", "console"]
                        },
                        {"name": "Josué",
                            "preferred_channel": "console",
                            "available_channels": ["email", "console"]
                        } 
                    ]
    """
    return jsonify([user.to_dict() for user in database_users]), 200

# Send a notification
@app.route('/notifications/send', methods=["POST"])
def send_notification():
    """
    Send a notification message to a specific user
    --- 
    tags:
        - Notification
    parameters:
        - in: body
          name: body
          required: true
          schema:
            id: Notification
            required:
                - user_name
                - message
                - priority
            properties:
                user_name:
                    type: string
                    description: Name of the user to send the notification to
                    example: Samuel
                message:
                    type: string
                    description: Message to send to the user
                    example: "Hello, Samuel! This is a test notification."
                priority:
                    type: string
                    description: Priority of the notification
                    example: "high"
                    enum:
                        - low
                        - medium
                        - high
    responses:
        200:
            description: Notification sent successfully
            examples:
                application/json: {"status": "Notification sent successfully through sms channel"}
        400:
            description: Invalid input
            examples:
                application/json: {"error": "User not found"}
            
    """

    data = request.get_json()

    try:
        validator_notification_data.handle(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    # Check if user exists
    user = next((user for user in database_users if user.name == data.get("user_name")), None)
    if not user:
        return jsonify({"error": "User not found"}), 400
    
    # Create notification
    notification = Notification.from_dict(data)

    # TODO: Implement the logic to send the notification through the user's preferred channel using chain of responsibility pattern
    # For now, we will just return a success message
    return jsonify({"status": f"Notification sent successfully through {user.preferred_channel} channel"}), 200
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)