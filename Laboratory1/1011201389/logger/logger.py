class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.log_file = "app.log"

    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + "\n")