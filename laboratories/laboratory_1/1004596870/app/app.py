from flask import Flask, request, jsonify
from channels.channel_factory import ChannelFactory
from services.notification_service import NotificationService
from models.user import User
from utils.logger import Logger

app = Flask(__name__)

users = []  # almacenamiento en memoria
logger = Logger.get_instance()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        name=data['name'],
        preferred_channel=data['preferred_channel'],
        available_channels=data['available_channels']
    )
    users.append(user)
    logger.log(f"User created: {user.name}")
    return jsonify({"message": "User registered successfully."}), 201

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify([user.to_dict() for user in users])

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.json
    user_name = data['user_name']
    message = data['message']
    priority = data['priority']

    user = next((u for u in users if u.name == user_name), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    factory = ChannelFactory()
    channels = [factory.create_channel(c) for c in user.available_channels]

    service = NotificationService(channels)
    result = service.send(user.preferred_channel, message)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
