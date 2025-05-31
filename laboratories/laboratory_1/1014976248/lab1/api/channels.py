from flask_restx import Resource
from extensions import api
from factories.strategy_factory import NotificationStrategyFactory

# Endpoint que expone los canales disponibles de notificación.
class ChannelsResource(Resource):

    @api.doc('get_available_channels')  # Documentación Swagger: nombre del endpoint
    @api.response(200, 'Success')       # Respuesta esperada si todo sale bien
    def get(self):
        """
        GET /channels

        Retorna la lista de tipos de canales de notificación disponibles 
        (por ejemplo: email, sms, push, console), junto con el total.
        """
        try:
            # Obtiene los canales desde la fábrica de estrategias
            channels = NotificationStrategyFactory.get_available_channels()
            return {
                'channels': channels,     # Lista de canales soportados
                'total': len(channels)    # Cantidad total
            }, 200
        except Exception as e:
            # Captura errores inesperados y retorna un mensaje de error estándar
            return {'error': f'Internal server error: {str(e)}'}, 500
