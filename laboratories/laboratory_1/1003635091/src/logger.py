class Logger:
    # Variable de clase para almacenar la única instancia
    _instance = None
    
    def __new__(cls):
        """
        Método especial para controlar la creación de instancias.
        Implementa el patrón Singleton garantizando una única instancia.
        
        Returns:
            Logger: La instancia única del logger
        """
        # Verificar si ya existe una instancia
        if cls._instance is None:
            # Crear nueva instancia si no existe
            cls._instance = super(Logger, cls).__new__(cls)
            # Aquí podrían inicializarse recursos (ej: archivo de log)
        return cls._instance
    
    def log(self, message, level="INFO"):
        """
        Registra un mensaje en el logger con el nivel especificado
        
        Args:
            message (str): Mensaje a registrar
            level (str, optional): Nivel de severidad. Default: "INFO"
        
        Output:
            Imprime en consola el mensaje formateado: [NIVEL] mensaje
        """
        # Formatear entrada de log
        log_entry = f"[{level}] {message}"
        
        # En producción aquí se añadiría a un archivo
        print(log_entry)