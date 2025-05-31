from flask_restx import Resource
from datetime import datetime
from extensions import api

# Endpoint para verificar el estado de salud del servicio (health check)
class HealthResource(Resource):

    @api.doc('health_check')             # Nombre del endpoint en la documentación Swagger
    @api.response(200, 'Service is healthy')  # Respuesta esperada si todo está bien
    def get(self):
        """
        GET /health

        Verifica si la API está operativa. 
        Útil para monitoreo y automatización de despliegues (DevOps).
        """
        return {
            'status': 'healthy',                              # Estado general del servicio
            'timestamp': datetime.now().isoformat(),          # Fecha y hora actual
            'service': 'Multichannel Notification System'     # Nombre del servicio
        }, 200
