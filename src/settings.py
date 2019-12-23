"""Модуль настроек проекта."""

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Config:
    APP_NAME = os.getenv('APP_NAME', 'Junior')
    DEBUG = os.getenv('DEBUG', False)
    CSRF_ENABLED = os.getenv('CSRF_ENABLED', True)
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', 'dsofpkoasodksap')
    SECRET_KEY = os.getenv('SECRET_KEY', 'SOSECRET')
    DB_ENGINE = os.getenv('ENGINE', 'postgres')
    DB_USER = os.getenv('DB_USER', 'junior')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'junior')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'junior')
    DB_PORT = os.getenv('DB_PORT', 5432)
    SQLALCHEMY_DATABASE_URI = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OAUTH_BACKEND = os.getenv('OAUTH_BACKEND', '').split()


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    extend_existing = True


class TestConfig(ProductionConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite://')
    OAUTH_BACKEND = os.getenv('TEST_OAUTH_BACKEND', 'github').split()
