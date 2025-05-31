# app.py
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from controllers.user_controller import user_bp
from controllers.notification_controller import notification_bp


# Crear una instancia de Flask y Swagger
app = Flask(__name__)
swagger = Swagger(app) # habilitar swagger 

# Limitar el numero de peticiones por minuto (5 peticiones por minuto)
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])


# Registrar los blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(notification_bp, url_prefix='/notifications')

if __name__ == '__main__':
    app.run(debug=True)