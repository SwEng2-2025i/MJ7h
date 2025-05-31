from flask import Flask
from flasgger import Swagger
from app.routes import api_blueprint

app = Flask(__name__)
swagger = Swagger(app)  # Inicializa Flasgger para documentación Swagger automática

# Registro del blueprint que contiene las rutas API
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    # Ejecuta la app en modo debug (auto-reload, más info en consola)
    app.run(debug=True)
