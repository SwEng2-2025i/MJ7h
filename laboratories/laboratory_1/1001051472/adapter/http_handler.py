from flask import Flask, request, jsonify
from application.use_cases import NotificationUseCase
from infrastructure.in_memory_repo import InMemoryUserRepository
from domain.logger_singleton import Logger

# Canales válidos para el sistema
VALID_CHANNELS = {"email", "sms", "console"}

# Se agrega integración con Swagger usando flasgger
def create_app():
    app = Flask(__name__)
    try:
        from flasgger import Swagger
        Swagger(app)
    except ImportError:
        pass  # Si flasgger no está instalado, la app sigue funcionando sin Swagger

    logger = Logger()  # Logger Singleton
    repo = InMemoryUserRepository()  # Repositorio en memoria
    use_case = NotificationUseCase(repo, logger)

    @app.route("/users", methods=["POST"])
    def create_user():
        """
        Registrar un usuario
        ---
        tags:
          - Usuarios
        parameters:
          - in: body
            name: user
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: Juan
                preferred_channel:
                  type: string
                  enum: [email, sms, console]
                  example: email
                available_channels:
                  type: array
                  items:
                    type: string
                    enum: [email, sms, console]
                  example: ["email", "sms"]
        responses:
          201:
            description: Usuario registrado exitosamente
            examples:
              application/json: { "message": "User registered successfully" }
          400:
            description: Error en los datos enviados
            examples:
              application/json: { "error": "Canal no válido. Solo se permiten: email, sms, console." }
        """
        data = request.json
        # Validar canales
        preferred = data.get("preferred_channel")
        available = data.get("available_channels", [])
        if preferred not in VALID_CHANNELS or any(ch not in VALID_CHANNELS for ch in available):
            return jsonify({"error": "Canal no válido. Solo se permiten: email, sms, console."}), 400
        if preferred not in available:
            return jsonify({"error": "El canal preferido debe estar en los canales disponibles."}), 400
        try:
            use_case.register_user(data["name"], preferred, available)
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/users", methods=["GET"])
    def list_users():
        """
        Listar todos los usuarios
        ---
        tags:
          - Usuarios
        responses:
          200:
            description: Lista de usuarios
            examples:
              application/json: [
                {
                  "name": "Juan",
                  "preferred_channel": "email",
                  "available_channels": ["email", "sms"]
                }
              ]
        """
        users = use_case.list_users()
        return jsonify(users)

    @app.route("/notifications/send", methods=["POST"])
    def send_notification():
        """
        Enviar una notificación a un usuario
        ---
        tags:
          - Notificaciones
        parameters:
          - in: body
            name: notification
            required: true
            schema:
              type: object
              properties:
                user_name:
                  type: string
                  example: Juan
                message:
                  type: string
                  example: Tu cita es mañana.
                priority:
                  type: string
                  example: high
        responses:
          200:
            description: Notificación enviada
            examples:
              application/json: { "status": "delivered", "via": "Email" }
          400:
            description: Error en los datos enviados
            examples:
              application/json: { "status": "failed", "reason": "User not found" }
        """
        data = request.json
        result = use_case.send_notification(data["user_name"], data["message"], data["priority"])
        return jsonify(result)

    return app
