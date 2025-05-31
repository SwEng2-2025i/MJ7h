class Logger:
    """
    Logger es una clase singleton que gestiona los registros (logs) de la aplicación.

    Al ser singleton, garantiza que todos los módulos utilicen la misma instancia para logging.
    Los logs se almacenan en memoria en una lista y también se imprimen por consola.

    Métodos:
        log(message): Agrega un mensaje a los logs.
        get_logs(): Devuelve la lista de logs almacenados.
    """
    _instance = None

    def __new__(cls):
        """
        Crea o retorna la única instancia de Logger.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message):
        """
        Agrega un mensaje al log y lo imprime en consola.

        Args:
            message (str): Mensaje a registrar.
        """
        self.logs.append(message)
        print(f"[LOG] {message}")

    def get_logs(self):
        """
        Devuelve todos los mensajes registrados.

        Returns:
            list: Lista de mensajes de log.
        """
        return self.logs
