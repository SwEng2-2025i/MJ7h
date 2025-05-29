from werkzeug.utils import quote as url_quote
from flask import Flask
from flask_restx import Api
from app.api.user_api import user_ns
from app.api.notification_api import notification_ns

def create_app():
    app = Flask(__name__)
    
    # Configuración clave para resolver el 405:
    app.config['SWAGGER_SUPPORTED_SUBMIT_METHODS'] = ['get', 'post']
    app.config['ERROR_INCLUDE_MESSAGE'] = False
    app.config['RESTX_MASK_SWAGGER'] = False

    api = Api(
        app,
        version='1.0',
        doc='/docs',
        default='users',
        default_label='User operations',
        title='Multichannel Notification System API',
        description='A REST API for sending notifications through multiple channels'
    )
    
    api.add_namespace(user_ns)
    api.add_namespace(notification_ns)
    
    return app