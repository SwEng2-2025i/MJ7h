def log_attempts(func):
    """
    Decorador para agregar logging antes y después de intentar enviar una notificación.
    Muestra si el intento fue exitoso o fallido en el canal actual.
    """
    def wrapper(self, user_name, message):
        self.logger.log(f"Attempting to send to {user_name} via {self.channel.upper()}...")
        result = func(self, user_name, message)
        status = "SUCCESS" if result else "FAILED"
        self.logger.log(f"Result for {user_name} via {self.channel.upper()}: {status}")
        return result
    return wrapper
