class NotificationLogger:
    """Clase singleton para registrar intentos de notificación.
    """
    _instance = None
    def __new__(cls):
        # Verifica si ya existe una instancia (por lo del singleton)
        if cls._instance is None:
            cls._instance = super(NotificationLogger, cls).__new__(cls)
            cls._instance.records = []
        return cls._instance
    #intento de loguear un mensaje de notificación
    def log_attempt(self, user_name, channel, message, success):
        record = {
            'user': user_name,
            'channel': channel,
            'message': message,
            'success': success
        }
        # Agregar el registro a la lista de registros
        self.records.append(record)
        print(f"[LOG] user: {user_name}, channel: {channel}, success: {success}")
    # Obtiene todos los registros de notificación
    def get_logs(self):
        return list(self.records)

# Instancia global accesible directamente
logger = NotificationLogger()