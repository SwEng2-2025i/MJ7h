from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from services.notification_service import NotificationService
from utils.logger import NotificationLogger

app = Flask(__name__)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Notification System API",
        "description": "A multichannel notification system with chain of responsibility pattern",
        "version": "1.0.0"
    }
})
notification_service = NotificationService()
logger = NotificationLogger()

@app.route('/users', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'preferred_channel', 'available_channels'],
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Name of the user'
                    },
                    'preferred_channel': {
                        'type': 'string',
                        'enum': ['email', 'sms', 'console'],
                        'description': 'Preferred notification channel'
                    },
                    'available_channels': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'enum': ['email', 'sms', 'console']
                        },
                        'description': 'List of available notification channels'
                    }
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'User registered successfully'
        },
        '400': {
            'description': 'Invalid input'
        }
    }
})
def register_user():
    data = request.get_json()
    
    required_fields = ['name', 'preferred_channel', 'available_channels']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    success = notification_service.register_user(
        data['name'],
        data['preferred_channel'],
        data['available_channels']
    )
    
    if success:
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": "Failed to register user"}), 400

@app.route('/users', methods=['GET'])
@swag_from({
    'responses': {
        '200': {
            'description': 'List of all registered users',
            'schema': {
                'type': 'object',
                'properties': {
                    'users': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string'},
                                'preferred_channel': {'type': 'string'},
                                'available_channels': {
                                    'type': 'array',
                                    'items': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def list_users():
    users = notification_service.get_users()
    return jsonify({"users": users}), 200

@app.route('/send', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['user_name', 'message', 'priority'],
                'properties': {
                    'user_name': {
                        'type': 'string',
                        'description': 'Name of the user to send notification to'
                    },
                    'message': {
                        'type': 'string',
                        'description': 'Notification message content'
                    },
                    'priority': {
                        'type': 'string',
                        'enum': ['low', 'medium', 'high'],
                        'description': 'Priority level of the notification'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Notification sent successfully'
        },
        '400': {
            'description': 'Invalid input or user not found'
        }
    }
})
def send_notification():
    data = request.get_json()
    
    required_fields = ['user_name', 'message', 'priority']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    success = notification_service.send_notification(
        data['user_name'],
        data['message'],
        data['priority']
    )
    
    if success:
        return jsonify({"message": "Notification sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send notification"}), 400

if __name__ == '__main__':
    app.run(debug=True)
