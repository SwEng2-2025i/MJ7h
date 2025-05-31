from flask import Flask
from flask_restx import Api
from utils.logger import Logger
from model.usersModel import UsersModel 
from services.notification_service import NotificationService

""""
Application entry point
Includes swagger logic, which makes it be
written in a roundabout way
"""
# Importar las funciones de inicialización de rutas
from routes.users import init_user_routes
from routes.notifications import init_notification_routes

# Initialize instances of singleton objects
logger =Logger()
logger.startLog()
UsersModel()
app = Flask(__name__)
api = Api(app,
          title="Multichannel Notification System APIMartin Moreno", 
          description="Swagger documentation for Laboratory 1",
          version="1.0",
          doc='/swagger-ui')

# Instance of userModel for swagger
users_model_singleton_instance = UsersModel() 

# Instance of notificationService
notification_service_instance = NotificationService()

# Add namespaces for routes and for swagger
user_ns = init_user_routes(api, users_model_singleton_instance)
notification_ns = init_notification_routes(api, notification_service_instance)

api.add_namespace(user_ns)
api.add_namespace(notification_ns)


@app.route('/')
def home():
    return "Welcome to the Multichannel Notification System API! Access Swagger UI at /swagger-ui"

if __name__=="__main__":
    app.run(debug=True)