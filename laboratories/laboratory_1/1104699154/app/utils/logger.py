import threading
from datetime import datetime

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def log(self, channel, message, status):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] Channel: {channel.upper()} | Status: {status.upper()} | Message: {message}")
