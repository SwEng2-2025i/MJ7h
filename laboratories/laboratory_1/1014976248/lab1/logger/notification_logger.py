import logging
from datetime import datetime
from typing import List, Dict

# Logger especializado en registrar intentos de notificación.
# Implementa el patrón Singleton para mantener una única instancia compartida.

class NotificationLogger:
    _instance = None               # Instancia única (Singleton)
    _initialized = False           # Bandera para evitar múltiples inicializaciones

    def __new__(cls):
        # Controla la creación de la instancia para garantizar un único objeto (Singleton)
        if cls._instance is None:
            cls._instance = super(NotificationLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Inicialización de atributos solo una vez
        if not NotificationLogger._initialized:
            self.logger = logging.getLogger('NotificationSystem')   # Logger de Python
            self.logger.setLevel(logging.INFO)

            # Configura el formato y salida del logger
            ch = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            # Historial interno de intentos de envío
            self.notification_history: List[Dict] = []

            NotificationLogger._initialized = True

    def log_attempt(self, user_name: str, channel: str, message: str, success: bool, priority: str = "normal"):
        """
        Registra un intento de envío, exitoso o fallido, tanto en consola como en el historial interno.

        :param user_name: Nombre del destinatario
        :param channel: Canal utilizado (email, SMS, etc.)
        :param message: Mensaje enviado
        :param success: True si fue exitoso, False si falló
        :param priority: Nivel de prioridad del mensaje
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_name': user_name,
            'channel': channel,
            'message': message,
            'success': success,
            'priority': priority
        }
        self.notification_history.append(log_entry)

        # Mensajes diferenciados según el resultado
        if success:
            self.logger.info(f"✅ Notification sent to {user_name} via {channel}: {message}")
        else:
            self.logger.warning(f"❌ Failed to send notification to {user_name} via {channel}: {message}")

    def get_history(self) -> List[Dict]:
        """
        Devuelve una copia del historial de intentos de notificación.

        :return: Lista de diccionarios con cada intento registrado
        """
        return self.notification_history.copy()
