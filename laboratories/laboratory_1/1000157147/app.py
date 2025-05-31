from flask import Flask, request, jsonify
from models.user import User
from data.store import users
from services.notification_service import send_notification
from logger.logger_singleton import Logger
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app)

@app.route("/users", methods=["POST"])
def create_user():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              example: "Diego"
            preferred_channel:
              type: string
              example: "email"
            available_channels:
              type: array
              items:
                type: string
              example: ["email", "sms", "console"]
    responses:
      201:
        description: Usuario registrado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario Diego registrado"
    """
    data = request.get_json()
    user = User(
        name=data["name"],
        preferred_channel=data["preferred_channel"],
        available_channels=data["available_channels"]
    )
    users[user.name] = user
    return jsonify({"message": f"Usuario {user.name} registrado"}), 201

@app.route("/users", methods=["GET"])
def list_users():
    """
    Listar todos los usuarios registrados
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios registrados
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              preferred_channel:
                type: string
              available_channels:
                type: array
                items:
                  type: string
    """

    return jsonify([
        {"name": u.name, "preferred_channel": u.preferred_channel, "available_channels": u.available_channels}
        for u in users.values()
    ])

@app.route("/notifications/send", methods=["POST"])
def send():
    """
    Enviar una notificación a un usuario
    ---
    tags:
      - Notificaciones
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              example: "Diego"
            message:
              type: string
              example: "Recordatorio: tu cita es mañana"
            priority:
              type: string
              example: "alta"
    responses:
      200:
        description: Notificación enviada con éxito
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Notificación enviada con éxito"
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Usuario no encontrado"
      500:
        description: Fallaron todos los intentos de notificación
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Fallaron todos los intentos de notificación"
    """
    data = request.get_json()
    user_name = data["user_name"]
    message = data["message"]
    user = users.get(user_name)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    success = send_notification(user, message)
    if success:
        return jsonify({"message": "Notificación enviada con éxito"})
    else:
        return jsonify({"message": "Fallaron todos los intentos de notificación"}), 500

if __name__ == "__main__":
    app.run(debug=True)
