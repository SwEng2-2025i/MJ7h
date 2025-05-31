from flask import Flask, request, jsonify
from models import User
from channels import EmailChannel, SMSChannel, ConsoleChannel
from logger import Logger
import yaml

app = Flask(__name__)

users = {}

# Helper to build channel chain
CHANNEL_CLASSES = {
    'email': EmailChannel,
    'sms': SMSChannel,
    'console': ConsoleChannel
}

def build_channel_chain(preferred, available):
    chain = None
    last = None
    # Order: preferred first, then others
    ordered = [preferred] + [ch for ch in available if ch != preferred]
    for ch in ordered:
        if ch in CHANNEL_CLASSES:
            node = CHANNEL_CLASSES[ch]()
            if not chain:
                chain = node
            if last:
                last.set_next(node)
            last = node
    return chain

@app.route('/users', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels', [])
    if not name or not preferred or not available:
        return jsonify({'error': 'Missing fields'}), 400
    if name in users:
        return jsonify({'error': 'User already exists'}), 400
    user = User(name, preferred, available)
    users[name] = user
    return jsonify({'message': 'User registered', 'user': user.to_dict()}), 201

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify([u.to_dict() for u in users.values()])

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.json
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority')
    if not user_name or not message or not priority:
        return jsonify({'error': 'Missing fields'}), 400
    user = users.get(user_name)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    chain = build_channel_chain(user.preferred_channel, user.available_channels)
    delivered = chain.send(user.to_dict(), message)
    return jsonify({'delivered': delivered}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    logger = Logger()
    return jsonify(logger.get_logs())

@app.route('/swagger')
def swagger_spec():
    with open('swagger.yaml', 'r') as f:
        return app.response_class(f.read(), mimetype='application/yaml')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Notification System API is running."}), 200

if __name__ == '__main__':
    app.run(debug=True)
