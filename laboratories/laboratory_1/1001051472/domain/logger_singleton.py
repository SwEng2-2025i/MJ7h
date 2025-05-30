# Implementación del patrón Singleton para el logger
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []  # Lista para almacenar los logs
        return cls._instance

    def log(self, message):
        """Imprime y almacena un mensaje de log."""
        print(f"[LOG] {message}")
        self.logs.append(message)

    def get_logs(self):
        """Devuelve la lista de logs almacenados."""
        return self.logs
