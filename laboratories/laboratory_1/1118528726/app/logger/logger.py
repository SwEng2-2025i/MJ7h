import threading
from datetime import datetime

class LoggerSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(LoggerSingleton, cls).__new__(cls)
                    cls._instance.log_file = "notification.log"
        return cls._instance

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
