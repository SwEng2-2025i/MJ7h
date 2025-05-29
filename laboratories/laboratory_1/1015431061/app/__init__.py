from flask import Flask, redirect
from flask_restx import Api
from flask_cors import CORS  # Importante para evitar problemas CORS en desarrollo

def create_app():
    # Inicialización básica de Flask
    app = Flask(__name__)
    
    # Configuración crítica para evitar errores 405
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config['ERROR_404_HELP'] = False
    
    @app.route('/')
    def index():
        return redirect('/docs')
    @app.after_request
    def set_charset(response):
        if response.mimetype == 'application/json':
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    # Habilitar CORS para desarrollo (opcional pero recomendado)
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE"]
        }
    })
    
    # Configuración óptima de Flask-RESTX
    api = Api(
    app,
    version='1.0',
    title='Notification System API',
    description='API para el sistema de notificaciones multicanal',
    doc='/docs',   # la doc queda fuera del prefix /api
    prefix='/api', # todas las rutas empiezan con /api
    validate=True
)
    
    # Importar y registrar namespaces
    from app.api.user_api import user_ns
    from app.api.notification_api import notification_ns
    
    api.add_namespace(user_ns)
    api.add_namespace(notification_ns)
    
    return app
