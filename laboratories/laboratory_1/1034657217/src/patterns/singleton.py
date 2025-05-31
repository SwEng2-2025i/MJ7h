class Singleton:
    _instance = None
    """
    Asures the existance of a single instance of a class 
    by storing the first instance of said class and not
    allowing more instances
    """
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance