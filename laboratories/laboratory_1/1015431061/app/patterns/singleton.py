class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.log_messages = []
        return cls._instance

    def log(self, message):
        self.log_messages.append(message)
        print(f"[LOG] {message}")

    def get_logs(self):
        return self.log_messages