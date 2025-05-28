from flask import Flask
from flasgger import Swagger
from app.routes.user_routes import user_routes
from app.routes.notification_routes import notification_routes



def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_routes)
    app.register_blueprint(notification_routes)
    swagger = Swagger(app) #documentar API
    return app

