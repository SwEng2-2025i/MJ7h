from flask import Flask
from extensions import api  # Importa la instancia de API desde el archivo centralizado de extensiones

# Inicializa la aplicación Flask
app = Flask(__name__)
api.init_app(app)  # Asocia la API RESTx con la app de Flask

# Importación de los recursos de la API REST (endpoints)
from api.users import UsersResource
from api.notifications import NotificationResource, NotificationHistoryResource
from api.channels import ChannelsResource
from api.health import HealthResource

# Asociación de rutas con recursos REST
api.add_resource(UsersResource, '/users')  # Registrar usuario y listar usuarios
api.add_resource(NotificationResource, '/notifications/send')  # Enviar notificación
api.add_resource(NotificationHistoryResource, '/notifications/history')  # Historial de notificaciones
api.add_resource(ChannelsResource, '/channels')  # Obtener canales disponibles
api.add_resource(HealthResource, '/health')  # Endpoint de verificación de estado

# Punto de entrada principal del servidor
if __name__ == '__main__':
    # Ejecuta la aplicación en modo desarrollo, accesible desde cualquier IP
    app.run(debug=True, host='0.0.0.0', port=5000)
