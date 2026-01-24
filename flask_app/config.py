"""
Configuraciones de la aplicación Flask.
"""

import os


class Config:
    """Configuración base."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    ENV = 'production'


# Mapeo de configuraciones
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
