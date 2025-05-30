from flask import Flask, request, jsonify
from application.use_cases import NotificationUseCase
from infrastructure.in_memory_repo import InMemoryUserRepository
from domain.logger_singleton import Logger

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
                preferred_channel:
                  type: string
                available_channels:
                  type: array
                  items:
                    type: string
        responses:
          201:
            description: Usuario registrado exitosamente
          400:
            description: Error en los datos enviados
        """
        data = request.json
        try:
            use_case.register_user(data["name"], data["preferred_channel"], data["available_channels"])
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
                message:
                  type: string
                priority:
                  type: string
        responses:
          200:
            description: Notificación enviada
          400:
            description: Error en los datos enviados
        """
        data = request.json
        result = use_case.send_notification(data["user_name"], data["message"], data["priority"])
        return jsonify(result)

    return app
