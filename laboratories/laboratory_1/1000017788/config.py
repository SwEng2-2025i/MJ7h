"""
Configuration file for the notification system
"""

import os

class Config:
    """
    Application configuration
    """
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API configuration
    API_TITLE = 'Multichannel Notification System API'
    API_VERSION = '1.0'
    API_DESCRIPTION = 'A modular REST API for managing users and sending notifications using design patterns'
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'notification_system.log')
    
    # Notification configuration
    VALID_CHANNELS = ['email', 'sms', 'console']
    VALID_PRIORITIES = ['high', 'medium', 'low']
    
    # Simulation configuration
    FAILURE_SIMULATION = True  # Set to False to disable random failures

class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """
    Testing configuration
    """
    TESTING = True
    DEBUG = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
