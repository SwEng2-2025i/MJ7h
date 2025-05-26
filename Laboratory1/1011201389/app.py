from flask import Flask, jsonify, request
from flasgger import Swagger

# Validators
from handlers.register.register_handlers import NameHandler, PreferredChannelHandler, AvailableChannelsHandler, PreferredInAvailableChannelsHandler

# Database
from database.database import database_users

# Models
from user import User

app = Flask(__name__)
swagger = Swagger(app)

# Validate user data definition
validator_user_data = NameHandler(PreferredChannelHandler(AvailableChannelsHandler(PreferredInAvailableChannelsHandler())))

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
            required:
                - name
                - preferred_channel
                - available_channels
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
        400:
            description: Invalid input

    """
    data = request.get_json()
    try:
        validator_user_data.handle(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    # Create user
    user = User.from_dict(data)
    database_users.append(user)

    return jsonify(data), 201

# Get users
@app.get('/users')
def get_users():
    return jsonify([user.to_dict() for user in database_users]), 200

# Send a notification
@app.route('/notifications/send', methods=["POST"])
def send_notification():
    pass

if __name__ == '__main__':
    app.run(debug=True)