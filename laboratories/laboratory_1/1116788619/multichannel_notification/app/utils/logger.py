import threading
import datetime

class LoggerSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance.logs = []
        return cls._instance

    def log(self, channel, user, message, status):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} | Canal: {channel} | Usuario: {user['name']} | Mensaje: '{message}' | Estado: {status}"
        print(entry)
        self.logs.append(entry)

    def get_logs(self):
        return self.logs
