# Módulo con el  logger Singleton para registrar eventos de notificación.

import logging

class SingletonLogger:
    _instance = None

    def __new__(cls):
        """
        Implementa el patrón Singleton asegurando una única instancia del logger.
        """
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            # Config del logger
            logging.basicConfig(
                filename='notifications.log',
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            cls._instance.logger = logging.getLogger('NotificationLogger')
        return cls._instance

    def info(self, message: str):
        """
        Registra un mensaje de nivel INFO.
        Args:
            message: Mensaje a registrar.
        """
        self.logger.info(message)

    def error(self, message: str):
        """
        Registra un mensaje de ERROR.
        Args:
            message: Mensaje a registrar.
        """
        self.logger.error(message)