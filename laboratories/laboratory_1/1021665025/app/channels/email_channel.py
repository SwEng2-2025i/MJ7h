from .base_channel import BaseChannel
from app.utils.logger import logger

class EmailChannel(BaseChannel):
    #Hereda de `BaseChannel` e implementa la lógica específica para "enviar"
    #(simular el envío) de notificaciones por email.

    def _process_send(self, user_name: str, message: str) -> bool:
        #Simula el envío de una notificación por correo electrónico.
        #Registra el intento de envío y el resultado (éxito/fallo simulado).

        logger.info(f"Intentando enviar notificacion a '{user_name}' por Email: '{message}'")
        success = self._simulate_failure()
        if success:
            logger.info(f"Email enviado con exito a '{user_name}'.")
            return True
        else:
            logger.warning(f"Fallo al enviar email a '{user_name}'.")
            return False

    def channel_name(self) -> str:
        return "email" 