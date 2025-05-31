from flask import Flask, send_from_directory
import os
from utils.swagger_setup import setup_swagger
from utils.generate_swagger import generate_swagger_json
from .views.users import users_blueprint    
from .views.notifications import notifications_blueprint

def create_app():
    app = Flask(__name__)

    # Configuración Swagger
    setup_swagger(app)
    generate_swagger_json()

    # Registro de blueprints
    app.register_blueprint(users_blueprint)
    app.register_blueprint(notifications_blueprint)


    @app.route("/static/swagger.json")
    def specs():
        return send_from_directory(os.getcwd(), "static/swagger.json")
    
    print(app.url_map)

    return app