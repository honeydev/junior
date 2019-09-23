"""Модуль настроек проекта."""

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Config:
    DEBUG = os.getenv('DEBUG', False)
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    SECRET_KEY = 'SOSECRET'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgres://junior:junior@127.0.0.1:5432/junior'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    extend_existing = True