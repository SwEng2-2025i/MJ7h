class Logger:
    _instance = None

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("Logger is a singleton!")
        else:
            Logger._instance = self

    def log(self, message):
        print(f"[LOG]: {message}")