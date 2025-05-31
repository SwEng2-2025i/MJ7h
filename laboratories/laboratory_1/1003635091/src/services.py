from models import User, Notification
from channels import EmailHandler, SMSHandler, ConsoleHandler
from logger import Logger

logger = Logger()

class UserService:
    SUPPORTED_CHANNELS = ['email', 'sms', 'console']  # Canales válidos
    
    def __init__(self):
        """Servicio para gestión de usuarios en memoria"""
        self.users = []
    
    def register_user(self, name, preferred_channel, available_channels):
        """
        Registra un nuevo usuario con validación de datos
        
        Args:
            name: Nombre del usuario
            preferred_channel: Canal de notificación preferido
            available_channels: Canales disponibles para el usuario
        
        Returns:
            Objeto User registrado
        
        Raises:
            ValueError: Si los datos son inválidos
        """
        # Validación de campos requeridos
        if not all([name, preferred_channel, available_channels]):
            raise ValueError("Missing required fields")
        
        # Validación de canales soportados
        if preferred_channel not in self.SUPPORTED_CHANNELS:
            raise ValueError(f"Unsupported preferred channel: {preferred_channel}")
        
        for channel in available_channels:
            if channel not in self.SUPPORTED_CHANNELS:
                raise ValueError(f"Unsupported channel: {channel}")
        
        # Validación de consistencia de canales
        if preferred_channel not in available_channels:
            raise ValueError("Preferred channel must be in available channels")
        
        user = User(name, preferred_channel, available_channels)
        self.users.append(user)
        return user
    
    def get_all_users(self):
        """Obtiene todos los usuarios registrados"""
        return self.users
    
    def find_user(self, name):
        """
        Busca un usuario por nombre
        
        Args:
            name: Nombre del usuario a buscar
        
        Returns:
            Objeto User encontrado
        
        Raises:
            ValueError: Si el usuario no existe
        """
        for user in self.users:
            if user.name == name:
                return user
        raise ValueError("User not found")

class NotificationService:
    def __init__(self, user_service):
        """
        Servicio para envío de notificaciones usando Chain of Responsibility
        
        Args:
            user_service: Instancia de UserService para acceso a usuarios
        """
        self.user_service = user_service
        # Crear handlers (no encadenar aún)
        self.handlers = {
            'email': EmailHandler(),
            'sms': SMSHandler(),
            'console': ConsoleHandler()
        }
        # Construir cadena: email -> sms -> console
        self.handlers['email'].set_next(self.handlers['sms'])
        self.handlers['sms'].set_next(self.handlers['console'])
    
    def send_notification(self, user_name, message, priority):
        """
        Envía una notificación usando la cadena de responsabilidad
        
        Args:
            user_name: Nombre del usuario destino
            message: Contenido de la notificación
            priority: Prioridad de la notificación
        
        Returns:
            Diccionario con resultado del envío
        """
        user = self.user_service.find_user(user_name)
        
        logger.log(f"Sending notification to {user_name} ({priority}): {message}")
        
        # Iniciar cadena en el handler del canal preferido
        preferred_handler = self.handlers.get(user.preferred_channel)
        if not preferred_handler:
            logger.log(f"Preferred channel '{user.preferred_channel}' not found", "ERROR")
            return {
                'status': 'failed',
                'message': 'Preferred channel handler not available',
                'user': user.name
            }
        
        # Ejecutar la cadena desde el canal preferido
        result = preferred_handler.handle(user, message)
        
        # Retornar resultado basado en el éxito
        if result:
            return {
                'status': 'success',
                'message': 'Notification delivered',
                'channel': result,
                'user': user.name
            }
        
        return {
            'status': 'failed',
            'message': 'All delivery channels failed',
            'user': user.name
        }