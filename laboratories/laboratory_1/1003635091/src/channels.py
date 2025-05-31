"""
channels.py - Implementación del patrón Chain of Responsibility para manejo de canales de notificación

Este módulo define los manejadores concretos para cada canal de notificación (email, SMS, consola)
utilizando el patrón Chain of Responsibility. Cada manejador:
1. Intenta enviar una notificación por su canal
2. Simula un resultado aleatorio (éxito o fallo)
3. Si falla, pasa la solicitud al siguiente manejador en la cadena

Clases:
- ChannelHandler: Clase abstracta base para todos los manejadores
- EmailHandler: Manejador para notificaciones por email
- SMSHandler: Manejador para notificaciones por SMS
- ConsoleHandler: Manejador para notificaciones por consola
"""

import random
from abc import ABC, abstractmethod
from logger import Logger  # Logger Singleton para registro de eventos

# Instancia global del logger
logger = Logger()

class ChannelHandler(ABC):
    """
    Clase base abstracta para los manejadores de canales de notificación.
    Implementa el patrón Chain of Responsibility.
    
    Atributos:
        next_handler (ChannelHandler): Referencia al siguiente manejador en la cadena
        
    Métodos:
        set_next(handler): Establece el siguiente manejador en la cadena
        handle(user, message): Método abstracto para procesar la notificación
    """
    
    def __init__(self):
        """Inicializa el manejador sin siguiente handler"""
        self.next_handler = None
    
    def set_next(self, handler):
        """
        Establece el siguiente manejador en la cadena de responsabilidad
        
        Args:
            handler (ChannelHandler): Siguiente manejador en la cadena
            
        Returns:
            ChannelHandler: El manejador establecido (para permitir encadenamiento)
        """
        self.next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, user, message):
        """
        Método abstracto para manejar una notificación
        
        Args:
            user (User): Objeto usuario con preferencias y canales disponibles
            message (str): Contenido de la notificación
            
        Returns:
            str|None: Nombre del canal si tuvo éxito, None si falló
        """
        pass

class EmailHandler(ChannelHandler):
    """Manejador concreto para notificaciones por email"""
    
    def handle(self, user, message):
        """
        Intenta enviar la notificación por email
        
        Pasos:
        1. Verifica si el usuario tiene habilitado el canal de email
        2. Simula envío con resultado aleatorio (50% éxito)
        3. Si falla, pasa al siguiente manejador en la cadena
        """
        # Verificar si el canal está disponible para el usuario
        if 'email' in user.available_channels:
            # Simular éxito o fallo aleatorio
            success = random.choice([True, False])
            # Registrar intento
            logger.log(f"Attempting email to {user.name}: {'Success' if success else 'Fail'}")
            
            # Retornar si fue exitoso
            if success:
                return 'email'
        
        # Pasar al siguiente manejador si existe
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return None  # Fin de la cadena sin éxito

class SMSHandler(ChannelHandler):
    """Manejador concreto para notificaciones por SMS"""
    
    def handle(self, user, message):
        """
        Intenta enviar la notificación por SMS
        
        Misma lógica que EmailHandler pero para canal SMS
        """
        if 'sms' in user.available_channels:
            success = random.choice([True, False])
            logger.log(f"Attempting SMS to {user.name}: {'Success' if success else 'Fail'}")
            if success:
                return 'sms'
                
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return None

class ConsoleHandler(ChannelHandler):
    """Manejador concreto para notificaciones por consola"""
    
    def handle(self, user, message):
        """
        Intenta enviar la notificación por consola
        
        Misma lógica que otros handlers pero para canal consola
        """
        if 'console' in user.available_channels:
            success = random.choice([True, False])
            logger.log(f"Attempting console to {user.name}: {'Success' if success else 'Fail'}")
            if success:
                return 'console'
                
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return None