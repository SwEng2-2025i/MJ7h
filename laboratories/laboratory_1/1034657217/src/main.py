from flask import Flask
from flask_restx import Api
from utils.logger import Logger
from model.usersModel import UsersModel # Importa tu UsersModel
from services.notification_service import NotificationService

# Importa las funciones de inicialización de rutas
from routes.users import init_user_routes
from routes.notifications import init_notification_routes

logger =Logger()
logger.startLog()
UsersModel()
app = Flask(__name__)
api = Api(app,
          title="Multichannel Notification System APIMartin Moreno", 
          description="Swagger documentation for Laboratory 1",
          version="1.0",
          doc='/swagger-ui')

# Instanciar UsersModel y obtener la lista de usuarios en memoria
users_model_singleton_instance = UsersModel() 

# Instanciar el NotificationService, pasándole la lista de usuarios
notification_service_instance = NotificationService()

# --- Inicializar y agregar Namespaces ---
user_ns = init_user_routes(api, users_model_singleton_instance)
notification_ns = init_notification_routes(api, notification_service_instance)

api.add_namespace(user_ns)
api.add_namespace(notification_ns)


@app.route('/')
def home():
    return "Welcome to the Multichannel Notification System API! Access Swagger UI at /swagger-ui"

if __name__=="__main__":
    app.run(debug=True)