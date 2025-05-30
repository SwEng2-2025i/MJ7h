"""
Singleton Pattern Implementation
Ensures only one instance of the logger exists throughout the application
"""

import logging
from datetime import datetime
from typing import List

class NotificationLogger:
    """
    Singleton logger for notification system
    Ensures only one logger instance exists
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """
        Ensure only one instance is created
        """
        if cls._instance is None:
            cls._instance = super(NotificationLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Initialize the logger (only once)
        """
        if not NotificationLogger._initialized:
            self.logs: List[str] = []
            self._setup_logging()
            NotificationLogger._initialized = True
    
    def _setup_logging(self):
        """
        Setup logging configuration
        """
        # Configure logging with UTF-8 encoding for Windows compatibility
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',            handlers=[
                logging.FileHandler('notification_system.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('NotificationSystem')
        
        # Set console handler encoding for Windows
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                try:
                    handler.stream.reconfigure(encoding='utf-8')
                except AttributeError:
                    # Fallback for older Python versions
                    pass
        
        self.log("Notification Logger initialized (Singleton pattern)")
    
    def log(self, message: str):
        """
        Log a message
        
        Args:
            message: The message to log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # Store in memory
        self.logs.append(formatted_message)
        
        # Clean message for Windows console compatibility
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        
        # Log to file and console
        self.logger.info(safe_message)
    
    def get_logs(self) -> List[str]:
        """
        Get all logged messages
        
        Returns:
            List of all logged messages
        """
        return self.logs.copy()
    
    def clear_logs(self):
        """
        Clear all logged messages
        """
        self.logs.clear()
        self.log("Logs cleared")

# Global instance access
def get_logger():
    """
    Get the singleton logger instance
    
    Returns:
        NotificationLogger instance
    """
    return NotificationLogger()
