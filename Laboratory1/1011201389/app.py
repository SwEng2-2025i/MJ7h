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
@app.route('/notifications/send')
def send_notification():
    pass

if __name__ == '__main__':
    app.run(debug=True)