from flask_restx import Api

# Instancia global de la API RESTx
# Esta instancia se importa en `app.py` y se inicializa con la aplicación Flask
# Configuración de la documentación Swagger en la ruta /swagger/
api = Api(
    doc='/swagger/',  # Ruta donde se expone la documentación Swagger
    title='Multichannel Notification System API',  # Título visible en Swagger UI
    description='A REST API for managing users and sending notifications through multiple channels'  # Descripción general del sistema
)
