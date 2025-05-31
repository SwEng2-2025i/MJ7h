import datetime

class Logger:
    """
    Singleton Logger class to centralize logging of notification attempts.
    Ensures only one instance of the logger exists throughout the application.
    """
    _instance = None
    _log_messages = [] # In-memory storage for log messages

    def __new__(cls):
        """
        Controls the creation of Logger instances, ensuring only one is ever created.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            print("Logger instance created.") # For demonstration
        return cls._instance

    @classmethod
    def get_instance(cls):
        """
        Returns the single instance of the Logger.
        """
        if cls._instance is None:
            cls() # Create the instance if it doesn't exist
        return cls._instance

    def log(self, message: str):
        """
        Logs a message with a timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self._log_messages.append(log_entry)
        print(f"LOG: {log_entry}") # Also print to console for real-time visibility

    def get_logs(self):
        """
        Retrieves all logged messages.
        """
        return self._log_messages
