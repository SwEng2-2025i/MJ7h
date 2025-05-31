from flask import Flask
from flasgger import Swagger
from routes.routes import bp

def create_app():
    app = Flask(__name__)
    
    # Swagger configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Notification Service API",
            "description": "API para gestión de usuarios y envío de notificaciones a través de múltiples canales (email, SMS, consola). Implementa el patrón Chain of Responsibility para el manejo de notificaciones.",
            "contact": {
                "name": "API Support",
                "email": "support@notificationservice.com"
            },
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": [
            "http"
        ],
        "consumes": [
            "application/json"
        ],
        "produces": [
            "application/json"
        ],
        "tags": [
            {
                "name": "Users",
                "description": "Operaciones relacionadas con la gestión de usuarios"
            },
            {
                "name": "Notifications", 
                "description": "Operaciones para el envío de notificaciones"
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Import blueprint with correct path
    
    app.register_blueprint(bp)
    
    return app
