import threading

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Logger, cls).__new__(cls)
                    cls._instance.logs = []
        return cls._instance

    def log(self, message):
        self.logs.append(message)
        print(message)

    def get_logs(self):
        return self.logs
