# api/main.py
from flask import Flask
from flask_restful import Api
from flasgger import Swagger 

def create_app() -> Flask:
    """Fábrica de la aplicación Flask.

    - Crea la instancia `app`.
    - Registra los recursos REST.
    - Devuelve un servidor listo para ejecutar pruebas o correr en prod.
    """
    app = Flask(__name__)
    Swagger(app) 
    api = Api(app)

    # ---------- Health-check ------------------------------------------------
    @app.route("/")
    def health():
        """Endpoint de latido (readiness probe para Docker/K8s)."""
        return {"status": "OK"}

    # ---------- Importación diferida de recursos ---------------------------
    # Mantener las importaciones aquí evita ciclos (api → resources → api).
    from API.resources.user import UserResource
    from API.resources.notification import NotificationSendResource

    api.add_resource(UserResource, "/users", endpoint="users")
    api.add_resource(NotificationSendResource,
                     "/notifications/send",
                     endpoint="notifications_send")

    return app


# ---------- Arranque local -------------------------------------------------
if __name__ == "__main__":
    # DEBUG solo en desarrollo.  En prod usa gunicorn/uwsgi y DEBUG=False.
    create_app().run(debug=True)
