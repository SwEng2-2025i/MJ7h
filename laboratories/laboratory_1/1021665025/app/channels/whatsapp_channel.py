from .base_channel import BaseChannel
from app.utils.logger import logger

class WhatsappChannel(BaseChannel):
    #Hereda de `BaseChannel` e implementa la lógica específica para "enviar"
    #(simular el envío) de notificaciones por WhatsApp.

    def _process_send(self, user_name: str, message: str) -> bool:
        #Simula el envío de una notificación por WhatsApp.
        #Registra el intento de envío y el resultado (éxito/fallo simulado).

        logger.info(f"Intentando enviar notificacion a '{user_name}' por WhatsApp: '{message}'")
        # Simulación de éxito/fallo
        success = self._simulate_failure()
        if success:
            logger.info(f"Mensaje de WhatsApp enviado con exito a '{user_name}'.")
            return True
        else:
            logger.warning(f"Fallo al enviar mensaje de WhatsApp a '{user_name}'.")
            return False

    def channel_name(self) -> str:
        return "whatsapp" 