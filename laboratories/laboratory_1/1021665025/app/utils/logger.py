import logging
import sys

class Logger:
    #Clase Singleton para gestionar el logging en toda la aplicación.
    #Esta clase asegura que solo exista una instancia del logger y proporciona
    #un punto de acceso global para registrar mensajes. Registra los mensajes
    _instance = None

    def __new__(cls):
        #Sobrescribe el método __new__ para implementar el patrón Singleton.
        #Si no existe una instancia, crea una nueva; de lo contrario, retorna la existente.

        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        #Inicializa el logger con la configuración deseada.
        self.logger = logging.getLogger("NotificationAppLogger")
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Manejador para la consola
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # Manejador para el archivo
        file_handler = logging.FileHandler('app.log') # Los logs se guardarán en el directorio raíz del proyecto
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

# Punto de acceso global a la instancia del Logger
logger = Logger() 