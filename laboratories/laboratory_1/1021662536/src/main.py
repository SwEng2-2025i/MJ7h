# Módulo principal que configura la API REST con Flask y Flask-RESTx
# Define los endpoints y usa Swagger para documentación

from flask import Flask
from flask_restx import Api, Resource, fields
from src.models.user import User
from src.models.notification import Notification
from src.handlers.notification_handler import NotificationHandler

# Inicializar la aplicación Flask y la API con Flask-RESTx
app = Flask(__name__)
api = Api(
    app,
    title="Sistema de Notificaciones Multicanal - Gabriela Gallegos Rubio",
    description="API REST para gestionar usuarios y enviar notificaciones. Se implementa a través de patrones de diseño (Singleton, Chain of responsibility, Factory method).",
)
ns = api.namespace("api : ", description="Operaciones de notificaciones y gestión de usuarios")

# Modelos para Swagger
user_model = api.model("User", {
    "name": fields.String(required=True, description="Nombre del usuario"),
    "fav_channel": fields.String(required=True, description="Canal favorito de notificación"),
    "available_channels": fields.List(fields.String, required=True, description="Lista de canales disponibles")
})

notification_model = api.model("Notification", {
    "user_name": fields.String(required=True, description="Nombre del usuario destino"),
    "message": fields.String(required=True, description="Mensaje de la notificación"),
    "priority": fields.String(required=True, description="Prioridad de la notificación")
})

# Almacenamiento en memoria para usuarios
users = []

@ns.route("/users")
class UserResource(Resource):
    @ns.expect(user_model)
    @ns.response(201, "Usuario creado con éxito")
    @ns.response(400, "Datos inválidos")
    def post(self):
        """
        Registra un nuevo usuario con nombre, canal preferido y canales disponibles.
        """
        data = api.payload

        # Verificar que los datos estén completos
        if not all(key in data for key in ["name", "fav_channel", "available_channels"]):
            return {"message": "Faltan campos requeridos"}, 400
        # Veficar que el canal preferido esté en los canales disponibles
        if data["fav_channel"] not in data["available_channels"]:
            return {"message": "El canal favorito debe estar en los canales disponibles"}, 400
        user = User(data["name"], data["fav_channel"], data["available_channels"])
        users.append(user)
        return {"message": "Usuario creado", "user": user.to_dict()}, 201

    @ns.response(200, "Lista de usuarios")
    def get(self):
        """
        Devuelve la lista de todos los usuarios registrados.
        """
        return {"users": [user.to_dict() for user in users]}, 200

@ns.route("/notifications/send")
class NotificationResource(Resource):
    @ns.expect(notification_model)
    @ns.response(200, "Notificación enviada con éxito")
    @ns.response(404, "Usuario no encontrado")
    @ns.response(400, "Fallo al enviar la notificación")
    def post(self):
        """
        Envía una notificación a un usuario usando la cadena de canales.
        """
        data = api.payload
        # Validar que los datos estén completos
        if not all(key in data for key in ["user_name", "message", "priority"]):
            return {"message": "Faltan campos requeridos"}, 400
        # Buscar el usuario
        user = next((u for u in users if u.name == data["user_name"]), None)
        if not user:
            return {"message": "Usuario no encontrado"}, 404
        
        # Crear y enviar la notificación
        notification = Notification(data["user_name"], data["message"], data["priority"])
        handler = NotificationHandler()
        success = handler.send_notification(user, notification)
        return {"message": "Notificación enviada" if success else "Error al enviar notificación"}, 200 if success else 400

if __name__ == "__main__":
    app.run(debug=True)